from PIL import Image
from array import array

import arcade
import arcade.gl as gl
from arcade.gui import bind
from arcade.resources import resolve_resource_path

import style


class HitboxFrame:

    def __init__(self, parent_widget):
        self._parent = parent_widget
        bind(parent_widget, "rect", self.change_parent_rect)

        self.ctx = arcade.get_window().ctx

        self.frame_texture = self.ctx.texture(size=parent_widget.size)
        self.frame_fbo = self.ctx.framebuffer(color_attachments=[self.frame_texture])

        self.checkerboard_texture = self.ctx.texture(
            size=(32, 32), data=Image.open(resolve_resource_path(":source:/Checkerboard.png")).tobytes(),
            filter=(gl.NEAREST, gl.NEAREST))

        self.final_render_program = self.ctx.load_program(
            vertex_shader=":source:/shaders/hitbox_frame_vert.glsl",
            fragment_shader=":source:/shaders/hitbox_frame_frag.glsl"
        )

        self.current_sprite = arcade.Sprite(":source:/DiceBaggie.png")
        self.sprite_cam = arcade.Camera(*self.frame_fbo.size)

        # The variables used to position the checkerboard, sprite, and hit-boxes in the frame.
        self._zoom = 1
        self._pos = (0.0, 0.0)
        self._size = self.frame_texture.size
        self._shift = (0.0, 0.0)

        self.final_render_program['pos'] = 0.0, 0.0
        self.final_render_program['size'] = self.frame_texture.size

        self.final_render_program['checkerUV'] = 800 / 32 * self._zoom, 800 / 32 * self._zoom
        self.final_render_program['shift'] = 0.0, 0.0

        self.final_render_program['checkerBoard'] = 0
        self.final_render_program['hitboxFramebuffer'] = 1

        self.square_geo = self.ctx.geometry(
            [gl.BufferDescription(self.ctx.buffer(data=array('f', (0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0))),
                                  '2f', ['in_uv'])], mode=gl.TRIANGLE_STRIP)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self.final_render_program['pos'] = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self.final_render_program['size'] = value
        self.final_render_program['checkerUV'] = self._size[0] / 32 * self._zoom, self._size[1] / 32 * self._zoom
        self.frame_texture.resize(value)

    @property
    def shift(self):
        return self._shift

    @shift.setter
    def shift(self, value):
        self._shift = value
        self.final_render_program['shift'] = self._shift

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        self._zoom = value
        self.final_render_program['checkerUV'] = self._size[0] / 32 * self._zoom, self._size[1] / 32 * self._zoom

    def change_parent_rect(self):
        size = self._parent.size
        self.size = int(size[0]-2), int(size[1]-2)
        pos = self._parent.position
        self.pos = int(pos[0]+1), int(pos[1]+1)

    def update_all_variables(self, pos=None, size=None, shift=None, zoom=None):
        if any((pos, size, shift, zoom)):
            self._pos = pos or self._pos
            self._size = size or self._size
            self._shift = shift or self._shift
            self._zoom = zoom or self._zoom

            self.final_render_program['pos'] = self._pos
            self.final_render_program['size'] = self._size

            self.final_render_program['checkerUV'] = self._size[0] / 32 * self._zoom, self._size[1] / 32 * self._zoom
            self.final_render_program['shift'] = self._shift

    def draw(self):
        with self.frame_fbo.activate() as _fbo:
            _fbo.clear((0, 0, 0, 0))
            self.current_sprite.draw(pixelated=True)
        self.checkerboard_texture.use(0)
        self.frame_texture.use(1)
        self.square_geo.render(self.final_render_program)

