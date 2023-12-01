import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gtk, Adw, GObject

from .scene_settings import SceneSettings

from ...common.utils import valid_directory
from ...common.scanner import Description


@Gtk.Template(filename=os.path.join(__dir__, "scene_new_window.ui"))
class SceneNewWindow(Adw.Window):
    __gtype_name__ = "SceneNewWindow"

    __gsignals__ = {
        "done": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    toast = Gtk.Template.Child()
    content = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self._scene_settings = SceneSettings()
        self.content.props.child = self._scene_settings

    def _notify(self, title) -> None:
        toast = Adw.Toast()
        toast.props.title = title
        toast.props.timeout = 3

        self.toast.add_toast(toast)

    @Gtk.Template.Callback("on_cancel_clicked")
    def __on_cancel_clicked(self, button: Gtk.Button) -> None:
        self.destroy()

    @Gtk.Template.Callback("on_create_clicked")
    def __on_create_clicked(self, button: Gtk.Button) -> None:
        if not self.title:
            self._notify("A valid name must be provided")
            return

        if not valid_directory(self.data_path):
            self._notify("A valid project must be provided")
            return

        self.emit("done")
        self.close()

    @property
    def title(self) -> str:
        return self._scene_settings.title

    @property
    def data_path(self) -> None:
        return self._scene_settings.data_path

    @property
    def description(self) -> Description:
        return self._scene_settings.description
