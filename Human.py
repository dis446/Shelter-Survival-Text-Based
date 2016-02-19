"""Module containing all Human classes."""

from general_funcs import print_line


class Human(object):
    """Basic class for all humans in game."""

    def __init__(
            self, first_name=None, day_of_birth=0,
            parent_1=None, parent_2=None, age=0, gender='M', surname=None):
        """Constructor for Human class.

        Arguments:
        first_name -- first name of Human
        day_of_birth -- day Human was born
        parent_1 -- name of Human's father
        parent_2 -- name of Human's mother
        age -- age of Human
        gender -- gender of Human
        """
        self.alive = True
        self.name = first_name  # First name
        self.day_of_birth = day_of_birth
        self.parent_1 = parent_1  # Surname
        self.parent_2 = parent_2  # Surname
        self.age = age
        self.gender = gender
        self.hunger = 0
        self.thirst = 0
        try:
            self.surname = self.parent_1.surname
        except:
            self.surname = surname
        self.partner = ""

        # The stats of the person. Affects the production of
        # room the person has been assigned to.
        self.strength = 1
        self.perception = 1
        self.endurance = 1
        self.charisma = 1
        self.intelligence = 1
        self.luck = 1

        self.assigned_room = ""  # Keeps track of where person is working.
        self.children = []  # List of all children
        self.partner = ""
        self.level = 1  # Determines production efficiency
        self.XP = 0

    def __str__(self):
        """String representation of object, first name and last name.

        Returns:
        str -- "Firstname Lastname"
        """
        return "{} {}".format(self.name, self.surname)

    def print_(self):
        """Print name and attributes."""
        print_line(
            self,
            "    Age: {}".format(self.age),
            " Gender: {}".format(self.gender),
            " Hunger: {}".format(self.hunger),
            " Thirst: {}".format(self.thirst),
            fast = True)
        if self.assigned_room != "":
            print_line("   Room: {}".format(self.assigned_room))
    
    def see_stats(self):
        """Check stats of inhabitant."""
        print_line("Strength: ", self.strength)
        print_line("Perception: ", self.perception)
        print_line("Endurance: ", self.endurance)
        print_line("Charisma: ", self.charisma)
        print_line("Intelligence: ", self.intelligence)
        print_line("Luck: ", self.luck)
        if isinstance(self, Player):  # Player has extra stats
            print_line("")
            print_line("Medic: ", self.medic)
            print_line("Crafting: ", self.crafting)
            print_line("Tactician: ", self.tactician)
            print_line("Cooking: ", self.cooking)
            print_line("Inspiration: ", self.inspiration)
            print_line("Scrapping: ", self.scrapper)
            print_line("Bartering: ", self.barter)
            print_line("Electricain: ", self.electrician)
    
    def level_up(self):
        """Level up Human and ask player for input on what stat to level up."""
        see_stats(self.name, self.surname)
        self.level += 1
        if self.name == people[0].name:  # If player has leveled up
            print_line("\n")
            choice = input("Please choose an attribute to level up: ")
            choice.lower()
            if choice == "strength":
                self.strength += 1
            elif choice == "perception":
                self.perception += 1
            elif choice == "endurance":
                self.endurance += 1
            elif choice == "charisma":
                self.charisma += 1
            elif choice == "intelligence":
                self.intelligence += 1
            elif choice == "luck":
                self.luck += 1
            elif choice == "medic":
                self.medic += 1
            elif choice == "crafting":
                self.crafting += 1
            elif choice == "tactitian":
                self.tactitian += 1
            elif choice == "cooking":
                self.cooking += 1
            elif choice == "inspiration":
                self.inspiration += 1
            elif choice == "scrapper":
                self.scrapper += 1
            elif choice == "barter":
                self.barter += 1
            elif choice == "electrician":
                self.electrician += 1
            else:
                print_line("Invalid choice")
                self.level -= 1
                self.level_up()
        else:  # If NPC has levelled up
            if choice == "strength":
                self.strength += 1
            elif choice == "perception":
                self.perception += 1
            elif choice == "endurance":
                self.endurance += 1
            elif choice == "charisma":
                self.charisma += 1
            elif choice == "intelligence":
                self.intelligence += 1
            elif choice == "luck":
                self.luck += 1
            else:
                print_line("\nInvalid choice.\n")
                self.level -= 1
                self.level_up()

    def heal(self, amount):
        """Heal Human.

        Arguments:
        amount -- amount of health to give
        """
        player = people[0]
        if player.medic > 0:  # Medic Boost.
            amount = amount * (1 + (0.05 * player.medic))
        self.HP += amount
        if self.HP > 99:  # Truncates health
            self.HP = 100

    def rebirth(self):
        """Don't know if I'll ever use this."""
        self.age = 0
        if self.gender == "f":
            print_line(
                self.name +
                " has been reborn and his stats have been reset")
        else:
            print_line(
                self.name +
                " has been reborn and her stats have been reset")
        self.strength = 1
        self.perception = 1
        self.endurance = 1
        self.charisma = 1
        self.intelligence = 1
        self.luck = 1

    def get_index(self): #Shouldn't need this anymore
        """Return index of Human in list of all people.

        Returns:
        x -- index of Human in list
        """
        for x in range(len(people)):
            if people[x].name == self.name and \
                    people[x].surname == self.surname:
                return int(x)

    def mature(self, person):
        """Increment Human's age.

        Arguments:
        person -- Human who's aging
        """
        person.age += 1
        print_line(
            person.name + " has matured and is now ",
            person.age + " years old!")

    def take_damage(self, amount):
        """Take health from Human.

        Arguments:
        amount -- amount of health to take
        """
        person.defense = person.strength * 10
        damage_taken = amount - person.defense
        if damage_taken < 1:
            damage_taken = 0
        else:
            person.HP -= damage_taken
            if person.HP < 1:
                person.die()
    
    def increase_hunger(self, amount):
        """Increase hunger level of Human by certain amount
        
        Arguments:
        amount -- amount of hunger to increase by
        """
        self.hunger += amount
    
    def increase_thirst(self, amount):
        """Increase thirst level of Human by certain amount
        
        Arguments:
        amount -- amount of thirst to increase by
        """
        self.thirst += amount
    
    def scavenge(self, days=10):
        """Send inhabitant on scavenging mission.

        Arguments:
        days -- ask user for number of days if this is 'days'.
        """
        self.current_activity = "scavenging"
        if not (isinstance(days, int)) or days <= 0:
            person.days_to_scavenge_for = 10
        else:
            person.days_to_scavenge_for = days
    
    def unassign(self):
        """Unassign Human from room."""
        pass #Needs work

    def assign_to_room(self, chosen_room):
        """Assign Human to room.

        Arguments:
        chosen_room -- room to assign to
        """
        
        """ #This needs complete reworking.
        global rooms
        global people
        person_index = self.get_index()
        # print_line("Index of ",self.name,"is",person_index)
        room_index = get_room_index(chosen_room)
        # print_line("Index of ",chosen_room," is ",room_index)
        room = rooms[room_index]  # Refers to the actual room
        # print_line("Chosen room is",room.name)
        if people[person_index].assigned_room != '':
            for room in rooms:
                string = str(room.assigned)
                lst = []
                for digit in string:
                    lst.append(digit)
                lst[person_index] = '0'
                string = ''
                for digit in lst:
                    string = string + digit
                room.assigned = string
        string = str(room.assigned)
        # print_line("Assigned log",string)
        lst = []
        for digit in string:
            lst.append(digit)
        # print_line("Assigned log",lst)
        lst[person_index] = '1'
        string = ''
        for digit in lst:
            string = string + digit
        room.assigned = string
        # print_line("Updated assigned log",room.assigned)
        # Let's  character know where they've been assigned.
        people[person_index].assigned_room = str(chosen_room)
        # print_line("Room",self.name,"has been assigned to is",
        #     people[person_index].assigned_room)
        """
        print_line(
            self.name + " " + self.surname +
            "has been assigned to " + chosen_room)

    def can_mate(self):
        """Check if Human meets requirements to have children.

        Returns:
            bool -- whether or not human can mate
        """
        if self.age < 18:
            return False
        if len(self.children) > 5:  # Upper limit of children is 5
            return False
        # Have to wait for a year before parent can have child again.
        for child in self.children:
            if people(child).age < 1:
                return False
        return True

    def die(self, game):
        """Kill self, and unassign from a assigned room.

        Arguments:
        game -- main game object
        """
        print_line("{} has died!".format(self))
        if self.assigned_room:
            game.rooms[self.assigned_room].remove(str(self))
        if not isinstance(self, Player):
            del game.people[str(self)]
        else:
            game.player.alive = False


