# Text-based Fallout Shelter game developed by T.G.
from random import randint  # Used for random choosing of values ( E.g. names)
from time import sleep  # Used to space out prints and create Fake loading times
from tqdm import tqdm  # Used to make loading screens.

from Human import Human
from Room import Room
from Item import Item


# Information system!
# Bunch of functions used by other functions to retrieve information about
# the shelter, it's assigned, rooms and items.
# If this is 1, loading screens are activated. If 0, no loading screens.
load = 0


# This is a fake loading screen. There's no loading happening, just
# improves pacing of the game.
def load_time(x, message):
    if load == 1:
        print(str(message))
        for x in tqdm(range(0, x)):
            sleep(0.01)
    else:
        print(str(message))
        sleep(x / 10000)


# Whenever player has to input an integer, this should be used. Catches errors.
def input_int(s):
    while True:
        try:
            x = int(input(s))
        except:
            print("Invalid. Only integer numbers are accepted!")
    return x


# Counts total number of an item present in an inventory
def count_item(item, target_inventory):
    item = str(item)
    if target_inventory == "player":
        return inventory.count(item)
    elif target_inventory == "trader":
        return trader_inventory.count(item)
    else:
        print("Bug with item counting system. Please contact dev!")


def count_weight():  # Calculates the sum of the weights of all items currently in the inventory,
    count = 0
    for x in inventory:
        # Creates instances of class on the fly. If 5 wood present, tempoarily
        # creates 5 wood, one by one, uses their weight and discards them
        count += Item(x).weight
    return count


# Calculates how much weight player can store.  Used to check if player
# can take any more items.
def storage_capacity(all_rooms):
    capacity = all_rooms("storage").production
    return capacity


def check_room(x):  # Checks if the room exists
    if x in all_rooms:
        return True
    return False


def check_built_room(x):  # Checks if room has been built yet
    for r in rooms:
        if x == r.name:
            return True
    return False


def see_people():  # Displays everyone in the shelter.
    for person in people:
        print(person.name, person.surname)
        print(
            "    Age:",
            person.age,
            " Gender:",
            (person.gender).upper(),
            " Hunger:",
            person.hunger,
            " Thirst:",
            person.thirst,
            " Room:",
            person.assigned_room)


def see_rooms():
    print("")
    for r in rooms:
        for word in r.name.split():
            print(word[0].upper() + word[1:], end=" ") #Capitlaizes the first letter of the name and print's it out.
        if r.can_produce == 1: 
            r.update_production() #To get the most up-to-date data on it's production.
            print(
                "\n    Risk:",
                r.risk * 10,
                "%  Level:",
                r.level,
                "  Power:",
                r.power_available,
                "  Production:",
                r.production)
        else:
            print(
                "\n    Risk:",
                r.risk,
                "  Level:",
                r.level,
                "  Power:",
                r.power_available)

        # Only rooms that can produce have assignments, with the exception
        # of the trader.
        if r.can_produce == 1 or r.name == "trader":
            r.see_assigned()


# Displays all items in inventory in the form
# (Log*5.Weight=5.Value=10.Components="Wood". Rarity=1).
def see_inventory(inven):
    inven = str(inven)
    # Stores item types already seen, so if 5 units of wood are present, they
    # are all shown in bulk in one go, instead of each one individualy.
    seen_items = []
    if inven == "player":
        for x in inventory:
            if x not in seen_items:
                count = count_item(x, "player")
                if count > 0:  # If there are no instances of the item present, no need to display it.
                    # Creates a tempoary object so it's data can be fetched.
                    it = Item(x)
                    print(
                        x,
                        "*",
                        count,
                        ". Weight: ",
                        it.weight,
                        ". Value: ",
                        it.value,
                        ". Components: ",
                        it.components,
                        ". Rarity: ",
                        it.rarity)
                    seen_items.append(x)
    elif inven == "trader":
        for x in trader_inventory:
            if x not in seen_items:
                count = count_item(x, "trader")
                if count > 0:  # If there are no instances of the item present, no need to display it.
                    it = Item(x)
                    print(
                        x,
                        "*",
                        count,
                        ". Weight: ",
                        it.weight,
                        ". Value: ",
                        it.value,
                        ". Components: ",
                        it.components,
                        ". Rarity: ",
                        it.rarity)
                    seen_items.append(x)
    else:
        print("Major bug with inventory information system. Please contact dev!")


# Returns maximum number of inhabitants that can exist in the shelter,
# depending on the level of the living room.
def living_capacity():
    room = rooms[get_room_index('living')]
    print("Maximum number of inhabitants", 5 * room.level)
    return (5 * room.level)


def see_resources():
    print("Food * ", count_item("food", "player"))
    print("Water * ", count_item("water", "player"))
    print("Power * ", count_item("watt", "player"))


def get_person_index(first_name, surname):
    for x in range(len(people)):
        if people[x].name == first_name[0].upper(
        ) + first_name[1:] and people[x].surname == surname[0].upper() + surname[1:]:
            return x


def get_room_index(room):
    room = str(room)
    for r in range(0, len(rooms)):
        #print("Room index scan is now",r)
        if rooms[r].name == room:
            #print("Room index fetch returns,",r)
            return int(r)


# Scavenging system.
# Sends people on a scavenging mission.
def scavenge(first_name, surname, var=None):
    global people
    if not check_person(first_name, surname):
        print("Error with scavenging system. Please contact dev!")
    else:
        person = people[get_person_index(first_name, surname)]
        person.scavenging = 1
        if var == "days":  # If player chooses to send player for certain number of days, or until health drops below 20.
            day_choice = input_int("How many days do you want to send this person out?")
            person.days_to_scavenge_for = day_choice
        else:
            # Their health will drop below 20 before 100 days, so this is fine.
            person.days_to_scavenge_for = 100
    use_points(10)


