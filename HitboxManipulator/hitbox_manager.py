from typing import List

from arcade import Texture, load_texture, draw_point, draw_line, get_window
import arcade.color as colors
import arcade.key as key

from hitbox_data import FrameData, HitboxData
from hitbox_renderers import Frame, Sprite, Hitbox


class HitboxManager:
    """
    The Hitbox manager holds each object required to edit and create a hitbox.
    :Frame data: holds all data relating to the frame which the hitbox is rendered to.

    :Sprites: lists the arcade.Textures.
    :Hitboxes: lists the hitbox data. This includes the references to the GPU buffers for the hitbox.
    :Frame Renderer: Renders the frame which includes a fbo that the other renders draw to.
    :Sprite Renderer: Renders the currently active texture
    :Hitbox Renderer: Renders the currently active hitbox
    """

    def __init__(self, frame_parent):
        self._frame_data: FrameData = FrameData(frame_parent, 1/3, (0.0, 0.0))
        self._sprites: List[Texture] = [load_texture(":source:/DiceBaggie.png")]
        self._hitboxes: List[HitboxData] = [HitboxData(self._sprites[0], (1.0, 1.0, 0.0))]

        self._frame_renderer = Frame(self._frame_data)
        self._sprite_renderer = Sprite(self._frame_data)
        self._hitbox_renderer = Hitbox(self._frame_data)

        self._sprite_renderer.texture = self._sprites[0]
        self._hitbox_renderer.add_hitbox(self._hitboxes[0])

        self._active_hitbox = self._hitboxes[0]

        self._mouse_pos = (0, 0)

        self._window = get_window()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self._mouse_pos = (x, y)
        f_d = self._frame_data
        rel_x = (x - f_d.x)
        rel_y = (y - f_d.y)
        if 0 <= rel_x <= f_d.size[0] and 0 <= rel_y <= f_d.size[1]:
            rel_x -= f_d.size[0]/2
            rel_y -= f_d.size[1]/2
            old_zoom = f_d.zoom
            f_d.zoom = ((int(f_d.size[0]*f_d.zoom) - int(scroll_y)*3) / f_d.size[0]) % 2 or 2
            zoom_change = (old_zoom - f_d.zoom)
            s = f_d.shift
            f_d.shift = s[0] + rel_x * zoom_change, s[1] + rel_y * zoom_change

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self._mouse_pos = (x, y)
        if buttons & 4:
            rel_x = (x - self._frame_data.x)
            rel_y = (y - self._frame_data.y)
            if 0 <= rel_x <= self._frame_data.size[0] and 0 <= rel_y <= self._frame_data.size[1]:
                shift = list(self._frame_data.shift)
                zoom = self._frame_data.zoom
                shift[0] -= dx * zoom
                shift[1] -= dy * zoom
                self._frame_data.shift = shift

    def on_mouse_press(self, x, y, button, modifiers):
        self._mouse_pos = (x, y)
        if button == 1:
            rel_x = (x - self._frame_data.x)
            rel_y = (y - self._frame_data.y)
            if 0 <= rel_x <= self._frame_data.size[0] and 0 <= rel_y <= self._frame_data.size[1]:
                rel_x = self._frame_data.zoom * (rel_x - self._frame_data.size[0] // 2)  # -width to width
                rel_y = self._frame_data.zoom * (rel_y - self._frame_data.size[1] // 2)  # -height to height

                rel_x = int(rel_x + self._frame_data.shift[0])  # / self._active_hitbox.sprite_size[0]
                rel_y = int(rel_y + self._frame_data.shift[1])  # / self._active_hitbox.sprite_size[1]

                self._active_hitbox.add_point((rel_x, rel_y))

    def mouse_move(self, x, y):
        self._mouse_pos = (x, y)

    def mouse_frame_pos(self):
        rel_x = int((self._window.mouse['x'] - self._frame_data.frame_pos[0]) * (self._window.width/self._frame_data.size[0]))
        rel_y = int((self._window.mouse['y'] - self._frame_data.frame_pos[1]) * (self._window.height/self._frame_data.size[1]))
        return rel_x, rel_y

    def draw(self):
        with self._frame_renderer.activate_fbo() as fbo:
            fbo.clear((0.0, 0.0, 0.0, 0.0))
            self._sprite_renderer.draw()
            self._hitbox_renderer.draw()
            draw_point(*self.mouse_frame_pos(), colors.ORANGE_RED, 4)

        self._frame_renderer.draw()

    def on_key_press(self, button):
        _shift = self._frame_data.shift
        if button == key.W:
            self._frame_data.shift = _shift[0]+16, _shift[1]+16
        elif button == key.S:
            self._frame_data.shift = _shift[0]-16, _shift[1]-16



