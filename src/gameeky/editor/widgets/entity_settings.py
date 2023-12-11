from typing import Optional

from gi.repository import GLib, Gtk, GObject

from .actuators_row import ActuatorsRow
from .utils import get_position_in_model

from ...common.scanner import Description
from ...common.definitions import DEFAULT_TIMEOUT


@Gtk.Template(resource_path="/dev/tchx84/gameeky/editor/widgets/entity_settings.ui")  # fmt: skip
class EntitySettings(Gtk.Box):
    __gtype_name__ = "EntitySettings"

    __gsignals__ = {
        "changed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    name = Gtk.Template.Child()
    target_name = Gtk.Template.Child()
    stamina = Gtk.Template.Child()
    durability = Gtk.Template.Child()
    weight = Gtk.Template.Child()
    strength = Gtk.Template.Child()
    target_type = Gtk.Template.Child()
    radius = Gtk.Template.Child()
    rate = Gtk.Template.Child()
    recovery = Gtk.Template.Child()
    density = Gtk.Template.Child()
    luminance = Gtk.Template.Child()
    removable = Gtk.Template.Child()
    takeable = Gtk.Template.Child()
    usable = Gtk.Template.Child()
    visible = Gtk.Template.Child()
    direction = Gtk.Template.Child()
    state = Gtk.Template.Child()
    actuators = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._handler_id: Optional[int] = None

        self._actuators = ActuatorsRow()
        self._actuators.connect("changed", self.__on_changed)
        self.actuators.props.child = self._actuators

        # XXX Move these to UI file somehow
        self.removable.connect("notify::active", self.__on_changed)
        self.takeable.connect("notify::active", self.__on_changed)
        self.usable.connect("notify::active", self.__on_changed)
        self.visible.connect("notify::active", self.__on_changed)
        self.direction.connect("notify::selected-item", self.__on_changed)
        self.state.connect("notify::selected-item", self.__on_changed)

    @Gtk.Template.Callback("on_changed")
    def __on_changed(self, *args) -> None:
        if self._handler_id is not None:
            GLib.Source.remove(self._handler_id)

        self._handler_id = GLib.timeout_add_seconds(
            DEFAULT_TIMEOUT / 2,
            self.__on_change_delayed,
        )

    def __on_change_delayed(self) -> int:
        self.emit("changed")
        self._handler_id = None
        return GLib.SOURCE_REMOVE

    @property
    def description(self) -> Description:
        return Description(
            name=self.name.props.text,
            target_name=self.target_name.props.text,
            stamina=int(self.stamina.props.value),
            durability=int(self.durability.props.value),
            weight=int(self.weight.props.value),
            strength=int(self.strength.props.value),
            target_type=int(self.target_type.props.value),
            radius=int(self.radius.props.value),
            rate=int(self.rate.props.value),
            recovery=round(self.recovery.props.value, 2),
            density=round(self.density.props.value, 2),
            luminance=round(self.luminance.props.value, 2),
            removable=self.removable.props.active,
            takeable=self.takeable.props.active,
            usable=self.usable.props.active,
            visible=self.visible.props.active,
            direction=self.direction.props.selected_item.props.string,
            state=self.state.props.selected_item.props.string,
            actuators=self._actuators.value,
        )

    @description.setter
    def description(self, description: Description) -> None:
        self.name.props.text = description.name
        self.target_name.props.text = description.target_name
        self.stamina.props.value = description.stamina
        self.durability.props.value = description.durability
        self.weight.props.value = description.weight
        self.strength.props.value = description.strength
        self.target_type.props.value = description.target_type
        self.radius.props.value = description.radius
        self.rate.props.value = description.rate
        self.recovery.props.value = description.recovery
        self.density.props.value = description.density
        self.luminance.props.value = description.luminance
        self.removable.props.active = description.removable
        self.takeable.props.active = description.takeable
        self.usable.props.active = description.usable
        self.visible.props.active = description.visible
        self.direction.props.selected = get_position_in_model(
            self.direction.props.model, description.direction
        )
        self.state.props.selected = get_position_in_model(
            self.state.props.model, description.state
        )
        self._actuators.value = description.actuators