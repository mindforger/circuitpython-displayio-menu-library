import displayio
import terminalio
from adafruit_display_text.label import Label
from adafruit_display_shapes.rect import Rect
from adafruit_displayio_layout.layouts.grid_layout import GridLayout

class BasicEntry():
    def __init__(self):
        raise OSError("BasicEntry is not supposed to be instantiated")
    label_defaults = {
        "font": terminalio.FONT,
        "padding_left": 2,
        "padding_right": 2,
        "padding_top": -2,
        "padding_bottom": -1,
        "scale": 1,
        "x": 0,
        "y": 0,
    }

    @staticmethod
    def complementary_color(bg_color: int):
        fg_color = 0xFFFFFF
        if bg_color > 0xFFFFFF or bg_color < 0:
            raise OSError("invalid color")
        
        if ((bg_color>>8)&(0xFF)) > 0xD0 or (((bg_color)&(0xFF)) > 0x7F and ((bg_color>>16)&(0xFF)) > 0x7F):
            fg_color = 0
        return {"color": fg_color, "background_color": bg_color}

    @staticmethod
    def highlight(label, yes):
        if yes:
            label._background_palette.make_opaque(0)
            label.color = BasicEntry.complementary_color(label.background_color)["color"]
        else:
            label._background_palette.make_transparent(0)
            label.color = 0xFFFFFF

class MenuEntry(BasicEntry):

    def highlight(self, yes):
        BasicEntry.highlight(self.label, yes)
        
    def __init__(self, name, highlight_color=0xFFFFFF, **kwargs) -> None:
        self.name = name
        self.highlight_color = highlight_color
        label_properties = BasicEntry.label_defaults.copy()
        label_properties.update(kwargs)
        label_properties.update(BasicEntry.complementary_color(self.highlight_color))
        self.label = Label(text=self.name, **label_properties)
        self.highlight(False)

class MenuMultiEntry(BasicEntry):
    pass


class MenuLayout:

    class Orientation:
        VERTICAL = 0
        HORIZONTAL = 1
    
    @property
    def _scrolling(self):
        return len(self.menu_entries) > self.display_entries

    def _set_index(self, no):
        if self._scrolling:
            if no >= len(self.menu_entries):
                no = len(self.menu_entries)-1
            elif no < 0:
                no = 0
            offset = int(self.display_entries / 2 - 0.5)
            pos = (self.cell_space*(-no+offset))+1
            print("no:{} len:{} pos:{} off:{} self:{}".format(no, len(self.menu_entries), pos, offset, self.__dict__))
            if self.orientation == self.Orientation.VERTICAL:
                self.layout.y = pos
            elif self.orientation == self.Orientation.HORIZONTAL:
                self.layout.x = pos
    
    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, index):
        self.menu_entries[self._index].highlight(False)
        self._index = index
        self.menu_entries[self._index].highlight(True)
        self._set_index(self._index)

    def __init__(self, display, entries, display_entries=3, orientation=Orientation.VERTICAL, **kwargs):
        self.display = display
        self.orientation = orientation
        self.group = displayio.Group()
        self.menu_entries = []
        self.display_entries = display_entries
        self._index = 0
        self._i_offset = 0
        if len(entries) < display_entries:
            self._i_offset = display_entries - len(entries)
        for me in entries:
            self.add_label(me)
        space = w = h = x_off = y_off = 0
        c = l = 1
        if self.orientation == self.Orientation.VERTICAL:
            w = display.width
            l = len(self.menu_entries)
            space = display.height / self.display_entries
            h = space * l
            y_off = int(space*self._i_offset/2 - 0.5)
#            y = int((self.display.height/2)-(space*len(self.menu_entries)/2))
        elif self.orientation == self.Orientation.HORIZONTAL:
            h = self.display.height
            c = len(self.menu_entries)
            space = display.width / self.display_entries
            w = space * c
            x_off = int(space*self._i_offset/2 - 0.5)
#            x = int((self.display.width/2)-(self.cell_space*len(self.menu_entries)/2))
        self.cell_space = int(space)
        print("cs:{} w:{} h:{} c:{}, l:{}".format(self.cell_space,w,h,c,l))
        self.layout = GridLayout(
            x=x_off,
            y=y_off,
            width=w,
            height=h,
            grid_size=(c, l),
            cell_padding=0,
            divider_lines=False,
            cell_anchor_point=(0.5, 0.5)
        )
        self.labels = []
        for i in range (0,len(self.menu_entries)):
            x = y = 0
            if self.orientation == self.Orientation.VERTICAL:
                y = i
            elif self.orientation == self.Orientation.HORIZONTAL:
                x = i
            self.layout.add_content(self.menu_entries[i].label, grid_position=(x, y), cell_size=(1, 1))
        self.group.append(self.layout)

    def add_label(self, menu_entry, **kwargs):
        self.menu_entries.append(menu_entry)

    def show(self):
        self.display.show(self.group)