# Construction system.
# Builds a room once checks are done. Should append to (rooms) list.
def build(r):
    global rooms
    global inventory
    built_room = Room(str(r))  # creates a room.
    rooms.append(built_room)  # Stores the room in memory.
    load_time(5, ("Building ", r))
    for y in built_room.components:  # Does this for each component
        for x in inventory:
            if y == x:  # If it matches, delete this.
                Item(x).destroy("player")
                # Ensures that only one instance of the item is removed for
                # every one instance of the component.
                break
    people[0].gain_xp(100)
    use_points(10)


# Crafts an item once checks are done. Just adds the name of an item to the
# inventory list.
def craft(x):
    global inventory
    load_time(5, ("Crafting ", x))
    add_to_inven(x, 1, "player")
    # Perk bonuses
    a = Item(x) 
    for l in range(0, 5):
        if people[0].crafting == l:
            chance = l * 2
            break
    for y in a.components:
        for x in inventory:
            if y == x:
                chance_game = randint(0, 101)
                if chance_game > chance:
                    inventory.remove(x)
                break # Ensures that only one instance of the item is referenced.
    people[0].gain_xp(a.rarity * 10)
    use_points(5)


# Human management system
def get_player_gender():  # Asks player what gender they are.
    gender = input("Please choose a gender(M/F): ")
    if len(gender) > 0:
        gender = gender[0].lower()
        if gender == "m" or gender == "f":
            return gender
        else:
            print("Invalid gender choice!")
            get_player_gender()
    else:
        print("No input detected!")
        get_player_gender()


def get_gender():  # Randomly generates a gender. For NPCs
    if randint(0, 1) == 0:
        return "m"
    else:
        return "f"


def check_person(first_name, surname):  # Check if a person exists.
    for per in people:
        if per.name == first_name[0].upper() + first_name[1:] 
        and per.surname == surname[0].upper() + surname[1:]:
            return True
    else:
        return False


def check_xp(name, surname):
    global people
    # Fetches index of person in the people list.
    person_index = get_person_index(name, surname)
    # Fetches person object and stores it locally. So now (person) is a
    # shortcut to the person.
    person = people[person_index]
    # Xp needed to level up increases exponentially
    xp_needed = 1000 + (3**person.level)
    if person.XP + 1 > xp_needed:
        print(person.name, " has", person.XP, " XP")
        print(person.name, " has leveled up")
        person.level_up()
        print(person.name, "  is now level ", person.level)


# Creates new character.
def birth(
        parent_1_first_name,
        parent_1_surname,
        parent_2_first_name,
        parent_2_surname):
    global people
    name = input("Choose a first name for the new child: ")
    if len(name.split()) == 1:  # Player can only input one word
        if name not in used_names:
            # Capitalizes first letter_
            name = name[0].upper() + name[1:]
            parent_1 = people[
                get_person_index(
                    parent_1_first_name,
                    parent_1_surname)]
            parent_2 = people[
                get_person_index(
                    parent_2_first_name,
                    parent_2_surname)]
            if parent_2.gender == "m":
                parent_1, parent_2 = parent_2, parent_1
            people.append(
                Human(
                    name,
                    day_count,
                    parent_1.surname,
                    parent_2.surname,
                    get_gender()))
            # Following lines let parent's know about their children and their
            # partners.
            parent_1.children.append(str(name + " " + parent_1_surname))
            parent_2.children.append(str(name + " " + parent_1_surname))
            parent_1.partner = parent_2.name + " " + parent_2.surname
            parent_2.partner = parent_1.name + " " + parent_1.surname
            see_people()
            update_all_assignment()
            if day_count > 2:  # First few births cost no points
                use_points(50)
            people[0].gain_xp(100)
            use_points(25)
            used_names.append(name)
            load_time(5, (name, " is being born!"))
        else:
            print("Someone already has that name.")
            birth(
                parent_1_first_name,
                parent_1_surname,
                parent_2_first_name,
                parent_2_surname)
    else:
        print("You have to input a single word!")
        birth(
            parent_1_first_name,
            parent_1_surname,
            parent_2_first_name,
            parent_2_surname)


def first_few():  # Runs once at beginning of game. Creates 4 new people. Costs no Action Points!
    global people
    global used_names
    global rooms
    global used_names
    # Random names for inital 5 inhabitants. All children will inherit their
    # surnames from their parents.if day_count<2: #Initial 5 inhabitants need
    # to be birthed
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
    for person in people:
        used_names.append(person.name)
        used_names.append(person.surname)
    while len(people) < 8:
        num_1 = randint(0, len(names) - 1)
        num_2 = randint(0, len(names) - 1)
        if num_1 == num_2:  # People can't have the same surname and first name.
            continue
        if names[num_1] in used_names or names[num_2] in used_names:
            continue
        # First few inhabitants all have the same mother.
        people.append(
            Human(
                names[num_1],
                day_count,
                names[num_2],
                "Alena",
                get_gender()))
        used_names.append(names[num_1])
        used_names.append(names[num_2])


