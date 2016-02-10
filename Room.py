"""Module containing Room class."""

from general_funcs import print_line


class Room(object):  # Basic class for the rooms in the game.
    """Room class."""

    def __init__(self, name, player):
        """Room class constructor.

        Arguments:
        name -- name of room
        player -- ???
        """
        self.name = name
        self.assigned = ''  # should be a list

        # Determines the production level, max assigned limit etc.
        self.level = 1
        self.risk = False  # Risk of breaking down, when rushed.
        self.broken = False
        # 'On' if there is enough power for the room, 'Off' otherwise.
        self.power_available = "On"
        # Living rooms have no "assigned". Number of living rooms just limits
        # the total population of the shelter.
        if self.name == "living":
            # Stores whether or not room actually produces anything.
            # self.components=["wood",] #Need to add components.
            self.can_produce = False
            self.assigned_limit = 0
            self.components = ["wood", "wood", "wood", "wood"]
            self.power_usage = 5
        elif self.name == "generator":
            self.risk = 2
            self.can_produce = True
            self.components = ["steel", "steel", "steel", "steel"]
            # Max number of workers that can work in the room at one time.
            self.assigned_limit = 3
            self.power_usage = 0
        elif self.name == "storage":
            self.can_produce = False
            self.assigned_limit = 0
            self.components = ["steel", "steel"]
            self.power_usage = 1
        elif self.name == "kitchen":
            self.risk = 1
            self.can_produce = True
            self.assigned_limit = 3
            self.components = ["wood", "wood", "wood"]
            self.power_usage = 10
        elif self.name == "trader":
            self.can_produce = False
            self.assigned_limit = 1
            self.components = ["wood", "wood", "steel", "steel", "wood"]
            self.power_usage = 2
        elif self.name == "water works":
            self.risk = 2
            self.can_produce = True
            self.assigned_limit = 3
            self.components = ["wood", "wood", "steel"]
            self.power_usage = 10
        elif self.name == "radio":
            self.can_produce = False
            self.assigned_limit = 2
            self.components = ["wood", "wood", "steel", "steel", "wood"]
            self.power_usage = 15
        # Need to add more names.
        else:
            print_line(
                "Bug with room creation system.",
                "Please contact dev. Class specific bug.")
        if self.can_produce:
            self.production = 0
            self.can_rush = True
            self.rushed = False
        else:
            self.can_rush = False

    def __str__(self):
        """String representation of object.

        Returns:
        self.name -- eg. "Living Room"
        """
        return "{}{} Room".format(self.name[0].upper(), self.name[1:])

    def rush(self):
        """Rush building of Room."""
        global rooms
        self.rushed = 1  # Lets game know this room has been rushed.
        self.risk += 5
        print_line(self.name, " has been rushed!")

    def fix(self):
        """Repair room if damaged."""
        global rooms

    def update_production(self, player):
        """Calculate production value of Room.

        Arguments:
        player -- player object
        """
        if self.broken:
            production = 0
            print_line(self.name, "is broken and needs to be fixed.")
        else:
            production = 0
            if self.name == "generator":
                for person_index in str(self.assigned):
                    if person_index == '1':
                        production += people[int(person_index)].strength * 10
                if player.electrician > 0:
                    production = production * (1 + (player.electrician * 0.05))
            elif self.name == "kitchen":
                for person_index in str(self.assigned):
                    if person_index == '1':
                        production += people[int(person_index)].intelligence \
                                    * 10
                if player.cooking > 0:
                    production = production * \
                        (1 + (player.cooking * 0.05))

            elif self.name == "water works":
                for person_index in str(self.assigned):
                    if person_index == '1':
                        production += people[int(person_index)].perception * 10
                if player.cooking > 0:
                    production = production * \
                        (1 + (player.cooking * 0.05))
            elif self.name == "radio":
                for person_index in str(self.assigned):
                    if person_index == '1':
                        production += people[int(person_index)].charisma * 10
                if player.inspiration > 0:
                    production = production * \
                        (1 + (player.inspiration * 0.05))
            else:
                print_line(
                    "Bug with room production update system.",
                    "Please contact dev.")
            if player.inspiration > 0:
                production = production * \
                    (1 + (player.inspiration * 0.03))
            if self.can_rush and self.rushed:
                production = production * 2
            return production

    def count_assigned(self):
        """Count inhabitants assigned to Room."""
        count = 0
        for x in str(self.assigned):
            if x == '1':
                count += 1
        return count

    def see_assigned(self):
        """Print names of inhabitants assigned to Room."""
        count = 0
        for x in str(self.assigned):
            if x == '1':
                person = people[count]
                print_line("      ", person.name, person.surname)
            count += 1

    def count_component(self, component):
        """Count components required to build Room.

        Arguments:
        component -- component to count

        Returns:
        int -- amount of component required to build Room
        """
        return self.components.count(str(component))



    def use_power(self):
        """Consume player's power."""
        for x in range(0, self.power_usage):
            Item('watt').destroy("player")


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
