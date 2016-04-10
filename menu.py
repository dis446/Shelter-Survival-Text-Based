"""Menu screens for use with GameShell"""

class Menu(object):

    def __init__(self, name):
        self.name = name
        self.menu_items = []


    def __str__(self):
        return self.name

    def add_menu_item(self, item):
        self.menu_items.append(item)

    def __call__(self, shell, stack):
        choice = shell.choose_from(self.name, self.menu_items)
        stack.push(self)
        return choice

class MenuItem(object):
    def __init__(self, name, fn):
        self.name = name
        self.fn = fn

    def __str__(self):
        return self.name

    def __call__(self, *args):
        return self.fn(*args)

#decorator
def menu_item(name):
    def bind(fn):
        return MenuItem(name, fn)
    return bind

@menu_item("Change Speed")
def speed_change(shell, stack):
    speed = shell.choose_from("Change Speed", shell.speeds)
    shell.set_speed(speed)
    return None

@menu_item("New Game")
def new_game(shell, stack):
    shell.print_line("New Game not implemented")
    return None

@menu_item("Load Game")
def load_game(shell, stack):
    shell.print_line("Load Game not implemented")
    return None

def back(shell, stack):
    stack.pop()
    return None

settings_menu = Menu("Settings")
settings_menu.add_menu_item(speed_change)
settings_menu.add_menu_item(MenuItem("Back", back))

main_menu = Menu('Main Menu')
main_menu.add_menu_item(new_game)
main_menu.add_menu_item(load_game)
main_menu.add_menu_item(settings_menu)
main_menu.add_menu_item(MenuItem("Exit", back))
