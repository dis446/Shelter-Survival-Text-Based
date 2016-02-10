"""General functions used by most modules in this project."""

from time import sleep

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


def print_line(*messages):
    """Replace print() with artificial line spacing.

    Arguments:
    *messages -- any number of arguments to print
    """
    for message in messages:
        message=str(message)
        for line in message.splitlines():
            #sleep(0.5)  # Normal value used.
            sleep(0.1) # Only used while game is in development.
            print(line)


def load_time(x, message):
    """Loading bars.

    Arguments:
    x -- length of loading bar in seconds
    message -- message to print before loading bar
    """
    if load:
        print_line(str(message))
        for x in tqdm(range(0, x)):
            sleep(0.01)
    else:
        print(str(message))
        sleep(x / 10000)


