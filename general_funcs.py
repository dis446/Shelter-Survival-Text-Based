"""General functions used by most modules in this project."""

from time import sleep


def print_line(*messages):
    """Replace print() with artificial line spacing.

    Arguments:
    *messages -- any number of arguments to print
    """
    for message in messages:
        for line in message.splitlines():
            sleep(0.5)  # Normal value used.
            # sleep(0.1) # Only used while game is in development.
            print(line)


