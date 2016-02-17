"""Text-based Fallout Shelter game developed by T.G."""

from collections import OrderedDict
from random import randint
import pickle
import sys
import os

from Human import Human, Player, NPC
from Room import Room, all_rooms
from Item import Item, Inventory, all_items

from general_funcs import *


_save_file = "fstb.p"


class Game(object):
    """Main game class."""

    def __init__(self):
        """Initilize main game system."""
        self.setup_player()
        self.all_items = all_items()  # Fetches all items from items.json
        self.all_rooms = all_rooms()  # Fetches all items from rooms.json
        self.inventory = Inventory(self.all_items)
        self.inventory['turret'] += 1
        self.trader_inventory = Inventory(self.all_items)
        self.rooms = {}
        self.people = {}
        self.caps = 100
        self.happiness = 100
        self.action_points = 50
        self.security = "secure"  # Is this the player's job security?
        self.days = 1
        self.actions = OrderedDict()  # [('action': function)]
        self.first_few()
        action_see_people(0,game)
        
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
            "see trader",
            action_see_inventory)
        self.add_action(
            "see rooms",
            action_see_rooms)
        self.add_action(
            "see resources",
            action_see_resources)
        self.add_action(
            "auto assign",
            action_auto_assign)
        self.add_action(
            "trade",
            action_trade)

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
                gender = gender.upper()
                break
            print_line("Invalid gender.")
        self.player = Player(first_name, 0, father, mother, 21, gender)
        
    
    def first_few(self):
        """Create first few inhabitants with random names.
    
        Arguments:
        game -- Main game object
    
        Returns:
        game -- Main game object
        """
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
        for person in self.people:
            used_names.append(person)
            used_names.append(person)
        while len(self.people) < 5:
            num_1 = randint(0, len(names) - 1)
            num_2 = randint(0, len(names) - 1)
            if num_1 == num_2:
                continue
            if names[num_1] in used_names or names[num_2] in used_names:
                continue
            self.people[
                names[num_1] + names[num_2]] = NPC(
                    names[num_1],
                    self.days,
                    names[num_2],
                    "Alena",
                    21,
                    get_gender())
            used_names.append(names[num_1])
            used_names.append(names[num_2])


    def storage_capacity(self):
        """Calculate max inventory capacity of player.

        Returns:
        capacity -- max inventory capacity of player
        """
        capacity = self.rooms["storage"].production
        return capacity

    def run(self, debug=False):
        """Main game. Once all values are initilized, this is run."""
        action_help(self)  # Initially prints the available commands.
        while True and self.player.alive:  # Day loop
            if self.action_points < 50:
                self.action_points += 50
            load_time(100,"A new day dawns. It is now day {} in the vault".format(
                self.days))

            for room in self.rooms:
                if self.inventory['watt'] > room.wattage:
                    resource, production = room.production()
                    self.inventory['watt'] -= room.wattage
                    self.inventory[resource] += production
                else:
                    print_line("Not enough power to operate room: {}".format(
                        room.name))

                if room.rushed:
                    room.rushed = False

            for person in self.people.items():
                person.increase_hunger()
                if person.hunger > 99:
                    person.kill("hunger")
                elif person.hunger > 80:
                    print_line(
                        "Warning! {} is starving and may die soon".format(
                            person))
                elif person.hunger > 50:
                    print_line("{} is hungry".format(person))
                person.increase_thirst()
                if person.thirst > 99:
                    person.kill("thirst")
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

            while self.action_points > 0:  # Choice loop
                a = input("Choose an action: ")
                if len(a) > 0:
                    action, *args = a.split()
                    if action.lower() == "skip":
                        break
                    if a in self.actions.keys():
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


def load_game(noarg=None, save=_save_file):
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
            fast=True)


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
    for room in game.rooms:
        room.print_(game.player)


def action_see_resources(game, *args):
    """See available resources (food, water, and power).

    Arguments:
    game -- Main game object
    """
    print_line("Food * ", game.inventory["food"])
    print_line("Water * ", game.inventory["water"])
    print_line("Power * ", game.inventory["watt"])


