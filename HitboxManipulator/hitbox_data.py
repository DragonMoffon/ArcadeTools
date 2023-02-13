from typing import Tuple
from array import array

import numpy as np
from numpy import float32, frombuffer, insert as np_insert, array as np_array, zeros as np_zeros

from arcade.gui import UIWidget, bind, Property
from arcade import get_window, Texture
from arcade.gl import BufferDescription


class FrameData:

    frame_pos: Tuple[int, int] = Property((0, 0))
    frame_size: Tuple[int, int] = Property((1, 1))
    frame_zoom: float = Property(1.0)
    frame_shift: Tuple[float, float] = Property((0.0, 0.0))

    def __init__(self, parent_widget: UIWidget, zoom: float, shift: Tuple[float, float]):
        self._parent: UIWidget = parent_widget

        self.frame_size = (1, 1)
        self.frame_pos = (0, 0)
        self.update_rect()
        bind(parent_widget, "rect", self.update_rect)

        self.frame_zoom = zoom or 1
        self.frame_shift = shift

    def update_rect(self):
        size = self._parent.size
        pos = self._parent.position

        self.size = int(size[0]-2), int(size[1]-2)
        self.pos = int(pos[0]+1), int(pos[1]+1)

    @property
    def size(self):
        return self.frame_size

    @size.setter
    def size(self, value):
        self.frame_size = value

    @property
    def pos(self):
        return self.frame_pos

    @pos.setter
    def pos(self, value):
        self.frame_pos = value

    @property
    def zoom(self):
        return self.frame_zoom

    @zoom.setter
    def zoom(self, value):
        self.frame_zoom = value

    @property
    def shift(self):
        return self.frame_shift

    @shift.setter
    def shift(self, value):
        self.frame_shift = value

    @property
    def x(self):
        return self.frame_pos[0]

    @property
    def y(self):
        return self.frame_pos[1]


class HitboxData:

    def __init__(self, sprite_data: Texture, color: Tuple[float, float, float] = (1.0, 1.0, 1.0), _count: int = 256):
        _ctx = get_window().ctx

        # per point there are 28 bytes. This is to have the position and indies to draw
        self._points_GPU = _ctx.buffer(reserve=_count * 4 * 2, usage='dynamic')  # 2 32-bit floats for 8 bytes per point
        self._points_CPU = np_zeros([_count, 2], dtype=float32)
        self._point_indices = _ctx.buffer(reserve=_count * 4, usage='dynamic')  # 1 32-bit int for 4 bytes per point

        self._point_count = 0
        self._insert_point = -1
        self._max_count = _count

        _point_descriptions = [BufferDescription(self._points_GPU, "2f", ['pos'])]
        self._point_geometry = _ctx.geometry(_point_descriptions,
                                             self._point_indices, 4)

        self._color = color
        self._sprite_size = sprite_data.size

        if sprite_data.hit_box_points is not None and len(sprite_data.hit_box_points) <= _count:
            for point in sprite_data.hit_box_points:
                self.add_point((point[0], point[1]))

    @property
    def size(self):
        return self._point_count

    @property
    def points(self):
        """
        WARNING EXPENSIVE OPERATION
        """
        print("WARNING EXPENSIVE OPERATION")
        return frombuffer(self._points_GPU.read(4 * 2 * self._point_count), dtype=float32)

    @property
    def sprite_size(self):
        return self._sprite_size

    @property
    def color(self):
        return self._color

    @property
    def red(self):
        return self._color[0]

    @property
    def green(self):
        return self._color[1]

    @property
    def blue(self):
        return self._color[2]

    def change_insert_point(self, new_index):
        if new_index <= self._point_count:
            self._insert_point = new_index
        else:
            print("Attempting to insert to an index outside the hitbox")

    def reset_insert_point(self):
        self._insert_point = -1

    def add_point(self, point):
        if self._point_count < self._max_count:
            # If the insert point is at the end there is no reason to read from the buffer.
            if self._insert_point == -1 or self._point_count - self._insert_point == 0:
                self._points_GPU.write(np_array(point, dtype=float32), self._point_count * 8)
            else:
                # we read all values after the insert point and then and the insert point to the start of the array.
                # This new array is then rewritten to the gpu.
                shift_data = np_insert(frombuffer(self._points_GPU.read((self._point_count - self._insert_point) * 8,
                                                                        self._insert_point * 8), dtype=float32),
                                       0, np_array(point, dtype=float32))

                self._points_GPU.write(shift_data, self._insert_point * 8)

            self._point_indices.write(array('i', (self._point_count,)), self._point_count * 4)
            self._point_count += 1
        else:
            print("ERROR: Max Size Reached")

    @property
    def geometry(self):
        return self._point_geometry
