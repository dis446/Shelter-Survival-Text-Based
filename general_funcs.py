"""General functions used by most modules in this project."""

from time import sleep
from sys import stdout

load = False  # Enables/disables loading screens.
if load:
    from tqdm import tqdm


def input_int(s):
    """Allow user to input integers while catching errors.

    Arguments:
    s -- string to print as a prompt

    Returns:
    x -- integer inputted by user
    """
    while True:
        try:
            x = int(input(s))
            break
        except:
            print_line("Invalid. Only integer numbers are accepted!")
    return x


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


def print_line(*messages, end="\n", fast=False):
    """Print message with artificial spacing by sleeping.

    Arguments:
    *messages -- tuple of strings to print
    end -- end of string
    fast -- if true, shortens time between prints
    """
    for message in messages:
        for line in message.splitlines():
            if fast:
                sleep(0.1)
            else:
                sleep(0.5)
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
    if load:
        print_line(str(message))
        for x in tqdm(range(0, x)):
            sleep(0.01)
    else:
        for message in messages:
            print_line(message)
        sleep(x / 10000)


def count_item(item, target_inventory):
    """Count total number of specified item in inventory.

    Arguments:
    item -- item to count
    target_inventory -- inventory to count in

    Returns:
    int -- count of item in inventory
    """
    item = str(item)
    if target_inventory == "player":
        return inventory.count(item)
    elif target_inventory == "trader":
        return trader_inventory.count(item)
    else:
        print_line("Bug with item counting system. Please contact dev!")
