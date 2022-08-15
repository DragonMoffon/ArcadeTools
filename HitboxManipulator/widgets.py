from typing import Iterable, Tuple

import arcade.gui as gui
from arcade.gui.widgets import UILayout, UIWidget, W


class UIStackLayout(UILayout):
    """
    Similar in function to a UIBoxLayout, but allows for children to be aligned to either end of the Layout.
    Depending on the vertical attribute, the Widgets are placed top to bottom or left to right.

    Hint: UIStackLayout does not adjust its own size if children are added.
    This requires a UIManager or UIAnchorLayout as parent.
    Use `self.fit_content()` to resize, bottom-left is used as anchor point.

    UIStackLayout supports: size_hint, size_hint_min

    :param float x: x coordinate of bottom left
    :param float y: y coordinate of bottom left
    :param vertical: Layout children vertical (True) or horizontal (False)
    :param align: Default alignment of children in orthogonal direction (x: left, center, right / y: top, center, bottom)
    :param children: Initial children, more can be added
    :param size_hint: A hint for :class:`UILayout`, if this :class:`UIWidget`
                    would like to grow (default 0,0 -> minimal size to contain children)
    :param size_hint_min: min width and height in pixel
    :param size_hint_max: max width and height in pixel
    :param space_between: Space between the children
    """

    def __init__(
        self,
        x=0,
        y=0,
        width=0,
        height=0,
        vertical=True,
        align="center",
        children: Iterable[UIWidget] = tuple(),
        size_hint=(0, 0),
        size_hint_min=None,
        size_hint_max=None,
        space_between=0,
        style=None,
        **kwargs
    ):
        self.align = align
        self.vertical = vertical
        self._space_between = space_between
        super().__init__(
            x=x,
            y=y,
            width=width,
            height=height,
            children=children,
            size_hint=size_hint,
            size_hint_min=size_hint_min,
            size_hint_max=size_hint_max,
            style=style,
            **kwargs
        )

        gui.bind(self, "_children", self._update_size_hints)

        # initially update size hints
        self._update_size_hints()

    def _update_size_hints(self):
        required_space_between = max(0, len(self.children) - 1) * self._space_between

        def min_size(child: UIWidget) -> Tuple[float, float]:
            mw, mh = child.size_hint_min or (None, None)
            return max(child.width, mw or 0), max(child.height, mh or 0)

        min_child_sizes = [min_size(child) for child in self.children]

        if len(self.children) == 0:
            width = 0
            height = 0
        elif self.vertical:
            width = max(size[0] for size in min_child_sizes)
            height_of_children = sum(size[1] for size in min_child_sizes)
            height = height_of_children + required_space_between
        else:
            width_of_children = sum(size[0] for size in min_child_sizes)
            width = width_of_children + required_space_between
            height = max(size[1] for size in min_child_sizes)

        base_width = self.padding_left + self.padding_right + 2 * self.border_width
        base_height = self.padding_top + self.padding_bottom + 2 * self.border_width
        self.size_hint_min = base_width + width, base_height + height

    def fit_content(self):
        """
        Resize to fit content, using `self.size_hint_min`

        :return: self
        """
        self.rect = self.rect.resize(*self.size_hint_min)
        return self

    def add(self, child: W, *, anchor="top", **kwargs):
        return super(UIStackLayout, self).add(child, anchor=anchor, **kwargs)

    def do_layout(self):
        start_y = self.content_rect.bottom
        start_x = self.content_rect.left

        if not self.children:
            return

        if self.vertical:
            available_width = self.width
            available_height = self.height

            end_y = start_y + available_height

            total_size_hint_height = sum(
                child.size_hint[1] or 0 for child in self.children if child.size_hint
            )

            for child, data in self._children:
                new_rect = child.rect

                # process size_hint_min
                if child.size_hint_min:
                    new_rect = new_rect.min_size(*child.size_hint_min)

                # apply size_hint
                if child.size_hint:
                    shw, shh = child.size_hint
                    if shw is not None:
                        new_rect = new_rect.resize(width=available_width * shw)

                    if shh:
                        # Maximal growth to parent.height * shh
                        available_growth_height = available_height * (
                                shh / total_size_hint_height
                        )
                        max_growth_height = self.height * shh
                        new_rect = new_rect.resize(
                            height=min(available_growth_height, max_growth_height)
                        )

                        total_size_hint_height -= shh

                # align
                if self.align == "left":
                    new_rect = new_rect.align_left(start_x)
                elif self.align == "right":
                    new_rect = new_rect.align_right(start_x + self.content_width)
                else:
                    center_x = start_x + self.content_width // 2
                    new_rect = new_rect.align_center_x(center_x)

                child_anchor = data.get("anchor", "top")
                if child_anchor == "top":
                    new_rect = new_rect.align_top(end_y)
                    end_y -= (new_rect.height + self._space_between)

                else:
                    new_rect = new_rect.align_bottom(start_y)
                    start_y += (new_rect.height + self._space_between)

                child.rect = new_rect
                available_height -= (new_rect.height + self._space_between)
        else:
            available_height = self.height
            available_width = self.width

            end_x = start_x + available_width

            total_size_hint_width = sum(
                child.size_hint[0] or 0 for child in self.children if child.size_hint
            )

            for child, data in self._children:
                new_rect = child.rect

                # process size_hint_min
                if child.size_hint_min:
                    new_rect = new_rect.min_size(*child.size_hint_min)

                # apply size_hint
                if child.size_hint:
                    shw, shh = child.size_hint
                    if shh is not None:
                        new_rect = new_rect.resize(height=available_height * shh)

                    if shw:
                        # Maximal growth to parent.width * shw
                        available_growth_width = new_rect.width + available_width * (
                                shw / total_size_hint_width
                        )
                        max_growth_height = self.width * shw
                        new_rect = new_rect.resize(
                            width=min(available_growth_width, max_growth_height)
                        )

                        total_size_hint_width -= shw

                # align
                if self.align == "top":
                    new_rect = new_rect.align_top(start_y + self.content_height)
                elif self.align == "bottom":
                    new_rect = new_rect.align_bottom(start_y)
                else:
                    center_y = start_y - self.content_height // 2
                    new_rect = new_rect.align_center_y(center_y)

                anchor = data.get("anchor", "left")
                if anchor == "left":
                    new_rect = new_rect.align_left(start_x)
                    start_x += (new_rect.width + self._space_between)
                else:
                    new_rect = new_rect.align_right(end_x)
                    end_x -= (new_rect.width + self._space_between)

                child.rect = new_rect
                available_width -= (new_rect.width + self._space_between)