# Only ran at start of game. First inhabitant of vault should be the player.
def create_player():
    global people
    name = input("Choose a first name for yourself: ")
    if len(name) > 0:
        name = name[0].upper() + name[1:len(name)]
        if len(name.split()) == 1:
            parent_1 = input("What is the surname of your father?")
            if len(parent_1.split()) == 1:
                parent_1 = parent_1[0].upper() + parent_1[1:len(parent_1)]
                parent_2 = input("What is the surname of your mother?")
                if len(parent_2.split()) == 1:
                    parent_2 = parent_2[0].upper() + parent_2[2:len(parent_2)]
                    people.append(
                        Human(
                            name,
                            day_count,
                            parent_1,
                            parent_2,
                            get_player_gender()))
                else:
                    print("Only single word inputs are accepted.")
                    create_player()
            else:
                print("Only single word inputs are accepted.")
                create_player()
        else:
            print("Only single word inputs are accepted.")
            create_player()
    else:
        print("You need a name!")
        create_player()


def update_all_assignment():
    global rooms
    for r in rooms:
        current_count = len(r.assigned)  # Count's how many digits exist
        #print("This many digits exist",current_count)
        required_count = len(people)  # Count's how many digits should exists
        #print("How many are needed",required_count)
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
            #print("We're adding this to the assigned",final)
            r.assigned = r.assigned + final
            #print("This is what happened", r.assigned)


def power_usage():  # Returns the total power needed by every room in the game.
    total = 0
    for r in rooms:
        total += r.power_usage
    return total


def power_production():
    total = 0
    generator = rooms[get_room_index('generator')]
    for x in range(0, generator.production):
        total += x
    return total


def auto_assign():  # Automatically assigns free inhabitants to rooms
    global people
    global rooms
    for person in people:
        if person.assigned_room == "":
            for r in rooms:
                if r.count_assigned() < r.assigned_limit:
                    person.assign_to_room(r.name)
                    break


def see_stats(first_name, surname):
    person = people[get_person_index(first_name, surname)]
    print("Strength: ", person.strength)
    print("Perception: ", person.perception)
    print("Endurance: ", person.endurance)
    print("Charisma: ", person.charisma)
    print("Intelligence: ", person.intelligence)
    print("Luck: ", person.luck)
    if person.name == people[0].name:  # Player has extra stats
        print("")
        print("Medic: ", person.medic)
        print("Crafting: ", person.crafting)
        print("Tactician: ", person.tactician)
        print("Cooking: ", person.cooking)
        print("Inspiration: ", person.inspiration)
        print("Scrapping: ", person.scrapper)
        print("Bartering: ", person.barter)
        print("Electricain: ", person.electrician)


# Inventory managment system!
def rand_item(target_inventory):
    # Following lines randomly choose an item, based on rarity
    num = randint(1, 1024)
    lst = [2**a for a in range(0, 11)]
    count = 0
    for chance in lst:
        if num < chance:
            break
        count += 1
    # Determines the rarity of an item. 50% chance it's a level 10, 25% chance
    # it's a level 9, 12.5% chance it's a level 8 and so on.
    rar = 10 - count
    # Stores each item if the rarity level matches what was randomly picked.
    possible_items = []
    for x in all_items:
        if Item(x).rarity == rar:
            possible_items.append(x)
    if len(possible_items) > 0:
        number = randint(0, len(possible_items) - 1)
        actual_item = possible_items[number]
        #print("Randomly adding",actual_item,"to",target_inventory,"inventory")
        # Following lines actually store the item in memory
        if target_inventory == "player":
            add_to_inven(actual_item, 1, 'inventory')
        elif target_inventory == "trader":
            add_to_inven(actual_item, 1, 'trader')
        else:
            print("Bug with random item system. Please contact dev!")


# Finds x items randomly and adds it to an inventory.
def find_rand_item(inven, times):
    for x in range(0, times + 1):
        rand_item(inven)  # passes iven to rand_item function


# Adds (x) (number) times to (inven) inventory. E.g. wood,5,player
def add_to_inven(x, number, inven):
    global trader_inventory
    global inventory
    x = str(x)
    inven = str(inven)
    if x not in all_items:
        # Should never happen, since all checks should be done before this
        # function is called.
        print("Item doesn't exist in the game's databases. Major bug with inventory adding system. Please contact dev")
    else:
        if inven == "player":
            for y in range(number):
                inventory.append(x)
        elif inven == "trader":
            for y in range(number):
                trader_inventory.append(x)


def lose_items(inven, number):  # Randomly deletes multiple items from the target_inventory
    global inventory
    global trader_inventory
    if inven == "trader":  # Runs daily. Simulates trader selling some items to NPCs.
        for x in range(number):
            rand_number = randint(0, len(trader_inventory) - 1)
            trader_inventory.remove(trader_inventory[rand_number])
    elif inven == "player":  # Only runs when shelter has been raided by a hostile force.
        print("The raid made off with these items!")
        for x in range(number):
            rand_number = randint(0, len(inventory) - 1)
            e = iventory[rand_number]
            print(inventory[e])
            inventory.remove(inventory[e])
    else:
        print("Major bug in item losing system. Please contact dev!")


def scrap(it):
    global inventory
    if it not in all_items:
        print("Bug with item scrapping system. Invalid argument passes to function. Please contact dev.")
    else:
        for item in inventory:
            if item == it:
                Item(it).scrap()
                load_time(300, ("Scrapping " + str(it)))
                people[0].gain_xp((Item(it).rarity) * 10)
                break
    use_points(2)


