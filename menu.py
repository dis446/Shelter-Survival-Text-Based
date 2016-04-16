"""Menu screens for use with GameShell"""
from collections import OrderedDict

class Menu(object):

    def __init__(self, name):
        self.name = name
        self.menu_items = OrderedDict()


    def __str__(self):
        return self.name

    def add_menu_item(self, label, item):
        self.menu_items[label] = item

    def __call__(self, shell, stack):
        choice = shell.choose_from(self.name, self.menu_items.items())
        stack.push(self)
        return choice

def speed_change(shell, stack):
    speed = shell.choose_from("Change Speed", zip(shell.speeds, shell.speeds))
    shell.set_speed(speed)
    return None

def new_game(shell, stack):
    shell.print_line("New Game not implemented")
    return None

def load_game(shell, stack):
    shell.print_line("Load Game not implemented")
    return None

def back(shell, stack):
    """
    Moves back a screen
    """
    stack.pop()
    return None

settings_menu = Menu("Settings")
settings_menu.add_menu_item("Change Speed", speed_change)
settings_menu.add_menu_item("Back", back)

main_menu = Menu('Main Menu')
main_menu.add_menu_item("New Game", new_game)
main_menu.add_menu_item("Load Game", load_game)
main_menu.add_menu_item(settings_menu.name, settings_menu)
main_menu.add_menu_item("Exit", back)
