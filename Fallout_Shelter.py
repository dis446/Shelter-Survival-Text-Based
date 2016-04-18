"""Text-based Fallout Shelter game developed by T.G."""

from collections import OrderedDict
from random import randint
from appdirs import user_data_dir
import pickle
import sys
import os

from Human import Human, Player, NPC
from Room import Room, all_rooms
from Item import Item, Inventory, all_items

from general_funcs import *

try:
    try:
        import readline
    except ImportError:
        import pyreadline as readline
        
#can't get any readline library, default to standard IO
except ImportError:
    pass
    
def save_file():
    """Generate save file location/name based on system.

    Returns:
    str -- path to save file
    """
    sfn = "fstb.p"
    if "-l" in sys.argv:
        sfp = os.path.split(os.path.abspath(sys.argv[0]))[0]
    else:
        appname = "Fallout-Shelter-Text-Based"
        sfp = user_data_dir(appname=appname, appauthor=False, roaming=True)
    return os.path.join(sfp, sfn)


_save_file = save_file()


class Game(object):
    """Main game class."""

    def __init__(self):
        """Initilize main game system."""
        self.setup_player()
        self.all_items = all_items()  # Fetches all items from items.json
        self.all_rooms = all_rooms()  # Fetches all items from rooms.json
        self.inventory = Inventory(self.all_items)
        self.inventory['turret'] += 1
        self.inventory["steel"] += 5
        self.inventory["chip"] += 1
        self.trader_inventory = Inventory(self.all_items)
        self.rooms = {
            'living' : Room('living'),
            'generator' : Room('generator'),
            'water' : Room('water'),
            #'trader' : Room('trader'),
            'kitchen' : Room('kitchen')
        }
        self.people = {}
        self.caps = 100
        self.trader_caps = 500
        self.happiness = 100
        self.action_points = 50
        self.defense = 0
        self.security = "secure"  # Is this the player's job security?
        self.days = 1
        self.overuse = False #If player uses too many action points in one day.
        self.actions = OrderedDict()  # [('action': function)]
        self.first_few()
        action_see_people(self)
        if check_built_room(self, "trader"):
            self = find_rand_items(self, 'trader', 10)

        self.add_action(
            "quit",
            action_quit)
        self.add_action(
            "save",
            action_save)
        self.add_action(
            "load",
            load_game)
        self.add_action(
            "skip",
            None)
        self.add_action(
            "help",
            action_help)
        self.add_action(
            "see day",
            action_see_day)
        self.add_action(
            "see people",
            action_see_people)
        self.add_action(
            "see inventory",
            action_see_inventory)
        self.add_action(
            "see items",
            action_see_inventory)
        self.add_action(
            "see trader",
            action_see_inventory)
        self.add_action(
            "see rooms",
            action_see_rooms)
        self.add_action(
            "see resources",
            action_see_resources)
        self.add_action(
            "auto assign all",
            action_auto_assign)
        self.add_action(
            "trade",
            action_trade)
        self.add_action(
            "craft",
            action_craft)
        self.add_action(
            "rush",
            action_rush_room)
        self.add_action(
            "assign",
            action_assign_to_room)
        self.add_action(
            "unassign",
            action_unassign)
        self.add_action(
            "auto feed all",
            action_auto_feed_all)
        self.add_action(
            "coitus",
            action_coitus)
        self.add_action(
            "build",
            action_build_room)
        self.add_action(
            "fix",
            action_fix_room)

    def add_action(self, name, action):
        """Add entries to the actions dictionary.

        Arguments:
        name -- name of action
        action -- function to execute
        """
        self.actions[name] = action

    def setup_player(self):
        """Create player object."""
        invalid_name = "Invalid name. Only one word is acceptable."
        while True:
            name = input("Choose a first name for yourself: ")
            if validate_name(name):
                first_name = name
                break
            print_line(invalid_name)
        while True:
            name = input("What is the surname of your father? ")
            if validate_name(name):
                father = Human(surname=name)
                break
            print_line(invalid_name)
        while True:
            name = input("What is the surname of your mother? ")
            if validate_name(name):
                mother = Human(surname=name)
                break
            print_line(invalid_name)
        while True:
            gender = input("Please enter your gender (M/F): ")
            if len(gender) >= 1 and gender[0].upper() in ("M", "F"):
                gender = gender[0].upper()
                break
            print_line("Invalid gender choice.")
        self.player = Player(first_name, 0, father, mother, 21, gender)

    def first_few(self):
        """Create first few inhabitants with random names."""
        used_names = []
        names = [
            "Thompson",
            "Elenor",
            "Codsworth",
            "Sharmak",
            "Luthor",
            "Marshall",
            "Cole",
            "Diven",
            "Davenport",
            "John",
            "Max",
            "Lex",
            "Leth",
            "Exavor"]
        for person_name in self.people.keys():
            used_names.append(person_name.split(" ")[0])
            used_names.append(person_name.split(" ")[1])
        load_time(100, "Populating vault with random inhabitants.")
        while len(self.people) < 5:
            num_1 = randint(0, len(names) - 1)
            num_2 = randint(0, len(names) - 1)
            if num_1 == num_2:
                continue
            if names[num_1] in used_names or names[num_2] in used_names:
                continue
            self.people["{} {}".format(names[num_1], names[num_2])] = NPC(
                    names[num_1],
                    self.days,
                    None,
                    "Alena",
                    21,
                    get_gender(),
                    names[num_2])
            used_names.append(names[num_1])
            used_names.append(names[num_2])

    def storage_capacity(self):
        """Calculate max inventory capacity of player.

        Returns:
        capacity -- max inventory capacity of player
        """
        capacity = self.rooms["storage"].production
        return capacity
        
    def use_points(self, number):
        """Remove action points from total.

        Arguments:
        number -- how many points to remove
        """
        if self.action_points - number < 0:  # If overuse occurs, i.e. if overuse is negative
            self.overuse = True
            self.overuse_amount = 0 - (self.action_points - number)
        self.action_points -= number
            
    def run(self, debug=False):
        """Main game. Once all values are initilized or loaded from a save file, this is run."""
        action_help(self)  # Initially prints the available commands.
        while True and self.player.alive:  # Day loop
            self.action_points = 50
            if self.overuse:
                self.action_points -= self.overuse_amount
                
            load_time(100, "A new day dawns. It is now day {} in the vault".format(
                self.days))
            

            self = update_all_room_production(self)
            #Room loop
            for room in self.rooms.values():
                if self.inventory['watt'] >= room.wattage:
                    self.inventory['watt'] -= room.wattage #Use power
                    if room.produce:
                        self.inventory[room.produce] += room.production
                else:
                    print_line("Not enough power to operate room: {}".format(
                        room.name))
                if room.rushed:
                    room.rushed = False
            
            self = action_auto_feed_all(game)
            for person in self.people.values(): #People loop
                if person.check_xp():
                    person.level_up()
                person.increase_hunger(10)
                if person.hunger > 99:
                    person.die(self, "hunger")
                elif person.hunger > 80:
                    print_line(
                        "Warning! {} is starving and may die soon".format(
                            person))
                elif person.hunger > 50:
                    print_line("{} is hungry".format(person))
                person.increase_thirst(20)
                if person.thirst > 99:
                    person.die(self, "thirst")
                elif person.thirst > 80:
                    print_line("Warning! {} is extremely thristy " +
                               "and may die soon.".format(person))
                elif person.thirst > 50:
                    print_line("{} is thirsty".format(person))
                if person.current_activity != "":
                    if person.current_activity == "scavenging":
                        person = take_damage(person, randint(0, 30))
                        if person.health < 20:
                            pass  # Need to end scavenging.
                    elif person.current_activity == "guarding":
                        pass
                    if person.days_active == person.activity_limit:
                        if person.current_activity == "scavenging":
                            print_line("{} has come back from".format(person) +
                                       " scavenging and has found these items")
                            # Need to print items found.
                        person.current_activity = ""
                        person.active_days = 0
                        person.activity_limit = 0
                    else:
                        person.days_active += 1
            
            if check_built_room(self, 'trader'): #Trader randomly loses and gains items daily
                if game.rooms['trader'].assigned:
                    self = lose_items(self, 'trader', 10)
                    self = find_rand_items(self, 'trader', 10)
                    
            while self.action_points > 0:  # Choice loop
                print_line("Action Points Remaining: {}".format(self.action_points))
                a = input("Choose an action: ")
                if len(a) > 0:
                    action, *args = a.split()
                    if action.lower() == "skip":
                        break
                    elif action in ("trade", "assign", "unassign", \
                    "auto feed all", "auto assign all", "build", "craft",\
                    "fix", 'rush', 'coitus'):
                        try:
                            self = self.actions[action](self, *args)
                        except TypeError:
                            print_line("Incorrect number of arguments")
                    elif a in self.actions.keys():
                        try:
                            self.actions[a](self, *args)
                        except Exception as e:
                            print_line("Error: {}".format(e))
                    elif action in ("save", "load"):
                        self.actions[action](self, args[0])
                    
                    else:
                        print_line("Invalid action selected. Try again.")
                else:
                    print_line("You have to choose a valid action.")
            self.days += 1