# Raiding system.
def raid():
    global people
    update_defense()
    raiders = ["Super Mutant", "Raider", "Synth", "Feral Ghoul"]
    raider_index = randint(0, len(raiders))
    raider = raiders[raider_index]  # Randomly chooses a raider party.
    increasing_attack = day_count // 5
    attack_power = randint(1, increasing_attack)
    load_time(10, ("There was a " + raider + " raid on your shelter!"))
    print("The total enemy power was", attack_power)
    print("Your total defenses are", defense)
    if defense > attack_power:
        print("Your defenses were strong enough to send them packing!")
    else:
        loss = attack_power - defense
        lose_items("player", loss)
        if loss > 10:
            death_chance = loss // 10
            dice = randint(2, 25)
            if death_chance < dice:
                # Death
                # The player can't die in a raid!
                possible_deaths = people[1, len(people) - 1]
                death_number = randint(len(possible_deaths))
                print(
                    possible_deaths[death_number],
                    " has been killed in a raid")
                possible_deaths[death_number].die()
    for person in people:
        person.gain_xp(attack_power * 10)
    use_points(30)


# Updates the defense rating of the shelter, according to the presence of
# defensive items.
def update_defense():
    global defense
    player = people[0]
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


# Happiness System.
def avg_hunger():  # Calculates average hunger level.
    total = 0
    for x in people:
        total += x.hunger
    avg = total // len(people)
    return avg


def avg_thirst():  # Calculates average thirst level
    total = 0
    for x in people:
        total += x.thirst
    avg = total // len(people)
    return avg


def feed(first_name, surname, amount):  # Reduces the hunger level of a person.
    # This needs to reduce the thirst level aswell.
    global people
    global inventory
    person = people[get_person_index(first_name, surname)]
    person.hunger -= amount * 10
    if person.hunger < 0:
        person.hunger = 0
    Item('food').destroy('player')


def drink(first_name, surname, amount):
    global inventory
    global people
    person = people[get_person_index(first_name, surname)]
    person.thirst -= amount
    if person.thirst < 0:
        person.thirst = 0
    Item('water').destroy('player')


def auto_feed_all():
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


# Depending on hunger or thirst level, reduces general happiness level.
def happiness_loss():
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
        print(
            "Due to your inhabitants being hungry and/or thirsty the shelter's overall happiness has dropped to ",
            happiness)


# Action Point usage system.
def use_points(point):
    global AP
    global overuse
    global overuse_amount
    if point > 50:
        print("Bug with point usage system. It's trying to use more than 50, please note this and contact dev.")
    else:
        usage = AP - point
        overuse = 0
        if usage < 0:  # If overuse occurs. i.e. if overuse is negative
            overuse_amount = 0 - usage
            overuse = 1
        else:  # If normal usage occurs.
            AP = AP - usage


# Trading system.
def trade():  # Trading system. Uses no Action Points
    load_time(100, "Initializing trading system.")
    global inventory
    global trader_inventory
    global caps
    global trader_caps
    barter = people[0].barter
    stop_trade = 0
    while stop_trade == 0:  # "continue" lets trading go on , "break" stops trading
        print("")
        print("Here are the traders' items: ")
        see_inventory("trader")
        print("\nThe trader has ", trader_caps, " caps.")

        print("\nHere are your items: ")
        see_inventory("player")
        print("\nYou have ", caps, " caps.")

        print("\nFor instance, input (buy 5 food) if you want to buy 5 units of food. Or input (end) to stop trading.")
        a = input("What trade would you like to make? ")
        if len(a) < 1:
            print("You have to input something")
            continue

        # Following lines are checks.
        let_trade = 0
        if len(a.split()) != 3:
            if len(a.split()) == 2:  # a is in the form (buy x) or (sell x)
                if a.split()[1] in all_items:
                    if a.split()[0] == "buy" or a.split()[0] == "sell":
                        a = "%s %s %s" % (a.split()[0], 1, a.split()[1])
                        let_trade = 1
                    else:
                        print("Invalid input. You can (buy) or (sell)")
                else:
                    print("This item doesn't exist")
            elif a.split()[0] == 'end' or a.split()[0] == 'stop':
                stop_trade = 1
            else:
                print("You have to input 3 words. Buy/sell,amount,item")
        elif len(a.split()) == 3:
            let_trade = 1
        if let_trade == 1:  # Messy conditional routine coming up.
            if a.split()[2] in all_items:
                check = 1
                try:
                    a.split()[1] = int(a.split()[1])
                except ValueError:
                    print("You have to input a number as the second word")
                    check = 0
                if check == 1:
                    # Fetches cost of item by tempoarily creating it's object
                    # and retreiving it's value attribute
                    cost = Item(a.split()[2]).value
                    print("Cost of one item", cost)
                    # Sums up the money that is exchanging hands
                    total_cost = cost * int(a.split()[1])
                    print("Cost of all item", total_cost)
                    a.split()[0] == a.split()[0].lower()
                    if a.split()[0] == "buy":
                        # Adjusts the prices, depending on bartering level.
                        for x in range(0, 4):
                            total_cost = int(total_cost * (1.2 - (x * 0.05)))
                        if total_cost > caps:
                            print("You can't afford that!")
                        else:
                            count = count_item(a.split()[2], "trader")
                            if int(a.split()[1]) > count:
                                if count == 0:
                                    print(
                                        "The trader doesn't have any ", a.split()[2])
                                else:
                                    print(
                                        "The trader doesn't have ",
                                        a.split()[1],
                                        " of ",
                                        a.split()[2])
                            else:
                                for x in range(int(a.split()[1])):
                                    trader_inventory.remove(str(a.split()[2]))
                                    inventory.append(a.split()[2])
                                caps -= total_cost
                                trader_caps += total_cost
                    elif a.split()[0] == "sell":
                        # Adjusts the prices, depending on bartering level.
                        for x in range(0, 4):
                            total_cost = int(total_cost * (0.8 + (x * 0.05)))
                        if total_cost > trader_caps:
                            print("The trader can't afford that!")
                        else:
                            count = count_item(a.split()[2], "player")
                            if int(a.split()[1]) > count:
                                if count == 0:
                                    print("You don't have any ", a.split()[2])
                                else:
                                    print(
                                        "You don't have ", int(
                                            a.split()[1]), " of ", a.split()[2])
                            else:
                                for x in range(int(a.split()[1])):
                                    inventory.remove(str(a.split()[2]))
                                    trader_inventory.append(a.split()[2])
                                trader_caps -= total_cost
                                caps += total_cost
                    else:
                        print("Invalid Input. (buy) and (sell) are accepted")
                else:
                    print("Only numbers are accepted")
            else:
                print("Sorry. ", a.split()[2], " doesn't exist!")
    load_time(100, "Ending trade")