# Old print_help function.
''' def print_help():
     """Print list of commands available to player."""
     print_line("""Commands:

     Room actions:
    see rooms           : View all rooms
    build x             : Construct room 'x'
    rush x              : Rush construction of room 'x'
    upgrade x           : Upgrade room 'x'
    fix x               : Fix damaged room 'x'

    Inhabitant actions:
    see people          : View all inhabitants
    feed x              : Feed inhabitant 'x'
    enable auto_feed    : Enable automatically feeding inhabitants
    disable auto_feed   : Disable automatically feeding inhabitants
    coitus x y          : Send inhabitants 'x' and 'y' to the love-house
    scavenge x          : Send inhabitant 'x' to scavenge in the wasteland
    heal x              : Heal inhabitant 'x'
    heal all            : Heal all inhabitants
    assign x y          : Assign inhabitant 'x' to room 'y'
    auto assign         : Automatically assign unassigned inhabitants to room

    Inventory actions:
    see items           : View all held items
    scrap x             : Destroy item and add components to your inventory
    trade               : Begin trading interaction

    Other actions:
    skip                : Skip current day
    see day             : View day number
    see resources       : View all resources available
    end                 : Quit game
    help                : See this help text
    """, fast=True)
'''


def living_capacity(game):
    """Get maximum inhabitant capacity of shelter.

    Arguments:
    game -- main game object

    Returns:
    int -- maximum capacity of shelter
    """
    room = game.room
    print_line("Maximum number of inhabitants", 5 * room.level)
    return (5 * room.level)


# Construction system:

def build(game, room):
    """Build room specified.

    Arguments:
    game -- Main game object
    room -- name of room to build

    Returns:
    game -- Main game object
    """
    built_room = Room(str(r), player)  # creates a room.
    game.rooms.append(built_room)  # Stores the room in memory.
    load_time(5, "Building " + r)
    for y in built_room.components:  # Does this for each component
        for x in game.inventory:
            if y == x:  # If it matches, delete this.
                Item(x).destroy("player")
                # Ensures that only one instance of the item is removed for
                # every one instance of the component.
                break
    game.player.gain_xp(100)
    use_points(10)
    return game


def craft(game, item):
    """Craft specified item.

    Arguments:
    game -- Main game object
    item -- item to craft

    Returns:
    game -- Main game object
    """
    load_time(5, ("Crafting ", x))
    add_to_inven(x, 1, "player")
    # Perk bonuses
    a = Item(x)
    for l in range(0, 5):
        if game.player.crafting == l:
            chance = l * 2
            break
    for y in a.components:
        for x in game.inventory:
            if y == x:
                chance_game = randint(0, 101)
                if chance_game > chance:
                    game.inventory[x] -= 1
                break
    game.player.gain_xp(a.rarity * 10)
    use_points(5)
    return game


# Human management system:

def get_player_gender():
    """Ask player what gender they are.

    Returns:
    char -- 'm' or 'f'
    """
    gender = input("Please choose a gender(M/F): ")
    if len(gender) > 0:
        gender = gender[0].lower()
        if gender == "m" or gender == "f":
            return gender
        else:
            print_line("Invalid gender choice!")
            get_player_gender()
    else:
        print_line("No input detected!")
        get_player_gender()


def get_gender():
    """Randomly generate gender for NPC.

    Returns:
    char -- 'm' or 'f'
    """
    if randint(0, 1) == 0:
        return "m"
    else:
        return "f"


def check_person(game, first_name, last_name):
    """Check if inhabitant exists in list of all inhabitants.

    Arguments:
    game -- Main game object
    first_name -- first name of inhabitant to check
    surname -- surname of inhabitant to check

    Returns:
    bool -- whether inhabitant exists or not
    """
    for per in people:
        if per.name == first_name.title() \
                and per.surname == surname.title():
            return True
    else:
        return False


def gain_xp(game, person_name, amount):
    """Add experience to Human.

    Arguments:
    game -- Main game object
    person_name -- name of person to gain experience
    amount -- amount of experience to add

    Returns:
    game -- with one more experienced person
    """
    person = game.people[person_name]
    person.XP += amount


def check_xp(game, person_name):
    """Check experience of inhabitant.

    Arguments:
    game -- Main game object
    person_name -- name of person

    Returns:
    bool -- Whether inhabitant can level up
    """
    person = game.people[str(person_name)]
    # Xp needed to level up increases exponentially
    xp_needed = 100 + (3**person.level)
    if person.XP + 1 > xp_needed:
        person = level_up(person)
    return game