def load_game(_=None, save=_save_file):
    """Load game from file, `load filename` to load from specific file.

    Arguments:
    save -- file to load from

    Returns:
    game -- Game object
    """
    with open(save, "rb") as s:
        try:
            game = pickle.load(s)
        except pickle.UnpicklingError:
            print_line("Unable to load game.")
            return None
    print_line("Game loaded from {}.".format(save))
    return game


def action_quit(*_):
    """Quit current game.

    Arguments:
    game -- main game object
    """
    save = default_input("Quit without saving? (y/N) ")
    if save == "n":
        return
    else:
        sys.exit(0)


def action_save(game, save=_save_file):
    """Save current game state, `save filename` to save to specific file.

    Arguments:
    game -- game object to save
    save -- file to save to
    """
    if os.path.exists(save):
        ow = default_input("{} already exists, overwrite? (Y/n) ".format(save))
        if ow != 'y':
            return
    with open(save, "wb") as s:
        try:
            pickle.dump(game, s)
        except pickle.PicklingError:
            print_line("Unable to save game.")
            return
    print_line("Game has been saved to {}.".format(save))


def action_help(game):
    """See help for all actions available.

    Arguments:
    game -- main game object
    """
    print_line('Actions:')
    lens = text_align(game.actions)
    for i, action in enumerate(game.actions.keys()):
        if action == "skip":
            desc = "Skip current day."
        else:
            desc = sentence_split(game.actions[action].__doc__)
        print_line('{}{}: {}'.format(
            action,
            ' ' * (2 + lens[i]),
            desc),
            speed=FAST)


def action_see_day(game, *args):
    """See current day number.

    Arguments:
    game -- main game object
    """
    print_line("It is currently day number {} in the vault.".format(game.days))


def action_see_people(game, *args):
    """Display info of all inhabitants.

    Arguments:
    game -- Main game object
    """
    game.player.print_()
    for person in game.people.values():
        person.print_()


def action_see_inventory(game, inventory):
    """See given inventory's contents.

    Arguments:
    game -- main game object
    inventory -- inventory to print
    """
    inv = inventory.lower()
    if inv == "inventory":
        game.inventory.print_()
    elif inv == "trader":
        game.trader_inventory.print_()
    else:
        print("No inventory named '{}' exists.".format(inventory))


def action_see_rooms(game, *args):
    """Print each room with details.

    Arguments:
    game -- main game object
    """
    game = update_all_room_production(game)
    for room in game.rooms.values():
        room.print_()


def action_see_resources(game, *args):
    """See available resources (food, water, and power).

    Arguments:
    game -- Main game object
    """
    print_line("Food * ", game.inventory["food"])
    print_line("Water * ", game.inventory["water"])
    print_line("Power * ", game.inventory["watt"])


def living_capacity(game):
    """Get maximum inhabitant capacity of shelter.

    Arguments:
    game -- main game object

    Returns:
    int -- maximum capacity of shelter
    """
    room = game.rooms["living"]
    print_line("Maximum number of inhabitants", 5 * room.level)
    return (5 * room.level)


# Construction system:

