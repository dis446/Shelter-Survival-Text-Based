"""Module containing NPC class."""

from Fallout_Shelter import print_line
from Human import Human


class NPC(Human):
    """NPC class, inherits Human attributes."""

    def __init__(self, first_name, day_of_birth,
                 parent_1, parent_2, age, gender):
        """NPC class constructor.

        Arguments:
        first_name -- first name of NPC
        day_of_birth -- day NPC was born on
        parent_1 -- name of father
        parent_2 -- name of mother
        age -- age of NPC
        gender -- gender of NPC
        """
        Human.___init__(
            self, first_name, day_of_birth,
            parent_1, parent_2, age, gender)
        self.scavenging = False
        self.days_scavenging = 0
        self.days_to_scavenge_for = 0

    def die(self):
        """Kill NPC."""
        global people
        global rooms
        print_line(self.name, " has died")
        if self.assigned_room != "":
            for x in range(people):  # Fetches the index of the person.
                if people[x].name == self.name:
                    index = x
                    break
            for r in rooms:
                # Removes person from the rooms' assigned records.
                del r.assigned[index]
        people.remove(self)
