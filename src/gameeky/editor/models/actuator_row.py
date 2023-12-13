from typing import Optional, List
from gettext import gettext as _

from gi.repository import Gio

from .base_row import BaseRow

from ...server.game.actuators.base import ActuatorRegistry


class ActuatorRow(BaseRow):
    __gtype_name__ = "ActuatorRowModel"

    __items__ = {
        "activates": _("Activates"),
        "activates_i": _("Activates on interaction"),
        "affects": _("Affects"),
        "affects_i": _("Affects on interaction"),
        "aggroes": _("Aggroes"),
        "collapses": _("Collapses"),
        "collapses_t": _("Collapses over time"),
        "destroys": _("Destroys"),
        "destroys_i": _("Destroys on interaction"),
        "deteriorates": _("Deteriorates"),
        "drops": _("Drops"),
        "exhausts": _("Exhausts"),
        "follows": _("Follows"),
        "interacts": _("Interacts"),
        "propulses": _("Propulses"),
        "requires": _("Requires"),
        "roams": _("Roams"),
        "spawns": _("Spawns"),
        "takes": _("Takes"),
        "targets": _("Targets"),
        "teleports": _("Teleports"),
        "teleports_i": _("Teleports on interaction"),
        "transmutes": _("Transmutes"),
        "triggers": _("Triggers"),
        "triggers_i": _("Triggers on interaction"),
        "uses": _("Uses"),
    }

    @classmethod
    def model(cls, default=False, exclude: Optional[List[str]] = None) -> Gio.ListStore:
        model = super().model()

        for value in ActuatorRegistry.names():
            model.append(cls(value=value, text=value))

        return model