def action_build_room(game, room_name):
    #Need to check if player has the materials to build room
    """Build room specified.

    Arguments:
    game -- Main game object
    room_name -- name of room to build

    Returns:
    game -- Main game object
    """
    if check_room(game, room_name):
        if not check_built_room(game, room_name):            
            room = Room(str(room_name))  # creates a room.
            game.rooms[str(room_name)] = room  # Stores the room in memory.
            load_time(50, "Building " + room_name)
            for y in room.components:  # Does this for each component
                game.inventory[y] -= 1
            #game.player.gain_xp(100) #Commented out for now since levelling up
            # system doesn't work
            game.use_points(50)
        else:
            print_line("You've already built the {} room.".format(room_name.title()))
    else:
        print_line("{} isn't a valid room name.".format(room_name.title()))
    return game


def action_craft(game, item_name):
    """Craft specified item.

    Arguments:
    game -- Main game object
    item_name -- name of item to craft

    Returns:
    game -- Main game object
"""
    if can_craft_item(game, item_name):
        load_time(5, ("Crafting ", item_name))
        game.inventory[item_name] += 1
        # Perk bonuses
        item = Item(item_name)
        chance = game.player.stats["crafting"]
        for component in item.components:
            if randint(1,101) > chance:
                #The higher the player's crafting level, the less
                #likely they are to lose their items.
                game.inventory[component] -= 1
        #game.player.gain_xp(item.rarity * 10)
        #game.use_points(5)
    return game

def action_scrap(game, item):
    """Deletes an item from the inventory and adds it's components to the inventory

    Arguments:
    game -- Main game object
    item -- name of item being scrapped

    Returns:
    game -- Main game object
    """
    it = Item(item)
    for component in it.components:
        game.inventory[component] += 1
    game.inventory[item] -= 1
    return game

# Human management system:


def get_gender():
    """Randomly generate gender for NPC.

    Returns:
    char -- 'm' or 'f'
    """
    if randint(0, 1) == 0:
        return "m"
    else:
        return "f"


def check_person(game, name):
    """Check if inhabitant exists in list of all inhabitants.

    Arguments:
    game -- Main game object
    name -- full name of person

    Returns:
    bool -- whether inhabitant exists or not
    """
    #print("Checking to see if {} exists".format(name.title()))
    if name.title() in game.people.keys():
        return True
    else:
        return False
    
def action_assign_to_room(game, *args):
    """ Assign a person to a room.
        In the form "assign first_name surname to room"
    
    Arguments:
    game -- main game object
    first_name -- first_name of person
    surname -- surname of person
    room -- room to assign to 
    
    Returns:
    game -- Main game object
    """
    
    if len(args) == 4:
        if args[2] == "to":
            if check_person(game, str(args[0]) + " " + str(args[1])):
                if check_built_room(game, args[3]):
                    game = assign_to_room(game,
                    args[0].title() + " " + args[1].title(),
                    args[3])
                else:
                    if not check_room(game, args[3]):
                        print_line("This room doesn't exist")
                    else:
                        print_line("You need to build the {} room".format(args[4]))
            else:
                print_line("This person doesn't exist")
        else:
            print_line("Invalid syntax. Must be in form of (assign cole leth to living)")
    else:
        print_line("Invalid syntax. Must be in form of (assign cole leth to living)")
    return game    
        
def assign_to_room(game, person_name, room_name):
    """Assign Human to room, assuming all inputted arguments are valid.

    Arguments:
    game -- Main game object
    person_name -- full name of person being assigned (with first letter's capitalized)
    room_name -- name of room to assign to
     
    """
    room = game.rooms[room_name]
    person = game.people[person_name]
    if room.count_assigned() < room.assigned_limit:
        if person.assigned_room: #If person is already assigned to a room, unassigns them.
            game = unassign(game, person_name)
        room.assigned.append(person_name)
        person.assigned_room = room_name
        game.use_points(1)
        print_line("{} has been assigned to the {}".format(person_name, str(room)))
    else:
        print("The {} has {} people assigned and can hold no more".format(str(room), room.count_assigned()))
    return game

def action_unassign(game, first_name, surname):
    """ Unassigns person from their room.
        Checks to see if all arguments are valid, then passes them to 
        unassing() function. Only called by the player.
    
    Arguments:
    game -- main game object
    first_name -- first name of person to unassign
    surname -- surname of person to unassign
    
    Returns:
    game -- Main game object
    
    """
    name = first_name.title() + " " + surname.title() 
    if len(name.split()) == 2:
        if check_person(game, name): 
            game = unassign(game, name)
        else:
            print_line(" This person doesn't exist")
    else:
        print_line("The name must be 2 words")
    return game

def unassign(game, name):
    """ Unassigns person from their room.
    
    Arguments:
    game -- main game object
    name -- name of person to unnassign
    
    Returns:
    game -- Main game object
    
    """
    name = name.split()[0].title() + " " + name.split()[1].title() 
    person = game.people[name]
    room = game.rooms[person.assigned_room]
    print_line("{} has been unassigned from the {}".format(name, str(room)))
    person.assigned_room = ""
    room.assigned.remove(name)
    return game

def action_coitus(game, *args):
    """Have two adults try for a child.
    
    Arguments:
    game -- main game object
    parent_1 -- name of first parent
    parent_2 -- name of second parent
    
    Returns:
    game -- main game object
    """
    if len(args.split(" ")) == 4:
        parent_1_name = args[0:2]
        if check_person(game, parent_1_name):
            parent_1 = game.people[parent_1_name]
            parent_2_name = args[2:]
            if check_person(game, parent_2_name):
                parent_2 = game.people[parent_2_name]
                person = create_npc(parent_1, parent_2)
                game.people[str(person)] = person
            else:
            print_line("Invalid name: {}".format(parent_2_name))
        else:
            print_line("Invalid name: {}".format(parent_1_name))
    else:
        print_line("Invalid input. You have to input two names")