def level_up(person):
    """Level up Human and ask player for input on what stat to level up.

    Arguments:
    person -- Person object at level x

    Returns:
    person -- Person object at level x+1
    """
    see_stats(person)
    if isinstance(person, Player):  # If player has leveled up
        print_line("\n")
        done = False
        while done is False:
            done = True
            choice = input("Please choose an attribute to level up: ").lower()
            if choice == "strength":
                person.strength += 1
            elif choice == "perception":
                person.perception += 1
            elif choice == "endurance":
                person.endurance += 1
            elif choice == "charisma":
                person.charisma += 1
            elif choice == "intelligence":
                person.intelligence += 1
            elif choice == "luck":
                person.luck += 1
            elif choice == "medic":
                person.medic += 1
            elif choice == "crafting":
                person.crafting += 1
            elif choice == "tactitian":
                person.tactitian += 1
            elif choice == "cooking":
                person.cooking += 1
            elif choice == "inspiration":
                person.inspiration += 1
            elif choice == "scrapper":
                person.scrapper += 1
            elif choice == "barter":
                person.barter += 1
            elif choice == "electrician":
                person.electrician += 1
            else:
                print_line("Invalid choice")
                done = False


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
            if name not in used_names:
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
                # Next few lines need some work.
                parent_1.children.append(str(name + " " + parent_1_surname))
                parent_2.children.append(str(name + " " + parent_1_surname))
                parent_1.partner = parent_2.name + " " + parent_2.surname
                parent_2.partner = parent_1.name + " " + parent_1.surname
                see_people()
                update_all_assignment()
                if days > 2:  # First few births cost no points
                    use_points(50)
                player.gain_xp(100)
                use_points(25)
                used_names.append(name)
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
        elif gender not in ("m", "f"):
            print_line("Invalid input. Only accepts 'm' or 'f'.")
        else:
            gender = gender.lower()
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
    for person in game.people.values():
        if person.assigned_room == "":
            for room in game.rooms:
                if room.count_assigned() < room.assigned_limit:
                    person.assign_to_room(r.name)
                    break


def update_all_assignment(game):  # Need to scrap this
    """Increase length of assignment variable.

    Arguments:
    game -- Main game object
    """
    for r in game.rooms:
        current_count = len(r.assigned)  # Count's how many digits exist
        # print_line("This many digits exist",current_count)
        required_count = len(people)  # Count's how many digits should exists
        # print_line("How many are needed",required_count)
        if current_count < required_count:
            difference = required_count - current_count
            lst = []
            for letter in r.assigned:
                lst.append(letter)
            for x in range(difference):
                lst.append('0')
            final = ''
            for letter in lst:
                final = final + letter
            # print_line("We're adding this to the assigned",final)
            r.assigned = r.assigned + final
            # print_line("This is what happened", r.assigned)


# Room Management system:

def get_room_index(room):  # Shouldnt'need this function anymore
    """Get index of room in room list.

    Arguments:
    room -- room to get index of

    Returns:
    r -- index of room
    """
    room = str(room)
    for r in range(len(rooms)):
        # print_line("Room index scan is now",r)
        if rooms[r].name == room:
            # print_line("Room index fetch returns,",r)
            return r


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


def can_use_power(room):
    """
    Determine whether the room may use power or not.

    Arguments:
    room - room which uses power

    Returns:
    bool -- whether room may use power
    """
    if count_item('watt', 'player') > room.power_usage:
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


def find_rand_item(game, inven, num):
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
        num = randint(1, 1024)  # More likely to find common items than rare.
        lst = [2**a for a in range(0, 11)]
        count = 0
        for chance in lst:
            if num < chance:
                break
            count += 1
        # Determines the rarity of an item. 50% chance it's a level 10,
        # 25% chance it's a level 9, 12.5% chance it's a level 8 and so on.
        rar = 10 - count
        # Stores each item if the rarity level matches what was randomly picked
        possible_items = []
        for x in game.all_items:
            if Item(x).rarity == rar:
                possible_items.append(x)
        if len(possible_items) > 0:
            number = randint(0, len(possible_items) - 1)
            actual_item = possible_items[number]
            # Following lines actually store the item in memory
            if target_inventory == "player" or target_inventory == "trader":
                if target_inventory == "player":
                    game = add_to_inven(game, actual_item, 1, 'inventory')
                elif target_inventory == "trader":
                    game = add_to_inven(game, actual_item, 1, 'trader')
            else:
                print_line("Bug with random item system. Please contact dev!")
    return game


