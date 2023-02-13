from math import sqrt

import arcade

from tool_gui import GUIManager
from hitbox_manager import HitboxManager
import style


class App(arcade.Window):

    def __init__(self):
        super().__init__(title="HitBox Manipulator - A dev tool for Python Arcade.", resizable=True)
        style.read_style(":source:/style.json")
        self.set_minimum_size(600, 450)
        self.background_color = style.COLOURS['-background-primary']
        self._ui_manager = GUIManager(self)
        self._ui_manager.enable()

        self._hitbox_manager = HitboxManager(self._ui_manager._base_slots._primary_tab._hitbox_line._hitbox_frame)

        self._current_pixel = None

        # Vector Test
        self.p_1 = (300, 120)
        self.p_2 = (540, 145)
        self.p_3 = (0, 0)
        self.v_1 = self.p_2[0] - self.p_1[0], self.p_2[1] - self.p_1[1]
        _len = sqrt(self.v_1[0]**2 + self.v_1[0]**2)
        self.n_1 = -self.v_1[1] / _len, self.v_1[0] / _len
        self.n_2 = self.v_1[0] / _len, self.v_1[1] / _len
        self.v_2 = (0, 0)

    def on_draw(self):
        self.clear()
        # self._ui_manager.draw()
        # self._hitbox_manager.draw()

        arcade.draw_line(*self.p_1, *self.p_2, arcade.color.RHYTHM, 2)
        arcade.draw_line(*self.p_1, self.p_1[0] + self.n_1[0] * 60, self.p_1[1] + self.n_1[1] * 60, arcade.color.ORANGE_RED, 2)
        arcade.draw_line(*self.p_1, *self.p_3, arcade.color.ROSE, 2)
        #arcade.draw_point(*self.p_3, arcade.color.ROSE, 4)
        dot_1 = self.n_1[0] * self.v_2[0] + self.n_1[1] * self.v_2[1]
        v_3 = self.n_1[0] * dot_1 * 2, self.n_1[1] * dot_1 * 2
        dot_2 = self.n_2[0] * self.v_2[0] + self.n_2[1] * self.v_2[1]
        v_4 = self.n_2[0] * dot_2 * 2, self.n_2[1] * dot_2 * 2
        arcade.draw_line(self.p_1[0]+v_4[0], self.p_1[1]+v_4[1],
                         self.p_1[0]+v_4[0]+v_3[0], self.p_1[1]+v_4[1]+v_3[1],
                         arcade.color.PEAR, 2)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.close()
        else:
            self._hitbox_manager.on_key_press(symbol)

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        self._hitbox_manager.on_mouse_scroll(x, y, scroll_x, scroll_y)

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        self._hitbox_manager.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self._hitbox_manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.p_3 = (x, y)
        self.v_2 = x - self.p_1[0], y - self.p_1[1]
        self._hitbox_manager.mouse_move(x, y)