def create_npc(
        parent_1,
        parent_2):
    """Create new child inhabitant.

    Arguments:
    parent_1 -- parent of new child
    parent_2 -- parent of new child

    Returns:
    person -- New NPC
    """
    while True:
        name = input("Choose a first name for the new child: ")
        if len(name.split()) == 1:  # Player can only input one word
            if name not in used_names: #This doesn't work
                name = name.title()  # Capitalizes first letter_
                if parent_2.gender == "m":
                    parent_1, parent_2 = parent_2, parent_1
                person = NPC(
                    name,
                    days,
                    parent_1.surname,
                    parent_2.surname,
                    0,
                    get_gender())
                # From here
                parent_1.children.append(str(name + " " + parent_1_surname))
                parent_2.children.append(str(name + " " + parent_1_surname))
                parent_1.partner = parent_2.name + " " + parent_2.surname
                parent_2.partner = parent_1.name + " " + parent_1.surname
                if game.days > 2:  # First few births cost no points
                    use_points(50)
                used_names.append(name)
                #Unil here need to be moved outside of this function
                load_time(5, (name, " is being born!"))
                return person
            else:
                print_line("Someone already has that name.")
                create_npc(
                    parent_1,
                    parent_2)
        else:
            print_line("You have to input a single word!")
            create_npc(
                parent_1,
                parent_2)
        

def create_player():
    """Create player inhabitant.

    Returns:
    Player -- player object
    """
    while True:
        name = input("Choose a first name for yourself: ")
        if len(name) <= 0:
            print_line("You need a name!")
        elif len(name.split()) != 1:
            print_line("Only single word inputs are accepted.")
        else:
            name = name.title()
            break
    while True:
        parent_1 = input("What is the surname of your father? ")
        if len(parent_1) <= 0:
            print_line("Your father needs a surname!")
        elif len(parent_1.split()) != 1:
            print_line("Only single word inputs are accepted.")
        else:
            parent_1 = parent_1.title()
            break
    while True:
        parent_2 = input("What is the surname of your mother? ")
        if len(parent_2) <= 0:
            print_line("Your mother needs a surname!")
        elif len(parent_2.split()) != 1:
            print_line("Only single word inputs are accepted.")
        else:
            parent_2 = parent_2.title()
            break
    while True:
        gender = input("What is your gender?(m/f) ")
        if len(gender) == 0:
            print_line("You need a gender.")
        elif gender[0].lower() not in ("m", "f"):
            print_line("Invalid input. Only accepts 'm' or 'f'.")
        else:
            gender = gender[0].lower()
            break

    return Player(
        name,
        days,
        parent_1,
        parent_2,
        21,
        gender)


def action_auto_assign(game, *args):
    """Automatically assign inhabitants to rooms.

    Arguments:
    game -- Main game object
    """
    while True:
        for room in game.rooms.values():
            if room.count_assigned() < room.assigned_limit:
                for person in game.people.values():
                    if not person.assigned_room:
                        break
                game = assign_to_room(game, str(person), room.name)
        unemployed_count = 0
        for person in game.people.values():
            if not person.assigned_room:
                unemployed_count +=1
        if unemployed_count == 0:
            break
    return game


# Room Management system:

def action_rush_room(game, room):
    """Rush a room in the game.

    Arguments:
    game -- Main game object
    room -- name of room to rush

    Returns:
    game -- main game object
    """
    try:
        room = game.rooms[room]
    except KeyError:
        print_line("No such room!")
        return game

    if not room.can_rush:
        print_line("Cannot rush {}".format(room))
        return game

    room.rush()

    random = randint(0,101)
    if random < room.risk:
        print_line(" The {} room has been broken.".format(room.name))
        room.broken = True
    else:
        room.rushed = True
    return game

def check_room(game, room):
    """Check if room exists.

    Arguments:
    game -- main game object
    room -- room to check for

    Returns:
    bool -- whether room exists or not
    """
    if room in game.all_rooms:
        return True
    return False


def check_built_room(game, room):
    """Check if room has been built yet.

    Arguments:
    game -- main game object
    room -- room to check for

    Returns:
    bool -- whether room has been built or not
    """
    if room in game.rooms:
        return True
    return False


def can_use_power(game, room):
    """
    Determine whether the room may use power or not.

    Arguments:
    game -- main game object
    room - room which uses power

    Returns:
    bool -- whether room may use power
    """
    if game.inventory["watt"] > room.power_usage:
        return True
    else:
        return False


def power_usage(game):
    """Check total power needed.

    Arguments:
    game -- main game object

    Returns:
    total -- total power needed by all rooms
    """
    total = 0
    for room in game.rooms:
        total += room.power_usage
    return total


def power_production(game):
    """Check total power being produced.

    Arguments:
    game -- main game object

    Returns:
    production -- total amount of power being produced
    """
    generator = game.rooms['generator']
    return generator.production

def action_fix_room(game, room_name):
    """Tries to fix room.
    Arguments:
    game -- Main game object
    room_name -- Name of room to try to fix
    
    Returns:
    game -- Main game object
    """
    if check_room(game, room_name):
        if check_built_room(game, room_name):
            room = game.rooms[room_name]
            if room.broken:
                can_fix = True
                items_needed = Inventory(game.all_items)
                for component in room.components:
                    if randrange(0,1) == 0:
                        items_needed[component] += 1
                for item_needed in items_needed.keys():
                    if game.inventory[item_needed] \
                    < items_needed[item_needed]:
                        can_fix = False
                        print_line("You don't have enough {} to fix\
                        {} room".format(item_needed, room_name))
                if can_fix:
                    room.fix()
            else:
                print_line("{} room doesn't need to be fixed".format(room_name))
        else:
            print_line("You haven't built the {} room yet".format(room_name))
    else:
        print_line("Invalid room name: {}".format(room_name))
    return game
                        
def update_all_room_production(game):
    for room in game.rooms.values():
        production = 0
        if room.broken:
            print_line(room.name, "is broken and needs to be fixed.")
        else:
            player = game.player
            if room.attribute:
                attribute = room.attribute
                for person_name in room.assigned:
                    person = game.people[person_name]
                    for stat in person.stats:
                        if stat == attribute:
                            level = person.stats[stat]
                            production += level
                    production += 1
            
            if room.perk: #Some player perks improve production.
                value = game.player.stats[room.perk]
                production = production * (1 + (value * 0.05))
                
            if player.stats["inspiration"] > 0:
                production = production * \
                (1 + (player.inspiration * 0.03))
            if room.can_rush:
                if room.rushed:
                    production = production * 2
        
        room.production = production * 10
    return game


# Inventory managment system:


def count_weight(game):
    """Calculate weight of all items in inventory.

    Arguments:
    game -- main game object

    Returns:
    weight -- weight of all items in inventory
    """
    weight = 0
    for x in game.inventory:
        weight += Item(x).weight
    return weight


def find_rand_items(game, inven, num):
    """Find random items and add them to inventory.

    Arguments:
    game -- main game object
    inven -- inventory to add items to
    items -- how many items to add

    Returns:
    game -- with all items added.
    """
    for x in range(num):
        # Following lines randomly choose an item, based on rarity
        rand_num = randint(1, 1024)
        lst = [2**a for a in range(0, 11)]
        rarity = 1
        for chance in lst:
            if rand_num < chance:
                break
            rarity += 1
        # Determines the rarity of an item. 50% chance it's a level 1,
        # 25% chance it's a level 2, 12.5% chance it's a level 3 and so on.
        
        # Stores each item if the rarity level matches what was randomly picked
        possible_items = []
        for it in game.all_items:
            if Item(it).rarity == rarity:
                possible_items.append(it)
        if len(possible_items) > 0:
            actual_item = possible_items[randint(0, len(possible_items) - 1)]
            # Following lines actually store the item in memory
            if inven == "player":
                game.inventory[actual_item] += 1
            elif inven == "trader":
                game.trader_inventory[actual_item] += 1
    return game


def add_to_inven(game, item, number, inven): #Shouldn't need this anymore
    """Add given item to inventory.

    Arguments:
    x -- item to add to inventory
    number -- amount of item to add to inventory
    inven -- inventory to add item to
    """
    item = str(item)
    inven = str(inven)
    if inven == "player":
        for y in range(number):
            pass  
    elif inven == "trader":
        for y in range(number):
            pass  
    return game


def list_of_items(game, inven):
    """Returns a flat list of every item present in the chosen inventory
    
    Arguments:
    game -- Main game object
    inven -- chosen inventory to search
    
    Returns:
    list -- all the items found in the inventory.
    """
    found_items = []
    if inven == "player":
        for item, num in game.inventory.items():
            if num > 0:
                found_items.append(item)
    elif inven == "trader":
        for item, num in game.trader_inventory.items():
            if num > 0:
                found_items.append(item)
    return found_items


def can_craft_item(game, item_name):
    """Checks to see if an item can be built
    
    Arguments:
    game -- main game object
    item -- name of item to check
    
    Returns:
    bool -- Whether or not item can be crafted
    """
    item = Item(str(item_name))
    can_craft = True
    checked_components = []

    #handle case where item is not in items.json
    if not hasattr(item, 'components'):
        return False
    for component in item.components:
        if component not in checked_components:
            number_needed = item.components.count(component)
            number_available = game.inventory[component]
            if number_needed > number_available:
                can_craft = False
                print_line("You need {} more {} to craft this item"\
                .format(number_needed - number_available, component))
        checked_components.append(component)
        checked_components.append(component)
    return can_craft
    
def lose_items(game, inven, number):
    """Randomly delete multiple items from inventory.

    Arguments:
    game -- main game object
    inven -- inventory to delete items from
    number -- amount of items to delete

    Returns:
    game -- with less items in selected inventory
    """
    if inven == "trader":
        for x in range(number):
            items_available = list_of_items(game, "trader")
            item = items_available[randint(0, len(items_available) - 1)]
            game.inventory[item] -= 1
    elif inven == "player":
        for x in range(number):
            items_available = list_of_items(game, "player")
            item = items_available[randint(0, len(items_available) - 1)]
            game.trader_inventory[item] -= 1
    else:
        print_line("Major bug in item losing system. Please contact dev!")
    return game


def action_scrap(game, item):
    """Scrap item and recieve its components.

    Arguments:
    game -- main game object
    item -- item to scrap

    Returns:
    game -- with the item removed and it's components added to the
    """
    if item not in game.all_items:
        print_line(
            "Bug with item scrapping system.",
            "Invalid argument passes to function. Please contact dev.")
    else:
        game.inventory[item] -= 1
        item = Item(item)
        for component in item.components:
            game.inventory[component] += 1
    use_points(2)
    return game

# Raiding system:


def raid(game):
    """Force raid on shelter.

    Arguments:
    game -- main game object
    """
    game = update_defense(game, player)
    raiders = ["Super Mutant", "Raider", "Synth", "Feral Ghoul"]
    raider_index = randint(0, len(raiders))
    raider = raiders[raider_index]  # Randomly chooses a raider party.
    max_attack = days // 5
    attack_power = randint(1, max_attack)
    load_time(10, ("There was a " + raider + " raid on your shelter!"))
    print_line("The total enemy power was", attack_power)
    print_line("Your total defenses are", defense)
    if defense > attack_power:
        print_line("Your defenses were strong enough to send them packing!")
    else:
        loss = attack_power - defense
        lose_items("player", loss)
        if loss > 10:
            death_chance = loss // 10
            dice = randint(2, 25)
            if death_chance < dice:
                # Death
                # The player can't die in a raid!
                possible_deaths = people[1, len(game.people) - 1]
                death_number = randint(len(possible_deaths))
                print_line(
                    possible_deaths[death_number] +
                    " has been killed in a raid")
                # dead_person = game.people[death_number]
                game = death(game, dead.person.name)
    for person in game.people:  # Survivors gain xp
        person.gain_xp(attack_power * 10)
    use_points(30)
    return game


def update_defense(game, player):
    """Update defense of shelter based on guns and turrets in inventory."""
    game.defense = 0
    turret_count = game.inventory["turret"]
    game.defense += 10 * turret_count
    gun_count = game.inventory["gun"]
    game.defense += gun_count
    # Add cases for more items that increase defense
    strength_sum = 0
    for person in game.people.values():
        strength_sum += person.stats["strength"]
    game.defense += strength_sum
    if game.player.tactician > 0:
        game.defense = defense * (1 + (player.tactician * 0.05))
    if game.player.inspiration > 0:
        game.defense = defense * (1 + (player.inspiration * 0.03))
    return game

# Happiness System:

def avg_hunger(game):
    """Calculate average hunger level of all inhabitants.

    Returns:
    avg -- average hunger level
    """
    total = 0
    for person in game.people.values():
        total += person.hunger
    avg = total // len(game.people)
    return avg


