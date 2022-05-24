from menu import Menu, scan_input, menulayout
import mydisplay
stopped = False

class MainMenu(Menu):

    entries = [
        menulayout.MenuEntry("2022", 0xFFFFFF,scale=2),
        menulayout.MenuEntry("05", 0xFF0000, scale=2),
        menulayout.MenuEntry("22", 0x00FF00,scale=2),
#        menulayout.MenuEntry("D", 0x0000FF),
#        menulayout.MenuEntry("E", 0xFFFF00),
#        menulayout.MenuEntry("F", 0x7FD000),
#        menulayout.MenuEntry("G", 0x00FFFF),
    ]
    
    def up(self):
        print("up")
        self.selected_index -= 1
    
    def down(self):
        print("down")
        self.selected_index += 1
    
    actions = {
        Menu.Inputs.up: up,
        Menu.Inputs.down: down
    }
    
    def default_action(self, inp):
        print("unknown input {}".format(inp))
    
    def __init__(self, target):
        cells = 3
        orientation = menulayout.MenuLayout.Orientation.HORIZONTAL
        super().__init__(target, "main", MainMenu.entries, actions=MainMenu.actions, default_action=self.default_action, orientation=orientation, display_entries=cells)

def run():
    inp = None
    column = 0
    main_menu = MainMenu(mydisplay.display)
    main_menu.show_menu()
    while not stopped:
        inp = scan_input()
        if inp is not None:
            main_menu.update(inp)

run()