"""General functions used by most modules in this project."""

from string import ascii_uppercase
from time import sleep
from sys import stdout

load = False  # Enables/disables loading screens.
if load:
    from tqdm import tqdm


def input_int(message):
    """Allow user to input integers while catching errors.

    Arguments:
    message -- string to print as a prompt

    Returns:
    inp -- integer inputted by user
    """
    while True:
        inp = input(str(message))
        try:
            return int(inp)
        except:
            print_line("Invalid. Only integer numbers are accepted!")


def default_input(text):
    """Ask for input and accept a default answer.

    Example `text`: "Answer? (Y/n) " where `Y` is default answer.

    Arguments:
    text -- text as prompt

    Returns:
    char/None -- answer
    """
    answers = []
    default = ""
    in_ans = False
    for c in text[len(text):0:-1]:
        if in_ans:
            if c == "(":
                in_ans = False
                break
            answers += c.lower()
            if c in ascii_uppercase:
                default = answers[-1]
        if c == ")":
            in_ans = True
    answer = input(text).lower()
    if len(answer) == 0:
        return default
    elif answer in answers:
        return answer
    return None


def validate_input(text):
        """Check if input is valid ( i.e has enougth length).

        Arguments:
        text -- string to be checked

        Returns:
        bool -- Whether input is acceptable
        """
        if len(text) > 0:
                return True
        return False


def validate_name(name):
    """Check if name is valid ( Has to be one word only).

    Arguments:
    name -- name to be checked

    Returns:
    bool -- Whether name is acceptable or not
    """
    if validate_input(name) and len(name.split()) == 1:
        return True
    return False


def text_align(starts):
    """Align starts and ends so the beginning of end strings line up.

    Arguments:
    starts -- list of strings to begin

    Returns:
    align -- list of differences of max string length and each string length
    """
    lens = [len(s) for s in starts]
    align = [max(lens) - l for l in lens]
    return align


def sentence_split(text):
    """Split text by sentences and return first sentence.

    Arguments:
    text -- text to split

    Returns:
    sen -- first sentence
    """
    sens = text.split(".")
    sen = sens[0] + "."
    return sen

SLOW = 0.8
FAST = 0.1
NORMAL = 0.4

def print_line(*messages, end = "\n", speed = SLOW):
    """Print message with artificial spacing by sleeping.

    Arguments:
    *messages -- tuple of strings to print
    end -- end of string
    fast -- if true, shortens time between prints
    slow -- if true, extends time between prints
    """
    if len(messages) == 2:
        output = ' '.join([str(messages[0]), str(messages[1])])
        messages = (output,)
    for message in messages:
        message = str(message)
        for line in message.splitlines():
            sleep(speed)
            if end != "\n":
                stdout.write(line)
                stdout.flush()
            else:
                print(line)


def load_time(x, *messages):
    """Loading bars.

    Arguments:
    x -- length of loading bar in seconds
    messages -- tuple of message to print before loading bar
    """
    print_line(*messages)
    if load:
        for x in tqdm(range(0, x)):
            sleep(0.01)
    else:
        sleep(x / 10000)

