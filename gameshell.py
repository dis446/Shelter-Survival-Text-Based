from collections import OrderedDict
from time import sleep


class GameShell(object):
    """
    Handles text input and output, provides utility functions for displaying
    text to the player and handling player input - all player IO should be
    handled by this class
    """

    _speeds = OrderedDict((
            ('slow', 0.8),
            ('normal', 0.4),
            ('fast', 0.1),
        ))

    @property
    def speeds(self):
        """
        returns a list of valid options for speed
        """
        return list(self._speeds.keys())

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

        self.speed = 'normal'

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

    def print_line(self, *strings, sep='', end="\n", indent=0, speed=None):
        """
        Print strings with an artifical delay between each string

        Arguments:
        *strings -- strings to print
        sep    -- character to insert between strings
        end    -- character to insert at the end of the line
        indent -- indentation level
        speed  -- speed at which strings should be output, can be 'fast', 'slow',
                  'normal' or None. None will use self.speed, defaults to None
        """
        #special case for no lines so that it works the same way as print()
        if len(strings) == 0:
            strings = ['']

        indent_str = "    " * indent
        print(indent_str, end='')

        #if we're separating strings with newlines we need to add indentation
        #before each line
        if sep == '\n':
            sep += indent_str


        for i,string in enumerate(strings):
            #print the separator before every string except the first
            if i > 0:
                print(sep, end='', flush=True)
                self._sleep(speed)
            print(string, end='')

        #finally print end
        print(end, end='', flush=True)
        self._sleep(speed)



    def choose_from(self, text, choices):
        """
        Outputs a menu style selection and returns the user's selection

        Arguments:
        text    -- header text for the menu
        choices -- dictionary of {label: item, label:item} pairs. label is used to display
                   the choice to the user, item is what will be returned if
                   this option is selected

        Return:
        choice -- item part of member of 'choices' selected
        """

        self.print_line()
        self.print_line(text)
        self.print_line()
        
        for label,i in enumerate(choices.keys(),1):
            self.print_line("{}: {}".format(label, i))
            
        while True:
            choice = self.readline("Select a choice ({}-{}):".format(1,len(choices)))
            try:
                choice = int(choice) - 1
                #don't allow negative indices
                if choice < 0:
                    raise IndexError()
                return list(choices.keys())[choice]
                
            except (ValueError, IndexError):
                self.print_line("Invalid Choice")
                continue
            
            
    def confirmation_dialogue(self, text, default='n'):
        """
        Outputs a confirmation dialogue, validates the user input and
        returns a boolean representing the decision

        Arguments:
        text    -- confirmation text to output - should NOT include (y/n) or
                   similar as this is added automatically
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
        """
        Sets the speed of the shell

        Arguments:
        speed -- speed to set. Should be one of the options given by self.speeds
        """
        self.speed = speed


    def set_completer(self, complete):
        """
        Set completer function for readline if it is availible

        Arguments:
        complete -- completer function to set.
        """

        if self._has_readline:
            self._readline.set_completer(complete)

    def _init_readline(self):
        """
        Initialise the readline library
        """
        #TODO: specify histfile location using appdirs
        self._readline.parse_and_bind("tab: completion")


    def _sleep(self, speed=None):
        """
        sleep for a time determined by speed, if speed is not given use
        self.speed
        """

        if speed is None:
            speed = self.speed

        interval = self._speeds[speed.lower()]
        sleep(interval)
