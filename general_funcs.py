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


def print_line(*messages, fast=True):
    """Replace print() with artificial line spacing.

    Arguments:
    *messages -- any number of arguments to print
    """
    for message in messages:
        message = str(message)
        for line in message.splitlines():
            if fast:
                sleep(0.1)  # Only used while game is in development.
            else:
                sleep(0.5)  # Normal value used.
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
