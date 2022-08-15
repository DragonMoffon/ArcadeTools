import arcade.gui as gui

import widgets as gui_c
from toolWindow import HitboxFrame


import style

"""
ALL of the primary GUI used by the tool. Setup as a series of classes to split up functionality
Tree:
# BaseSlots
    # Navigation Bar
        # File
        # Edit
        # Tools
        # Help
    # Primary Tab
        # Hit Box Info Line
            # Current Hit Box Info
            # Hit Box Selector
        # Hit Box Line
            # Hit Box Frame Renderer
            # Hit Box Editor Tool Line
                # Hit Box Editor Tools
        # Sprite Picker Line
            # Sprites
    # Bottom Tab ( Filler )
"""


class NavigationBar(gui.UISpace):

    def __init__(self):
        super().__init__(size_hint=(1.0, 0.0), height=50)


class HitboxInfoLine(gui_c.UIStackLayout):

    def __init__(self):
        super().__init__(size_hint=(0.2, 1.0))

        # The Hit Box Info Line (The vertical line which holds the details about the current hit box)

        self._hitbox_info_data = gui.UISpace(size_hint=(0.8, 0.6),
                                             color=style.COLOURS['-background-secondary'])
        self._hitbox_info_data.border_width = 1
        self._hitbox_info_data.border_color = style.COLOURS['-background-border']
        self._hitbox_info_selector = gui.UISpace(size_hint=(0.8, 0.4),
                                                 color=style.COLOURS['-background-secondary'])
        self._hitbox_info_selector.border_width = 1
        self._hitbox_info_selector.border_color = style.COLOURS['-background-border']

        self.add(self._hitbox_info_data, anchor="top")
        self.add(self._hitbox_info_selector, anchor="top")


class HitboxTools(gui_c.UIStackLayout):

    def __init__(self):
        super().__init__(size_hint=(1.0, 0.0), height=40, space_between=10, vertical=False, align="bottom")
        # Hit box tools (the tools and buttons to change settings about how the hit box editor works)

        self._tools = [gui.UISpace(width=30, height=30, color=style.COLOURS['-background-secondary']) for _ in range(6)]
        for tool in self._tools:
            tool.border_width = 1
            tool.border_color = style.COLOURS['-background-border']
            self.add(tool, anchor="left")

        self._mode = gui.UISpace(width=120, height=30, color=style.COLOURS['-background-secondary'])
        self._mode.border_width = 1
        self._mode.border_color = style.COLOURS['-background-border']
        self.add(self._mode, anchor="right")


class HitboxLine(gui_c.UIStackLayout):

    def __init__(self):
        super().__init__(size_hint=(0.6, 1.0))
        # Hit Box line (the vertical line which holds the hit box editor frame)
        self._hitbox_frame = gui.UISpace(size_hint=(1.0, 1.0), color=style.COLOURS['-background-border'])
        self._hitbox_tools = HitboxTools()

        self.add(self._hitbox_tools, anchor="bottom")
        self.add(self._hitbox_frame, anchor="top")

        self._hitbox_renderer = HitboxFrame(self._hitbox_frame)


class SpritePickerLine(gui_c.UIStackLayout):

    def __init__(self):
        super().__init__(size_hint=(0.2, 1.0))
        # Sprite Picker Line (The vertical line which holds the list of current working sprites)
        self._sprite_picker = gui.UISpace(size_hint=(0.8, 1.0), color=style.COLOURS['-background-secondary'])
        self._sprite_picker.border_width = 1
        self._sprite_picker.border_color = style.COLOURS['-background-border']

        self.add(self._sprite_picker, anchor="top")


class PrimaryTab(gui.UIBoxLayout):

    def __init__(self):
        self._hitbox_info_line = HitboxInfoLine()
        self._hitbox_line = HitboxLine()
        self._sprite_picker_line = SpritePickerLine()
        super().__init__(size_hint=(1.0, 1.0), vertical=False,
                         children=[self._hitbox_info_line, self._hitbox_line, self._sprite_picker_line])


class BottomTab(gui.UISpace):

    def __init__(self):
        super().__init__(size_hint=(1.0, 0.0), height=50)


class BaseSlots(gui_c.UIStackLayout):

    def __init__(self):
        super().__init__(size_hint=(1.0, 1.0))
        # Navigation gui
        self._navigation_bar_tab = NavigationBar()

        # Primary tab gui
        self._primary_tab = PrimaryTab()

        # Bottom Padding (simply for filling in the space)
        self._bottom_tab = BottomTab()

        self.add(self._bottom_tab, anchor="bottom")
        self.add(self._navigation_bar_tab, anchor="top")
        self.add(self._primary_tab, anchor="top")


class GUIManager(gui.UIManager):

    def __init__(self, window):
        super().__init__(window)
        self._base_slots = BaseSlots()
        self.add(self._base_slots)