class NPC(Human):
    """NPC class, inherits Human attributes."""

    def __init__(
            self, first_name, day_of_birth,
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
        Human.__init__(
            self, first_name, day_of_birth,
            parent_1, parent_2, age, gender)
        self.current_activity = ""
        self.days_active = 0
        self.activity_limit = 0
        self.scavenging = False
        self.days_scavenging = 0
        self.days_to_scavenge_for = 0


class Player(Human):
    """Player class, inherits Human attributes."""

    def __init__(
            self, first_name=None, day_of_birth=0,
            parent_1=None, parent_2=None, age=21, gender='M'):
        """Player class constructor.

        Arguments:
        first_name -- first name of Player
        day_of_birth -- day Player was born
        parent_1 -- name of Player's father
        parent_2 -- name of Player's mother
        age -- age of player
        gender -- gender of player
        """
        Human.__init__(
            self, first_name, day_of_birth,
            parent_1, parent_2, age, gender)
        self.medic = 0  # Improves healing capabilities of stimpacks
        self.crafting = 0  # Chance to not use components when crafting.
        self.tactician = 0  # Boosts defense.
        self.cooking = 0  # Boosts production level of kitchen.
        self.barter = 0  # Increases selling prices, decreases buying prices.
        self.inspiration = 0  # Boosts production and defense.
        self.scrapper = 0  # Boosts chance of bonus components when scrapping.
        self.electrician = 0  # Boosts power production
