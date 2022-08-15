import arcade.gui as gui
import widgets as gui_c

import style


class UIGroup(gui.UIManager):

    def __init__(self, window):
        super().__init__(window)

        # Base Slots (The three primary slices of the UI)
        self._base_slots = gui_c.UIStackLayout(size_hint=(1.0, 1.0))
        self.add(self._base_slots)

        # Navigation gui
        self._navigation_bar_tab = gui.UISpace(size_hint=(1.0, 0.0), height=50)

        # Primary tab gui
        self._primary_tab = gui.UIBoxLayout(size_hint=(1.0, 1.0), vertical=False)

        # Bottom Padding (simply for filling in the space)
        self._bottom_tab = gui.UISpace(size_hint=(1.0, 0.0), height=50)

        self._base_slots.add(self._bottom_tab, anchor="bottom")
        self._base_slots.add(self._navigation_bar_tab, anchor="top")
        self._base_slots.add(self._primary_tab, anchor="top")