def add_to_inven(game, item, number, inven):
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
            pass  # Need to add to inven dict
    elif inven == "trader":
        for y in range(number):
            pass  # Same as previous comment
    return game


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
            # rand_number = randint(0, len(trader_inventory) - 1)
            pass  # Need to remove an item at index rand_number
    elif inven == "player":
        pass  # Need to remove from player's inventory
    else:
        print_line("Major bug in item losing system. Please contact dev!")


def action_scrap(game, it):
    """Scrap item and recieve its components.

    Arguments:
    game -- main game object
    it -- item to scrap

    Returns:
    game -- with the item removed and it's components added to the
    """
    if it not in all_items:
        print_line(
            "Bug with item scrapping system.",
            "Invalid argument passes to function. Please contact dev.")
    else:
        game.inventory[it] -= 1
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


def update_defense(player):
    """Update defense of shelter based on guns and turrets in inventory."""
    global defense
    defense = 0
    turret_count = count_item("turret", "player")
    defense += 10 * turret_count
    gun_count = count_item("gun", "player")
    defense += gun_count
    # Add cases for more items that increase defense
    strength_sum = 0
    for person in people:
        strength_sum += person.strength
    defense += strength_sum
    if player.tactician > 0:
        defense = defense * (1 + (player.tactician * 0.05))
    if player.inspiration > 0:
        defense = defense * (1 + (player.inspiration * 0.03))


# Happiness System:

def avg_hunger():
    """Calculate average hunger level of all inhabitants.

    Returns:
    avg -- average hunger level
    """
    total = 0
    for x in people:
        total += x.hunger
    avg = total // len(people)
    return avg


def avg_thirst():
    """Calculate average thirst level of all inhabitants.

    Returns:
    avg -- average thirst level
    """
    total = 0
    for x in people:
        total += x.thirst
    avg = total // len(people)
    return avg


def feed(first_name, surname, amount):
    """Reduce hunger level of inhabitant.

    Arguments:
    first_name -- first name of inhabitant to feed
    surname -- surname of inhabitant to feed
    amount -- how much to feed inhabitant
    """
    global people
    global inventory
    person = people[get_person_index(first_name, surname)]
    person.hunger -= amount * 10
    if person.hunger < 0:
        person.hunger = 0
    Item('food').destroy('player')


def drink(first_name, surname, amount):
    """Reduce thirst level of inhabitant.

    Arguments:
    first_name -- first name of inhabitant to feed
    surname -- surname of inhabitant to feed
    amount -- how much to feed inhabitant
    """
    global inventory
    global people
    person = people[get_person_index(first_name, surname)]
    person.thirst -= amount
    if person.thirst < 0:
        person.thirst = 0
    Item('water').destroy('player')


def auto_feed_all():
    """Automatically feed all inhabitants."""
    global people
    food_count = count_item("food", "player")
    water_count = count_item("water", "player")
    load_time(200, "Feeding all inhabitants.")
    while food_count > 0 and avg_hunger() > 2:
        for person in people:
            feed(person.name, person.surname, 1)
            food_count -= 1
    while water_count > 0 and avg_thirst() > 2:
        for person in people:
            drink(person.name, person.surname, 1)
            water_count -= 1


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


# Action Point usage system:

def use_points(game, point):
    """Remove action points from total.

    Arguments:
    game -- main game object
    point -- how many points to remove
    """
    if point > 50:
        print_line(
            "Bug with point usage system. ",
            "It's trying to use more than 50, " +
            "please note this and contact dev.")
    else:
        usage = game.action_points - point
        game.overuse = False
        if usage < 0:  # If overuse occurs. i.e. if overuse is negative
            # overuse_amount = 0 - usage
            game.overuse = True
        else:  # If normal usage occurs.
            # action_points -= usage
            pass

# Trading system:


