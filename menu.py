from binascii import hexlify
import usb_cdc
import menulayout


def scan_input():
    if usb_cdc.console.in_waiting > 0:
        return usb_cdc.console.read(usb_cdc.console.in_waiting)


class Menu(menulayout.MenuEntry):
    class Inputs():
        up = b'\x1b[A'
        down = b'\x1b[B'
        left = b'\x1b[D'
        right = b'\x1b[C'
        esc = b'\x1b'
        F1 =  b'\x1b[11~'
        F2 =  b'\x1b[12~'
        F3 =  b'\x1b[13~'
        F4 =  b'\x1b[14~'
        F5 =  b'\x1b[15~'
        F6 =  b'\x1b[17~'
        F7 =  b'\x1b[18~'
        F8 =  b'\x1b[19~'
        F9 =  b'\x1b[20~'
        F10 =  b'\x1b[21~'
        F11 =  b'\x1b[23~'
        F12 =  b'\x1b[24~'
        backspace =  b'\x7f'
        delete = b'\x1b[3~'

    @property
    def selected_index(self):
        return self.menu_layout.index

    @selected_index.setter
    def selected_index(self, index):
        if index >= len(self.menu_entries):
            self.menu_layout.index = len(self.menu_entries)-1
        elif index < 0:
            self.menu_layout.index = 0
        else:
            self.menu_layout.index = index
    
    def update(self, inp):
#        print("input: ({}) {} {}".format(len(inp), inp, hexlify(inp)))
        if inp in self.actions:
            self.actions[inp](self)
        elif self.default_action is not None:
            self.default_action(inp)

    def show_menu(self):
        self.menu_layout.show()

    def __init__(self, target, name, entries, actions={}, default_action=None, highlight_color=0xFFFFFF, **kwargs):
        super().__init__(name, highlight_color)
        self.actions = actions
        self.default_action = default_action
        self.menu_entries = []
        for i in range(0, len(entries)):
            self.menu_entries.append((i, entries[i]))
        self.menu_layout = menulayout.MenuLayout(target, entries=entries, **kwargs)
        self.selected_index = 0
