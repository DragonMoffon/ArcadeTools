from PIL import Image
from array import array
from contextlib import contextmanager

import arcade.gl as gl
from arcade import get_window, TextureAtlas, Texture
from arcade.gui import bind
from arcade.resources import resolve_resource_path

from hitbox_data import FrameData, HitboxData

from typing import Set


class Frame:
    def __init__(self, data):
        self._ctx = get_window().ctx
        self._data: FrameData = data

        # Bind the changing of the frame data to calling methods in the Frame renderer.
        bind(self._data, "frame_zoom", self.zoom)
        bind(self._data, "frame_shift", self.shift)
        bind(self._data, "frame_pos", self.pos)
        bind(self._data, "frame_size", self.size)

        # The texture and fbo that the sprite and hitboxes will draw to
        self._texture = self._ctx.texture(size=self._data.frame_size)
        self._fbo = self._ctx.framebuffer(color_attachments=[self._texture])

        # Checkerboard texture which is repeated in the final render
        self._checkerboard_texture = self._ctx.texture(
            size=(32, 32), data=Image.open(resolve_resource_path(":source:/Checkerboard.png")).tobytes(),
            filter=(gl.NEAREST, gl.NEAREST))

        # program for rendering to the screen.
        self._program = self._ctx.load_program(
            vertex_shader=":source:/shaders/hitbox_frame_vert.glsl",
            fragment_shader=":source:/shaders/hitbox_frame_frag.glsl"
        )

        # passing uniform variables to the program.
        self._program['pos'] = self._data.pos
        self._program['size'] = self._data.size

        self._program['checkerUV'] = (self._data.size[0] / 32 * self._data.zoom,
                                      self._data.size[1] / 32 * self._data.zoom)

        self._program['shift'] = self._data.shift

        self._program['checkerBoard'] = 0
        self._program['hitboxFramebuffer'] = 1

        # geometry for rendering to the screen.
        self._geo = self._ctx.geometry(
            [gl.BufferDescription(self._ctx.buffer(data=array('f', (0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0))),
                                  '2f', ['in_uv'])], mode=gl.TRIANGLE_STRIP)

    def zoom(self):
        self._program['checkerUV'] = (self._data.size[0] / 32 * self._data.zoom,
                                      self._data.size[1] / 32 * self._data.zoom)

    def shift(self):
        self._program['shift'] = self._data.shift

    def pos(self):
        self._program['pos'] = self._data.pos

    def size(self):
        self._program['size'] = self._data.size
        self._program['checkerUV'] = (self._data.size[0] / 32 * self._data.zoom,
                                      self._data.size[1] / 32 * self._data.zoom)

        self._texture.resize(self._data.size)
        self._fbo.resize()

    @contextmanager
    def activate_fbo(self):
        prev_fbo = self._ctx.active_framebuffer
        try:
            self._fbo.use()
            yield self._fbo
        finally:
            prev_fbo.use()

    def draw(self):
        self._checkerboard_texture.use(0)
        self._texture.use(1)
        self._geo.render(self._program)


class Sprite:

    def __init__(self, frame_data: FrameData, atlas: TextureAtlas = None):
        _ctx = get_window().ctx
        self._atlas: TextureAtlas = atlas or _ctx.default_atlas
        self._atlas.texture.filter = (gl.NEAREST, gl.NEAREST)

        self._current_texture: Texture = None

        self._frame_data = frame_data
        bind(frame_data, "frame_size", self._size)
        bind(frame_data, "frame_shift", self._shift)
        bind(frame_data, "frame_zoom", self._zoom)

        # ModernGl components for rendering
        self._render_program = _ctx.load_program(vertex_shader=":source:/shaders/sprite_render_vert.glsl",
                                                 fragment_shader=":source:/shaders/sprite_render_frag.glsl")
        self._render_geo = _ctx.geometry(
            [gl.BufferDescription(_ctx.buffer(data=array('f', (0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0))),
                                  '2f', ['vertUV'])], mode=gl.TRIANGLE_STRIP)

        # Setting program Uniforms
        self._render_program['textureInfo'] = 0
        self._render_program['textureAtlas'] = 1
        self._render_program['frameSize'] = frame_data.size

    def _size(self):
        self._render_program['frameSize'] = self._frame_data.size

    def _shift(self):
        self._render_program['shift'] = self._frame_data.shift

    def _zoom(self):
        self._render_program['zoom'] = self._frame_data.zoom

    @property
    def texture(self):
        return self._current_texture

    @texture.setter
    def texture(self, value: Texture):
        self._current_texture = value

        if value is not None:
            self._atlas.add(value)
            self._render_program['tex_id'] = self._atlas.get_texture_id(value.name)
            self._render_program['spriteSize'] = value.size

    def draw(self):
        if self._current_texture:
            self._render_program['shift'] = self._frame_data.shift
            self._render_program['zoom'] = self._frame_data.zoom
            self._atlas.use_uv_texture(0)
            self._atlas.texture.use(1)
            self._render_geo.render(self._render_program)


class Hitbox:

    def __init__(self, frame_data: FrameData):
        self._frame_data = frame_data
        bind(frame_data, "frame_size", self._size)
        bind(frame_data, "frame_shift", self._shift)
        bind(frame_data, "frame_zoom", self._zoom)

        self._ctx = get_window().ctx
        self._render_program = self._ctx.load_program(vertex_shader=":source:/shaders/hitbox_render_vert.glsl",
                                                      fragment_shader=":source:/shaders/hitbox_render_frag.glsl")

        self._render_program['frameSize'] = frame_data.size
        self._render_program['shift'] = frame_data.shift
        self._render_program['zoom'] = frame_data.zoom

        self._hitboxes: Set[HitboxData] = set()

    def _size(self):
        self._render_program['frameSize'] = self._frame_data.size

    def _shift(self):
        self._render_program['shift'] = self._frame_data.shift

    def _zoom(self):
        self._render_program['zoom'] = self._frame_data.zoom

    def add_hitbox(self, hitbox: HitboxData):
        self._hitboxes.add(hitbox)

    def remove_hitbox(self, hitbox: HitboxData):
        self._hitboxes.remove(hitbox)

    def draw(self):
        self._ctx.point_size = 4
        for hitbox in self._hitboxes:
            if hitbox.size > 0:
                self._render_program['colour'] = hitbox.color
                # self._render_program['spriteSize'] = hitbox.sprite_size
                hitbox.geometry.render(self._render_program, mode=gl.LINE_LOOP)
                hitbox.geometry.render(self._render_program, mode=gl.POINTS)