# Choice system!
def choice():
    global auto_feed
    global people
    global rooms
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
            #print("The potential room is",potential_room)
            if len(a.split()) < 2:
                print("You have to input 2 or more words to build a room.")
            elif not check_room(potential_room):
                print("Checking for room:", potential_room)
                print("This room doesn't exist.")
            elif check_built_room(potential_room):
                print("You've already built this room.")
            else:
                room = Room(potential_room)
                checked = []  # Stores components already checked. Useful. If there's 5 pieces of wood in the components list, the loop is only run once, instead of 5 times
                can_craft = 1
                for component in room.components:
                    if component not in checked:  # Only runs check if item hasn't been encountered before
                        if room.count_component(component) > count_item(
                                component, "player"):  # If player doesn't have enough
                            print(
                                "You don't have enough",
                                component,
                                "to build",
                                potential_room)
                            can_craft = 0
                            # break #I don't break so the users will see
                            # everything they don't have.
                        checked.append(component)
                if can_craft == 1:
                    print("You have built a", a.split()[1])
                    build(potential_room)

        elif a.split()[0] == "craft":
            # Checks to see if crafting possible.
            if a.split()[1] not in all_items:
                print("Invalid item. Try again.")
            else:
                can_craft = 1
                # Creates an instance of the item, so it's attributes can be
                # fetched.
                actual_item = Item(a.split()[1])
                if len(actual_item.components) == 0:
                    print("This is a basic item and so cannot be crafted.")
                else:
                    checked = []
                    for component in actual_item.components:
                        if component not in checked:
                            number_available = count_item(component, "player")
                            number_needed = actual_item.count_component(
                                component)
                            if number_needed > number_available:
                                print(
                                    "You don't have enough",
                                    component,
                                    "to craft",
                                    a.split()[1])
                                can_craft = 0
                            checked.append(component)
                    if can_craft == 1:
                        print("You have crafted a", a.split()[1])
                        craft(a.split()[1])

        elif a.split()[0] == "scrap":
            if len(a.split()) == 2:  # Only scrap item once.
                if a.split()[1] not in all_items:
                    print("Invalid item. Please try again.")
                else:
                    count = count_item(str(a.split()[1]), "player")
                    if count > 0:
                        scrap(a.split()[1])
                    else:
                        print("You don't have that item.")
            elif len(a.split()) == 3:  # Scrap multiple times
                if a.split()[1] in range(1, 100):
                    if a.split()[2] in all_items:
                        count = count_item(str(a.split()[1]), "player")
                        if count >= a.split()[1]:
                            for x in range(a.split()[1]):
                                scrap(a.split()[2])
                        else:
                            print(
                                "You don't have enough of these items to scrap that many times.")
                    else:
                        print("This item doesn't exist.")
                else:
                    print(
                        "Invalid input. You can scrap an item up to 99 times (If you have that many).")
            else:
                print("Invalid Input. Either enter (scrap wood) or (scrap 5 wood)")

        elif a.split()[0] == "rush":  # Speeds up room tempoarily.
            potential_room = ''
            for x in a.split()[1:]:
                if len(potential_room) == 0:
                    potential_room = x
                else:
                    potential_room = potential_room + " " + x
            if not check_room(potential_room):
                print("This room doesn't exist.")
            elif not check_built_room(potential_room):
                print("You haven't built this room yet.")
            elif Room(potential_room).can_rush == 0:
                print("This room cannot be rushed")
            elif Room(potential_room).rushed == 1:
                print("This room has already been rushed.")
            else:
                room = rooms[get_room_index(potential_room)]
                # Chance that the rush fails and the room tempoarily breaks.
                chance = randint(0, 9)
                if room.risk > chance:
                    print(room.name, " has failed to rush and is broken!")
                    room.broken = 1
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
                            print("Rush failed.")
                    else:
                        print("Rush failed.")
        elif a.split()[0] == "fix":
            potential_room = ''
            for x in a.split()[1:]:
                if len(potential_room) == 0:
                    potential_room = x
                else:
                    potential_room = potential_room + " " + x
            if not check_room(potential_room):
                print("This room doesn't exist.")
            elif not check_built_room(potential_room):
                print("You haven't built this room yet.")
            elif rooms[get_room_index(potential_room)].broken == 0:
                print("This room isn't even broken. There's no need to fix it!")
            else:
                room = rooms[get_room_index(potential_room)]
                can_fix = 1
                items_needed = []
                for it in room.components:
                    chance = randint(0, 1)
                    if chance == 1:
                        items_needed.append(it)
                checked_items = []
                for it in items_needed:
                    if it not in checked_items:
                        available = count_item(it, 'player')
                        needed = room.count_component(it)
                        if needed > available:
                            print("You need", needed - available,
                                  "more", it, "to fix this room.")
                            can_fix = 0
                        checked_items.append(it)
                if can_fix == 1:
                    room.broken = 0
                    for it in items_needed:
                        Item(it).destroy("player")
                    print(
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
                print("Today is day", day_count)
            elif a.split()[1] == "resources":
                see_resources()
            else:
                print(
                    "Incorrect input. You can (see people),(see inventory), (see rooms) or (see resources)")

        elif a.split()[0] == "coitus":  # Allows player to create new inhabitants
            if len(a.split()) != 5:
                print(
                    "You need to input 2 mature people of opposite genders in the form (coitus Alex Marshall Mallus Cumberland)")
            elif not check_person(a.split()[1], a.split()[2]):
                print("No such", a.split()[1], a.split()[2], " exists!")
            elif not check_person(a.split()[3], a.split()[4]):
                print("No such", a.split()[2], a.split()[4], " exists!")
            elif len(people) == living_capacity():
                print(
                    "You've reached the vault's maximum capacity. Upgrade your living room to hold more people")
            else:
                #print("Person_1 index",get_person_index(a.split()[1],a.split()[2]))
                #print("Person_2 index",get_person_index(a.split()[3],a.split()[4]))
                person_1 = people[get_person_index(a.split()[1], a.split()[2])]
                person_2 = people[get_person_index(a.split()[3], a.split()[4])]
                if (person_1.partner == "" and person_2.partner ==
                        "") or person_1.partner == person_2.name + " " + person_2.surname:
                    if person_1.age < 18:
                        print(a.split()[1], " isn't old enough to copulate.")
                    elif person_2.age < 18:
                        print(a.split()[2], " isn't old enough to copulate.")
                    elif person_1.surname == person_2.surname:
                        print("Sorry. Incest isn't allowed. At least be ethical!")
                    elif person_1.gender == person_2.gender:
                        print(
                            "The people need to be different genders! COME ON MAN CAN U EVEN BIOLOGY!?")
                    else:
                        # Pass these love birds to the birthing system
                        birth(
                            person_1.name,
                            person_1.surname,
                            person_2.name,
                            person_2.surname)
                else:
                    print("Infedility shall not be allowed!!!")
                    if person_1.partner != "":
                        print(
                            person_1.name,
                            person_1.surname,
                            " is married to ",
                            person_1.partner)
                    else:
                        print(
                            person_1.name,
                            person_1.surname,
                            " isn't  married.")
                    if person_2.partner != "":
                        print(
                            person_2.name,
                            person_2.surname,
                            " is married to ",
                            person_2.partner)
                    else:
                        print(
                            person_2.name,
                            person_2.surname,
                            " isn't  married.")

        # Checks if player has enough food to feed person and then calls
        # feed(person) function.
        elif a.split()[0] == "feed":
            if len(choice) > 0:
                # Counts how much food is available for feeding
                food_count = count_item("food")
                if avg_hunger() < 2:
                    print("Your people are working on full bellies boss!")
                elif len(a.split()) == 2:  # If player wants to feed only one person
                    if a.split()[1] not in people:  # Checks if chosen Human exists
                        print("This person doesn't exist.")
                    else:
                        # Fetches hunger level of selected Human
                        hunger = people(a.split()[1].hunger)
                        amount = input(
                            "Feed ", a.split()[1], "  by how much? ")
                        if amount < hunger:
                            print(
                                "You don't have enough food to feed ",
                                a.split()[1])
                        else:
                            feed(a.split()[1], amount)
                else:
                    print(
                        "Invalid input! Can only feed one person like this. Use the auto_feed system to feed everyone.")
            else:
                print("Invalid input. Who do you want to feed?")
        elif a.split()[0] == "trade":
            if not check_built_room('trader'):
                print("You haven't built a trader room yet!")
            elif '1' not in str(rooms[get_room_index('trader')].assigned):
                print(
                    "No one has been assigned to this room! You can't trade untill then.")
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
                print(
                    "You have to input 4 or more words. E.g. assign Thomas Marc to living")
            # Capitalizes first character of first and last name so player
            # doesn't have to.
            elif not check_person(a.split()[1], a.split()[2]):
                print("This ", a.split()[1], " doesn't exist.")
            elif not check_room(potential_room):
                print("This room doesn't exist.")
            elif not check_built_room(potential_room):
                print("You haven't built this room yet")
            elif rooms[get_room_index(potential_room)].assigned_limit == rooms[get_room_index(potential_room)].count_assigned():
                print("This room is full.")
                print(
                    "You can assign someone in the room to another room to create space.")
            else:
                person_index = get_person_index(
                    a.split()[1][0].upper() +
                    a.split()[1][
                        1:],
                    a.split()[2][0].upper() +
                    a.split()[2][
                        1:])
                people[person_index].assign_to_room(potential_room)

        elif a.split()[0] == "auto":  # All automaticf functions
            if a.split()[1] == "assign":
                auto_assign()  # Auto-assigns every free person to a room

        elif a.split()[0] == "upgrade":
            if not check_room(
                    a.split()[1]) or not check_built_room(
                    a.split()[1]):
                print("This room doesn't exist. Try again.")
            elif a.split()[1] == "trader":
                print("This room cannot be upgraded")
            else:
                # Tempoarily fetches room so it's attributes can be used
                r = rooms[get_room_index(a.split()[1])]
                items_needed = r.components
                for x in range(
                        r.level -
                        1):  # The higher the level, the more components needed to upgrade
                    for component in items_needed:
                        items_needed.append(component)
                can_up = 1
                for ite in all_items:
                    needed = 0
                    for comp in items_needed:
                        if ite == comp:
                            needed += 1
                    # Counts number of component available to the player
                    available = count_item(ite, "player")
                    if available < needed:  # Not enough
                        can_up = 0
                        print(
                            "You don't have enough",
                            ite,
                            "to upgrade your ",
                            r.name)
                        break
                if can_up == 1:
                    for component in items_needed:
                        inventory.remove(component)
                    r.upgrade()
                    print(
                        r.name,
                        "has been upgraded and is now level",
                        r.level)

        elif a.split()[0] == "disable":
            if a.split()[1] == "auto_feed":
                auto_feed = 0
                print(
                    "Warning. You have disabled the auto_feed feature. Be careful, your people may starve!")
            else:
                print("Invalid input. You can disable the (auto_feed) system.")

        elif a.split()[0] == "enable":
            if a.split()[1] == "auto_feed":
                auto_feed = 1
                print("Auto-feed system is working optimally.")
            else:
                print("Invalid Input. You can enable the (auto_feed) system.")

        elif a.split()[0] == "scavenge":
            if a.split()[1] not in people:
                print("This person doesn't exist.")
            elif people(a.split()[1]).scavenging == 1:
                print("This person is already out scavenging.")
            else:
                cho = input(
                    "Would you like to scavenge for a certain number of days or until their health gets low?(D/H) ")
                cho = cho[0].lower()
                if cho == "d":
                    scavenge(a.split()[1], "days")
                elif cho == "h":
                    scavenge(a.split()[1])
                else:
                    print(
                        "Let's just assume you wanted them to go out until their health gets low.")
                    scavenge(a.split()[1])

        elif a.split()[0] == "heal":
            if a.split()[1] == "all":
                heal_all()
            else:
                if a.split()[1] not in people:
                    print("That person doesn't exist.")
                else:
                    stim_count = count_item("stimpack", "player")
                    if stim_count > 0:
                        people(a.split()[1]).heal(heal_amount)
        elif a.split()[0] == "skip":
            global skip
            skip = 1
        elif a.split()[0] == "end":
            global player_quit
            confirm = input("Are you sure? All unsaved data will be lost! ")
            confirm = confirm[0].lower()
            if confirm == "y":
                player_quit = 1
        elif a.split()[0] == "help":
            print_help()
        else:
            print("Invalid Input. Try again.")
    else:
        print("You have to choose something!")


def print_help():
    print("Commands: \n")
    print("""Room actions:
    see rooms           : View all rooms
    build x             : Construct room 'x'
    rush x              : Rush construction of room 'x'
    upgrade x           : Upgrade room 'x'
    fix x               : Fix damaged room 'x'
    """)
    print("""Inhabitant actions:
    see people          : View all inhabitants
    feed x              : Feed inhabitant 'x'
    enable auto_feed    : Enable automatically feeding inhabitants
    disable auto_feed   : Disable automatically feeding inhabitants
    coitus x y          : Send inhabitants 'x' and 'y' to the love-house
    scavenge x          : Send inhabitant 'x' to scavenge in the wasteland
    heal x              : Heal inhabitant 'x'
    heal all            : Heal all inhabitants
    assign x y          : Assign inhabitant 'x' to room 'y'
    auto assign         : Automatically assign unassigned inhabitants to rooms
    """)
    print("""Inventory actions:
    see items           : View all held items
    scrap x             : Destroy item and add its components to your inventory
    trade               : Begin trading interaction
    """)
    print("""Other actions:
    see day             : View day number
    see resources       : View all resources available
    skip                : Skip
    end                 : Quit game
    help                : See this help text
    """)


# Game system.
def game():
    global AP
    global end
    global position
    global people
    global day_count
    global inventory
    global rooms
    global caps
    global trader_caps
    global trader_inventory
    global all_rooms
    global all_items
    global defense
    global overuse
    global overuse_amount
    global happiness
    global auto_feed
    global used_names
    global player_quit
    global skip
    load_time(300, "Initializing game.")

    day_count = 1
    skip = 0  # Keeps track of when player is skipping a day.
    end = 0  # Can lose position or die.
    position = "secure"  # Changed to "lost" when happiness drops below 5.
    player_quit = 0  # Allows player to quit the game.
    # All items that belong to the player. Just string names
    inventory = ['turret']
    rooms = [Room('generator'), Room('living'), Room('kitchen'), Room(
        'water works'), Room('trader')]  # List of built rooms. Objects!

    people = []  # All the people alive in the shelter. Objects!
    # Names that have been used in the game. Ensures no two people have the
    # same name.
    used_names = []
    all_items = [
        "wood",
        "steel",
        "turret",
        "food",
        "water",
        "wire",
        "silicon",
        "chip",
        "watt",
        "copper",
        "gun"]  # Stores every possible item in the inventory. Just names.
    # Stores every possible room in the game. Just names.
    all_rooms = [
        "living",
        "bath",
        "generator",
        "kitchen",
        "trader",
        "storage",
        "water works"]
    all_attributes = [
        "strength",
        "perception",
        "endurance",
        "charisma",
        "intelligence",
        "luck",
        "medic",
        "science",
        "tactitian",
        "cook",
        "inspiration",
        "scrapper",
        "barter",
        "electrician"]

    caps = 100  # Basic currency
    trader_caps = 400
    happiness = 100
    trader_inventory = []
    # Initializes trader inventory with 20 random items.
    find_rand_item("trader", 20)
    defense = 0
    # Keeps track of whether or not player has used too many action points.
    overuse = 0
    # Can be set to 0 by player to conserve food.  Recomended to only do so
    # during food emergencies.
    auto_feed = 1
		# Keeps track whether or not player has used too many Action points for a
		# day.
		# overuse = 0    Why is this declared twice?

    print("Welcome to the text-based fallout shelter game!")
    print("Welcome, great Overseer!")
    print("It is your great duty to increase the population of your vault and keep your inhabitants happy.")
    create_player()
    load_time(100, "Creating player.")
    people[0].age = 20  # Set's player to 20
    first_few()  # Creates the first five inhabitants.
    load_time(200, "Populating Vault with 5 random inhabitants")
    update_all_assignment()

    print("\nYou have been given 100 caps to start your journey.")
    AP = 50
    update_all_assignment()

    print_help()

    # Loops the day while player is alive,still the overseer and doesn't
    # decide to quit.
    while end == 0 and position == "secure" and player_quit == 0:
        AP = 50
        if overuse == 1:
            AP = 50 - overuse_amount
        load_time(300, "A new day dawns.")
        print("Today is day ", day_count)

        if auto_feed == 1:
            auto_feed_all()

        # Trader inventory updates with new items and loses some items.
        # Loses a random number of items
        number = randint(0, (len(trader_inventory) // 5))
        lose_items("trader", number)
        # Finds another random number.
        number = randint(0, len(trader_inventory) // 5)
        find_rand_item("trader", number)  # Finds random number of items.

        rooms[get_room_index('generator')].update_production()
        add_to_inven(
            "watt",
            rooms[
                get_room_index('generator')].production,
            "player")
        print(
            "Producing",
            rooms[
                get_room_index('generator')].production,
            " power")

        for r in rooms:  # Performs daily room checks.
            if r.name != 'generator' and r.can_produce == 1:
                if r.can_use_power():
                    r.use_power()
                    r.update_production()
                    if r.name == "kitchen":
                        add_to_inven("food", r.production, 'player')
                        print("Cooking", r.production, " food.")
                    elif r.name == "water works":
                        add_to_inven("water", r.production, 'player')
                        print("Pumping", r.production, "water.")
                    # Add more cases for each production capable room.
                else:
                    print(
                        "You don't have enough power to keep the",
                        r.name,
                        "supplied.")
                # De-rushes every room that was rushed.
                if r.can_rush == 1 and r.rushed == 1:
                    r.rushed = 0

        for person in people:  # Performs daily checks for all people.
            # Hunger Games.
            person.hunger += 10
            if person.hunger > 99:
                print(person.name, person.surname, " has died of hunger")
                person.die()
            elif person.hunger > 80:
                print(
                    "Warning!",
                    person.name,
                    person.surname,
                    " is starving and may die soon.")
            elif person.hunger > 50:
                print(person.name, person.surname, " is hungry.")
            # Thirsty games.
            person.thirst += 10
            if person.thirst > 99:
                print(person.name, person.surname, " has died of thirst")
                person.die()
            elif person.hunger > 80:
                print("Warning!", person.name, person.surname,
                      " is extremely thirsty and may die soon.")
            elif person.hunger > 50:
                print(person.name, person.surname, " is thirsty.")
            # Level Up games
            # Checks if person has enough xp to level up.
            check_xp(person.name, person.surname)
            if person.name != people[0].name:  # Routines specific to NPCs.
                # Scavenging games
                if person.scavenging == 1:
                    if person.days_to_scavenge_for == person.days_scavenging:
                        # Now that they've finished scavenging, set everything
                        # to 0
                        person.Scavenging = 0
                        person.days_to_scavenge_for = 0
                        person.days_scavenging = 0
                    else:
                        person.days_scavenging += 1
                        # Randomly finds an item
                        rand_item("player")
                        health_loss = randint(0, 50)
                        person.take_damage(health_loss)
                        person.gain_xp(randint(10, 200))
                    if person.health < 20:
                        person.scavenging = 0
                        person.days_to_scavenge_for = 0
                        person.days_scavenging = 0
                # Experience games
                if person.assigned_room != "":
                    # Can refer to room which character had been assigned to.
                    r = rooms[get_room_index(person.assigned_room)]
                    if r.can_produce == 1:
                        person.gain_xp(r.production // 10)

        # A raid should happen once every 5 days.
        raid_chance = randint(1, 5)
        if day_count < 11:
            raid_chance = 1  # No raids should happen in the early days.
        if day_count == 5:
            print("Test raid!")
            raid()
        if raid_chance > 4:
            raid()

        while AP > 0 and overuse == 0 and player_quit == 0:  # Loops player actions.
            choice()
            if skip == 1:
                break
        skip = 0

        print(
            "Due to your shelter's happiness level you have gained ",
            happiness // 10,
            " experience")
        people[0].gain_xp(happiness // 10)
        if happiness < 5:
            position = "lost"
        elif happiness < 25:
            print("Warning. Your people are unhappy. You could lose your position if you don't improve the situation soon.")
        happiness_loss()

        day_count += 1

    else:  # Once game ends.
        if end == 1:
            print("Too bad. You died.")
        elif position == "lost":
            print(
                "Too bad. You lost your position because of your poor leadership skills.")
        again = input("Want to play again? ")
        if again[0].lower() == "y":
            game()
        else:
            print("Okay. Thanks for playing!!!")

if __name__ == '__main__':
    game()