def action_trade(game):
    """Trading system."""
    load_time(100, "Initializing trading system.")
    while True:
        print_line("")
        print_line("Here are the traders' items: ")
        action_see_inventory(game, "trader")
        print_line("\nThe trader has ", game.trader_caps, " caps.")

        print_line("\nHere are your items: ")
        action_see_inventory(game, "player")
        print_line("\nYou have ", game.caps, " caps.")

        print_line(
            "\nFor instance, input (buy 5 food) if you want to buy 5 " +
            "units of food. Or input (end) to stop trading.")
        a = input("What trade would you like to make? ")
        if len(a) < 1:
            print_line("You have to input something")
            continue

        # Following lines are checks.
        let_trade = False
        if len(a.split()) != 3:
            if len(a.split()) == 2:  # a is in the form (buy x) or (sell x)
                if a.split()[1] in game.all_items:
                    if a.split()[0] == "buy" or a.split()[0] == "sell":
                        a = "%s %s %s" % (a.split()[0], 1, a.split()[1]) #Set's a to (buy 1 wood) if player inputs buy wood.
                        let_trade = True
                    else:
                        print_line("Invalid input. You can (buy) or (sell)")
                else:
                    print_line("This item doesn't exist")
            elif a.split()[0] == 'end' or a.split()[0] == 'stop':
                break
            else:
                print_line("You have to input 3 words. Buy/sell,amount,item")
        elif len(a.split()) == 3:
            if a.split()[0].lower() not in ("buy","sell"):
                print_line("Invalid input. You can only (buy) and (sell)")
                let_trade = False
            if a.split()[2] not in game.all_items():
                print_line("This item doesn't exist.")
                let_trade = False
            try:
                int(a.split()[1])
            except ValueError:
                print_line("You have to input a number as the second word")
                    let_trade = False
             
        if let_trade:  # Messy conditional routine coming up.
            # Fetches cost of item by tempoarily creating it's object
            # and retreiving it's value attribute
            cost = Item(a.split()[2]).value
            # Sums up the money that is exchanging hands
            total_cost = cost * int(a.split()[1])
            print_line("Cost of all items:", total_cost)
            if a.split()[0].lower() == "buy":
                # Adjusts the prices, depending on player's bartering level.
                for x in range(0, 4):
                    total_cost = int(total_cost * (1.2 - (x * 0.05)))
                if total_cost > game.caps:
                    print_line("You can't afford that!")
                else:
                    count = count_item(a.split()[2], "trader")
                    if int(a.split()[1]) > count: #If trader doesn't have enough.
                        if count < 1:
                            print_line(
                                "The trader doesn't have any " +
                                a.split()[2])
                        else:
                            print_line(
                                "The trader doesn't have ",
                                a.split()[1],
                                " of ",
                                a.split()[2])
                    else:
                        for x in range(int(a.split()[1])):
                            game.trader_inventory[a.split()[2]] -= 1
                            game.inventory[a.split()[2]] += 1
                        game.caps -= total_cost
                        game.trader_caps += total_cost
            elif a.split()[0].lower() == "sell":
                # Adjusts the prices, depending on bartering level.
                for x in range(0, 4):
                    total_cost = int(total_cost * (0.8 + (x * 0.05)))
                if total_cost > game.trader_caps:
                    print_line("The trader can't afford that!")
                else:
                    count = count_item(a.split()[2], "player")
                    if int(a.split()[1]) > count: #If player doesn't have enough of the item to sell.
                        if count < 1:
                            print_line(
                                "You don't have any " +
                                a.split()[2])
                        else:
                            print_line(
                                "You don't have " + int(a.split()[1]) +
                                " of ", a.split()[2])
                    else:
                        for x in range(int(a.split()[1])):
                            game.inventory[a.split()[2]] -= 1
                            game.trader_inventory[a.split()[2]] += 1
                        game.caps += total_cost
                        game.trader_caps -= total_cost

    print_line("Ending trade")
    return game


def choice():  # Need to move these commands into Game() class
    """Choice/Command input system."""
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
                                count_item(component, "player"):
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
                            number_available = count_item(component, "player")
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
                    count = count_item(str(a.split()[1]), "player")
                    if count > 0:
                        scrap(a.split()[1])
                    else:
                        print_line("You don't have that item.")
            elif len(a.split()) == 3:  # Scrap multiple times
                if a.split()[1] in range(1, 100):
                    if a.split()[2] in all_items:
                        count = count_item(str(a.split()[1]), "player")
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
                        available = count_item(it, 'player')
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

        elif a.split()[0] == "auto":  # All automaticf functions
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
                    available = count_item(ite, "player")
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

if __name__ == '__main__':
    game = None
    if os.path.exists(_save_file):
        load = default_input("Load game from {}? (Y/n) ".format(_save_file))
        if load == "y":
            game = load_game()
    if game is None:
        game = Game()
    game.run()
