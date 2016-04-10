from collections import OrderedDict
from time import sleep


class GameShell(object):
    """
    Handles text input and out, implements a basic Finite State Machine with
    a stack for handling different game screens in the 'run' method. Also
    provides utility functions for displaying text to the player and handling
    player input - all player IO should be handled by this class
    """

    def __init__(self):
        try:
            try:
                import readline
            except ImportError:
                import pyreadline as readline

            self._has_readline = True
            self._readline = readline
            self._init_readline()

        #can't get any readline library, default to standard IO
        except ImportError:
            pass

        self.current_screen = None
        self.speed = 'normal'
        self.screen_stack = []

    def readline(self, prompt):
        """
        Print prompt to stdout, read a line of user imput from stdin and
        return it as a string

        Arguments:
        prompt -- propmpt to output

        Returns:
        string -- line read
        """

        return input(prompt)

    def print_line(self, *lines, end="\n", indent=0, speed=None):
        """
        Print lines with indentation indent and an artifical delay between
        each line governed by speed

        Arguments:
        *lines -- lines to print
        end    -- character to insert betwween lines
        indent -- indentation level
        speed  -- speed at which lines should be output, can be 'fast', 'slow',
                  'normal' or None. None will use self.speed, defaults to None
        """
        #special case for no lines
        if len(lines) == 0:
            print(end=end, flush=True)
            return

        indent_str = "    " * indent
        for line in lines:
            print(indent_str + str(line), end=end, flush=True)
            self._sleep(speed)

    def run(self, screen):
        """
        Runs the shell starting from screen

        Arguments:
        screen -- screen to start from, screens should be callables that return
                  take the GameShell as an argument and return the next screen to be
                  displayed or None. Returning None will run the screen at the
                  top of the screen stack or exit if the screen stack is empty
        """
        while True:
            if screen is None:
                try:
                    screen = self.pop()
                except IndexError:
                    break
            self.current_screen = screen
            if hasattr(screen, 'complete'):
                self.set_completer(screen.complete())
            try:
                screen = screen(self)
            except EOFError:
                #if we recieve EOF we take this as a sign we want to move back a
                #screen
                self.print_line()
                screen = None

    def push(self, screen=None):
        """
        Pushes screen onto the screen stack

        Arguments:
        screen -- screen to push or None. If none it will push the current
                  screen onto the stack
        """
        if screen is None:
            screen = self.current_screen
        self.screen_stack.append(screen)

    def pop(self):
        """
        Pop a screen from the screen stack and return it. Throws IndexError
        if the stack is empty

        Returns:
        screen -- the screen from the top of the stack.
        """
        return self.screen_stack.pop()

    def choose_from(self, text, choices):
        """
        Outputs a menu style selection for choices headed by text and
        returns the user's selection

        Arguments:
        text -- header text for the menu
        choices -- iterable of choice. to handle the case where choices are
                   more complex objects than simple strings, choices will be
                   displayed as the 'str' representation of each choice and the
                   actual object selected will be returned

        Return:
        choice -- Member of 'choices' selected
        """

        self.print_line()
        self.print_line(text)
        for i, choice in enumerate(choices, start=1):
            self.print_line("{:d}) {!s}".format(i, choice), indent=1)

        self.print_line()
        while True:
            choice = self.readline("Select a choice ({}-{}):".format(1,len(choices)))
            try:
                choice = int(choice) - 1
                #don't allow negative indices
                if choice < 0:
                    raise IndexError()
                return choices[choice]
            except (ValueError, IndexError):
                self.print_line("Invalid Choice")
                continue

    def confirmation_dialogue(self, text, default='n'):
        """
        Outputs a confirmation dialogue, validates the user input and
        returns a boolean representing the decision

        Arguments:
        text -- confirmation text to output - should NOT include (y/n) or
                similar as this will be added for you
        default -- default option if the user inputs no choice, should be
                   either 'y' or 'n'. Defaults to 'n'

        Returns:
        bool -- True if the user selects 'yes', False for 'no'
        """

        default = default.lower()
        if default not in ('y', 'n'):
            raise TypeError("default argument of confirmation_dialogue should"
                             "be either 'y' or 'n', {} given".format(default))

        yes = 'y'
        no  = 'n'
        if default == 'y':
            yes = yes.upper()
        else:
            no = no.upper()

        while True:
            s = self.readline("{} ({}/{}): ".format(text, yes, no))
            s = s.strip().lower()
            if len(s) == 0:
                return default == 'y'
            if s not in ('y', 'yes', 'n', 'no'):
                self.print_line("Invalid Choice")
                continue

            return s in ('y', 'yes')

    def set_speed(self, speed):
        self.speed = speed


    def set_completer(self, complete):
        if self._has_readline:
            self._readline.set_completer(complete)

    def _init_readline(self):
        self._readline.parse_and_bind("tab: completion")

    intervals = OrderedDict((
            ('slow', 0.8),
            ('normal', 0.4),
            ('fast', 0.1),
        ))

    def _sleep(self, speed=None):
        """
        sleep for a time determined by speed, if speed is not given use
        self.speed
        """

        if speed is None:
            speed = self.speed

        interval = self.intervals[speed]
        sleep(interval)

if __name__ == "__main__":
    from menu import main_menu
    shell = GameShell()
    shell.run(main_menu)