def avg_thirst(game):
    """Calculate average thirst level of all inhabitants.

    Returns:
    avg -- average thirst level
    """
    total = 0
    for person in game.people.values():
        total += person.thirst
    avg = total // len(game.people)
    return avg



def action_auto_feed_all(game, *args):
    """Automatically feed all inhabitants."""
    food_count = game.inventory["food"]
    water_count = game.inventory["water"]
    load_time(200, "Feeding all inhabitants.")
    while game.inventory["food"] > 0 and avg_hunger(game) > 1:
        for person in game.people.values():
            person.feed(1)  
            game.inventory["food"] -= 1
    while game.inventory["water"] > 0 and avg_thirst(game) > 1:
        for person in game.people.values():
            person.drink(1)
            game.inventory["water"] -= 1
    return game


def happiness_loss():
    """Decrease overall happiness level based on overall hunger and thirst."""
    global happiness
    loss = 0
    for y in range(30, 101, 10):
        if avg_hunger() < y:
            loss += y - 30
            break
    for y in range(30, 101, 10):
        if avg_thirst() < y:
            loss += y - 30
            break
    if loss > 0:
        happiness -= loss
        print_line(
            "Due to your inhabitants being hungry and/or thirsty the " +
            "shelter's overall happiness has dropped to ",
            happiness)

# Trading system:


def action_trade(game):
    """Trading system."""
    can_trade = True
    if not check_built_room(game, 'trader'):
        print_line("You need to build a trader room")
        return game

    trader_room = game.rooms['trader']
    if not trader_room.assigned: #If trader_room.assigned is empty.
        print_line("There's no one assigned to the trader room!")
        return game
        
    load_time(100, "Initializing trading system.")
    while True:
        print_line("")
        print_line("Here are the traders' items: ")
        action_see_inventory(game, "trader")
        print_line("\nThe trader has " + str(game.trader_caps) + " caps.")

        print_line("\nHere are your items: ")
        action_see_inventory(game, "inventory")
        print_line("\nYou have " + str(game.caps) + " caps.")

        print_line(
            "\nFor instance, input (buy 5 food) if you want to buy 5 " +
            "units of food. Or input (end) to stop trading.")
        a = input("What trade would you like to make? ")
        if len(a) < 1:
            print_line("You have to input something")
            continue

        cmd, *args = a.split()
        cmd = cmd.lower()
        if cmd not in ('buy', 'sell', 'end', 'stop'):
            print_line("Invalid Input, you can (buy), (sell) or (end) the trade")
            continue

        if cmd in ('end', 'stop'):
            break

        #if a number of items is not given, default to 1
        if len(args) == 1:
            args = [1] + args

        if len(args) != 2:
            print_line("Invalid number of arguments")
            continue

        num, item = args

        if item not in game.all_items:
            print_line("This item doesn't exis")
            continue
        try:
            num = int(num)
        except ValueError:
            print_line("You have to input a number as the second word")
            continue

        cost = Item(item).value
        total_cost = cost * num
        print_line("Cost of all items: ", total_cost)
        if cmd == "buy":
            # Adjusts the prices, depending on player's bartering level.
            total_cost = int(total_cost * (1.2 - (game.player.stats['barter'] * 0.05)))
            if total_cost > game.caps:
                print_line("You can't afford that!")
                continue

            count = game.trader_inventory[item]

            if num > count:  # If trader doesn't have enough.
                if count < 1:
                    print_line( "The trader doesn't have any {}".format(item))
                else:
                    print_line( "The trader doesn't have {} of {}".format(num, item))
                continue

            for x in range(num):
                game.trader_inventory[item] -= 1
                game.inventory[item] += 1

            game.caps -= total_cost
            game.trader_caps += total_cost

        elif cmd == "sell":
            # Adjusts the prices, depending on bartering level.
            total_cost = int(total_cost * (0.8 + (game.player.stats['barter'] * 0.05)))
            print("Total cost is " + str(total_cost))
            if total_cost > game.trader_caps:
                print_line("The trader can't afford that!")
                continue

            count = game.inventory[item]
            if num > count:  # If player doesn't have enough of the item to sell.
                if count < 1:
                    print_line( "You don't have any {}".format(item))
                else:
                    print_line( "You don't have {} of {}".format(num, item))
                continue

            for x in range(num):
                game.inventory[item] -= 1
                game.trader_inventory[item] += 1

            game.caps += total_cost
            game.trader_caps -= total_cost
    print_line("Ending trade")
    return game

