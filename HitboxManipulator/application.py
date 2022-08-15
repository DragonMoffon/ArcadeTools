import arcade

from tool_gui import GUIManager
import style


class App(arcade.Window):

    def __init__(self):
        super().__init__(title="HitBox Manipulator - A dev tool for Python Arcade.", resizable=True)
        style.read_style(":source:/style.json")
        self.set_minimum_size(600, 450)
        self.background_color = style.COLOURS['-background-primary']
        self._ui_manager = GUIManager(self)
        self._ui_manager.enable()

        # self._hitbox_frame_renderer = HitboxFrame(self._ui_manager._base_slots._primarY_tab.._hitbox_frame)

    def on_draw(self):
        self.clear()
        self._ui_manager.draw()
        # self._hitbox_frame_renderer.draw()

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        pass
        # self._hitbox_frame_renderer.zoom = (self._hitbox_frame_renderer.zoom - scroll_y / 1000) % 2

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        pass
        # shift = list(self._hitbox_frame_renderer.shift)
        # zoom = self._hitbox_frame_renderer.zoom
        # shift[0] -= dx / 32 * zoom
        # shift[1] -= dy / 32 * zoom
        # self._hitbox_frame_renderer.shift = shift