"""
def choice():  # Need to move these commands into Game() class
    a = input("Choose what to do: ")
    # From here on out, a.split()[0] is used to cut out the first word of the
    # input and compare it individually.
    if len(a) > 0:
        # Allows player to build new rooms. Checks if player has components to
        # build room.
        if a.split()[0] == "build":
            potential_room = ''
            for x in a.split()[1:]:
                if len(potential_room) == 0:
                    potential_room = x
                else:
                    potential_room = potential_room + " " + x
            # print_line("The potential room is",potential_room)
            if len(a.split()) < 2:
                print_line(
                    "You have to input 2 or more " +
                    "words to build a room.")
            elif not check_room(potential_room):
                print_line("Checking for room:", potential_room)
                print_line("This room doesn't exist.")
            elif check_built_room(potential_room):
                print_line("You've already built this room.")
            else:
                room = Room(potential_room, player)
                checked = []
                can_craft = True
                for component in room.components:
                    if component not in checked:
                        if room.count_component(component) > \
                                count_item(game, component, "player"):
                            print_line(
                                "You don't have enough",
                                component,
                                "to build",
                                potential_room)
                            can_craft = False
                            # break #I don't break so the users will see
                            # everything they don't have.
                        checked.append(component)
                if can_craft:
                    print_line("You have built a", a.split()[1])
                    player = player
                    build(potential_room, player)

        elif a.split()[0] == "craft":
            # Checks to see if crafting possible.
            if a.split()[1] not in all_items:
                print_line("Invalid item. Try again.")
            else:
                can_craft = True
                # Creates an instance of the item, so it's attributes can be
                # fetched.
                actual_item = Item(a.split()[1])
                if len(actual_item.components) == 0:
                    print_line(
                        "This is a basic item and " +
                        "so cannot be crafted.")
                else:
                    checked = []
                    for component in actual_item.components:
                        if component not in checked:
                            number_available = count_item(game, component, "player")
                            number_needed = actual_item.count_component(
                                component)
                            if number_needed > number_available:
                                print_line(
                                    "You don't have enough",
                                    component,
                                    "to craft",
                                    a.split()[1])
                                can_craft = False
                            checked.append(component)
                    if can_craft:
                        print_line("You have crafted a", a.split()[1])
                        craft(a.split()[1])

        elif a.split()[0] == "scrap":
            if len(a.split()) == 2:  # Only scrap item once.
                if a.split()[1] not in all_items:
                    print_line("Invalid item. Please try again.")
                else:
                    count = count_item(game, str(a.split()[1]), "player")
                    if count > 0:
                        scrap(a.split()[1])
                    else:
                        print_line("You don't have that item.")
            elif len(a.split()) == 3:  # Scrap multiple times
                if a.split()[1] in range(1, 100):
                    if a.split()[2] in all_items:
                        count = count_item(game, str(a.split()[1]), "player")
                        if count >= a.split()[1]:
                            for x in range(a.split()[1]):
                                scrap(a.split()[2])
                        else:
                            print_line(
                                "You don't have enough of these items " +
                                "to scrap that many times.")
                    else:
                        print_line("This item doesn't exist.")
                else:
                    print_line(
                        "Invalid input.",
                        "You can scrap an item up to 99 times " +
                        "(If you have that many).")
            else:
                print_line(
                    "Invalid Input.",
                    "Either enter (scrap wood) " +
                    "or (scrap 5 wood)")

        elif a.split()[0] == "rush":  # Speeds up room tempoarily.
            potential_room = ''
            for x in a.split()[1:]:
                if len(potential_room) == 0:
                    potential_room = x
                else:
                    potential_room = potential_room + " " + x
            if not check_room(potential_room):
                print_line("This room doesn't exist.")
            elif not check_built_room(potential_room):
                print_line("You haven't built this room yet.")
            elif Room(potential_room).can_rush:
                print_line("This room cannot be rushed")
            elif Room(potential_room).rushed:
                print_line("This room has already been rushed.")
            else:
                room = rooms[get_room_index(potential_room)]
                # Chance that the rush fails and the room tempoarily breaks.
                chance = randint(0, 9)
                if room.risk > chance:
                    print_line(room.name, " has failed to rush and is broken!")
                    room.broken = True
                else:
                    check = input(
                        "Are you sure?",
                        room.name,
                        "has a",
                        room.risk * 10,
                        "% chance of breaking.")
                    if len(check) > 0:
                        if check[0].lower() == "y":
                            room.rush()
                        else:
                            print_line("Rush failed.")
                    else:
                        print_line("Rush failed.")
        elif a.split()[0] == "fix":
            potential_room = ''
            for x in a.split()[1:]:
                if len(potential_room) == 0:
                    potential_room = x
                else:
                    potential_room = potential_room + " " + x
            if not check_room(potential_room):
                print_line("This room doesn't exist.")
            elif not check_built_room(potential_room):
                print_line("You haven't built this room yet.")
            elif not rooms[get_room_index(potential_room)].broken:
                print_line(
                    "This room isn't even broken. " +
                    "There's no need to fix it!")
            else:
                room = rooms[get_room_index(potential_room)]
                can_fix = True
                items_needed = []
                for it in room.components:
                    chance = randint(0, 1)
                    if chance:
                        items_needed.append(it)
                checked_items = []
                for it in items_needed:
                    if it not in checked_items:
                        available = count_item(game, it, 'player')
                        needed = room.count_component(it)
                        if needed > available:
                            print_line(
                                "You need", needed - available,
                                "more", it, "to fix this room.")
                            can_fix = False
                        checked_items.append(it)
                if can_fix:
                    room.broken = False
                    for it in items_needed:
                        Item(it).destroy("player")
                    print_line(
                        room.name,
                        "has been fixed and is now in full working order.")

        elif a.split()[0] == "see":
            if a.split()[1] == "people":
                see_people()
            elif (a.split()[1]) == "items":
                see_inventory("player")
            elif a.split()[1] == "rooms":
                see_rooms()
            elif a.split()[1] == "day":
                print_line("Today is day", days)
            elif a.split()[1] == "resources":
                see_resources()
            else:
                print_line(
                    "Incorrect input.",
                    "You can (see people), (see inventory), " +
                    "(see rooms) or (see resources)")

        elif a.split()[0] == "coitus":
            if len(a.split()) != 5:
                print_line(
                    "You need to input 2 mature people of opposite genders " +
                    "in the form (coitus Alex Marshall Mallus Cumberland)")
            elif not check_person(a.split()[1], a.split()[2]):
                print_line("No such", a.split()[1], a.split()[2], " exists!")
            elif not check_person(a.split()[3], a.split()[4]):
                print_line("No such", a.split()[2], a.split()[4], " exists!")
            elif len(people) == living_capacity():
                print_line(
                    "You've reached the vault's maximum capacity.",
                    "Upgrade your living room to hold more people")
            else:
                person_1 = people[get_person_index(a.split()[1], a.split()[2])]
                person_2 = people[get_person_index(a.split()[3], a.split()[4])]
                if (person_1.partner == "" and person_2.partner == "") or \
                        person_1.partner == person_2.name + " " + \
                        person_2.surname:
                    if person_1.age < 18:
                        print_line(
                            a.split()[1] +
                            " isn't old enough to copulate.")
                    elif person_2.age < 18:
                        print_line(
                            a.split()[2] +
                            " isn't old enough to copulate.")
                    elif person_1.surname == person_2.surname:
                        print_line(
                            "Incest isn't allowed. " +
                            "At least be ethical!")
                    elif person_1.gender == person_2.gender:
                        print_line(
                            "The people need to be different genders! " +
                            "COME ON MAN CAN U EVEN BIOLOGY!?")
                    else:
                        # Pass these love birds to the birthing system
                        person = create_npc(
                            person_1,
                            person_2)
                        people.append(person)
                else:
                    print_line("Infedility shall not be allowed!!!")
                    if person_1.partner != "":
                        print_line(
                            person_1.name,
                            person_1.surname,
                            " is married to ",
                            person_1.partner)
                    else:
                        print_line(
                            person_1.name,
                            person_1.surname,
                            " isn't  married.")
                    if person_2.partner != "":
                        print_line(
                            person_2.name,
                            person_2.surname,
                            " is married to ",
                            person_2.partner)
                    else:
                        print_line(
                            person_2.name,
                            person_2.surname,
                            " isn't  married.")

        # Checks if player has enough food to feed person and then calls
        # feed(person) function.
        elif a.split()[0] == "feed":
            if len(choice) > 0:
                # Counts how much food is available for feeding
                # food_count = count_item("food")
                if avg_hunger() < 2:
                    print_line("Your people are working on full bellies boss!")
                elif len(a.split()) == 2:
                    if a.split()[1] not in people:
                        print_line("This person doesn't exist.")
                    else:
                        # Fetches hunger level of selected Human
                        hunger = people(a.split()[1].hunger)
                        amount = input(
                            "Feed ", a.split()[1], "  by how much? ")
                        if amount < hunger:
                            print_line(
                                "You don't have enough food to feed ",
                                a.split()[1])
                        else:
                            feed(a.split()[1], amount)
                else:
                    print_line(
                        "Invalid input! Can only feed one person like this. ",
                        "Use the auto_feed system to feed everyone.")
            else:
                print_line("Invalid input. Who do you want to feed?")
        elif a.split()[0] == "trade":
            if not check_built_room('trader'):
                print_line("You haven't built a trader room yet!")
            elif '1' not in str(rooms[get_room_index('trader')].assigned):
                print_line(
                    "No one has been assigned to this room!",
                    "You can't trade until then.")
            else:
                trade()

        elif a.split()[0] == "assign":
            potential_room = ''
            for x in a.split()[4:]:
                if len(potential_room) == 0:
                    potential_room = x
                else:
                    potential_room = potential_room + " " + x

            if len(a.split()) < 5:
                print_line(
                    "You have to input 4 or more words.",
                    "E.g. assign Thomas Marc to living")
            # Capitalizes first character of first and last name so player
            # doesn't have to.
            elif not check_person(a.split()[1], a.split()[2]):
                print_line("This ", a.split()[1], " doesn't exist.")
            elif not check_room(potential_room):
                print_line("This room doesn't exist.")
            elif not check_built_room(potential_room):
                print_line("You haven't built this room yet")
            elif rooms[get_room_index(potential_room)].assigned_limit == \
                    rooms[get_room_index(potential_room)].count_assigned():
                print_line("This room is full.")
                print_line(
                    "You can assign someone in the room to " +
                    "another room to create space.")
            else:
                person_index = get_person_index(
                    a.split()[1].title(),
                    a.split()[2].title())
                people[person_index].assign_to_room(potential_room)

        elif a.split()[0] == "auto":  # All automatic functions
            if a.split()[1] == "assign":
                auto_assign()  # Auto-assigns every free person to a room

        elif a.split()[0] == "upgrade":
            if not check_room(
                    a.split()[1]) or not check_built_room(
                    a.split()[1]):
                print_line("This room doesn't exist. Try again.")
            elif a.split()[1] == "trader":
                print_line("This room cannot be upgraded")
            else:
                # Tempoarily fetches room so it's attributes can be used
                r = rooms[get_room_index(a.split()[1])]
                items_needed = r.components
                for x in range(r.level - 1):
                    for component in items_needed:
                        items_needed.append(component)
                can_up = True
                for ite in all_items:
                    needed = 0
                    for comp in items_needed:
                        if ite == comp:
                            needed += 1
                    # Counts number of component available to the player
                    available = count_item(game, ite, "player")
                    if available < needed:  # Not enough
                        can_up = False
                        print_line(
                            "You don't have enough",
                            ite,
                            "to upgrade your ",
                            r.name)
                        break
                if can_up:
                    for component in items_needed:
                        inventory.remove(component)
                    r.upgrade()
                    print_line(
                        r.name,
                        "has been upgraded and is now level",
                        r.level)

        elif a.split()[0] == "disable":
            if a.split()[1] == "auto_feed":
                # auto_feed = False
                print_line(
                    "Warning. You have disabled the auto_feed feature. " +
                    "Be careful, your people may starve!")
            else:
                print_line(
                    "Invalid input.",
                    "You can disable the 'auto_feed' system.")

        elif a.split()[0] == "enable":
            if a.split()[1] == "auto_feed":
                # auto_feed = True
                print_line("Auto-feed system is working optimally.")
            else:
                print_line(
                    "Invalid Input.",
                    "You can enable the 'auto_feed' system.")

        elif a.split()[0] == "scavenge":
            if a.split()[1] not in people:
                print_line("This person doesn't exist.")
            elif people(a.split()[1]).scavenging:
                print_line("This person is already out scavenging.")
            else:
                cho = input(
                    "Would you like to scavenge for a certain number of " +
                    "days or until their health gets low?(1-100/H) ")
                try:
                    cho = int(cho)
                except:
                    pass
                scavenge(a.split()[1], cho)

        elif a.split()[0] == "heal":
            if a.split()[1] == "all":
                heal_all()
            else:
                if a.split()[1] not in people:
                    print_line("That person doesn't exist.")
                else:
                    stim_count = count_item("stimpack", "player")
                    if stim_count > 0:
                        people(a.split()[1]).heal(heal_amount)
        elif a.split()[0] == "skip":
            global skip
            skip = True
        elif a.split()[0] == "end":
            global player_quit
            confirm = input("Are you sure? All unsaved data will be lost! ")
            confirm = confirm[0].lower()
            if confirm == "y":
                player_quit = True
        elif a.split()[0] == "help":
            print_help()
        else:
            print_line("Invalid Input. Try again.")
    else:
        print_line("You have to choose something!")
"""

if __name__ == '__main__':
    game = None
    if os.path.exists(_save_file):
        load = default_input("Load game from {}? (Y/n) ".format(_save_file))
        if load == "y":
            game = load_game()
    if game is None:
        game = Game()
    game.run()
