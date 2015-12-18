#Text-based Fallout Shelter game developed by T.G. and The-9880

from random import randint

class human(object): #Basic class for all the humans present in the game.
	def __init__(self,name,day_of_birth,parent_1,parent_2,gender):
		if len(all_people) <6 and day_count<3: #First 5 people will be 21 years old, so they can mate.
			self.age=21
		else:
			self.age=0
			
		self.allocated_room=[] #Keeps track of where person is working.
		self.hunger=0
		self.thirst=0
		self.name = name
		self.parent_1=parent_1
		self.parent_2=parent_2
		self.gender=gender[0].lower()
		
		#The stats of the person. Plan to use this to affect the production of room the person has been assigned to.
		self.strength=1
		self.perception=1
		self.endurance=1
		self.charisma=1
		self.intelligence=1
		self.luck=1
		
		self.can_mate=0 #Keeps track of mating ablility
		self.children=[] #List of all children
		self.partner="" #Keeps track of partner of person. Only partners can have coitus.
	def mature(self):
		self.age+=1
		print(self.name," has matured and is now ",self.age," years old!")
	def rebirth(self): #Don't know if I'll ever use this.
		self.age=0
		if self.gender=="f":	
			print(self.name," has been reborn and his stats have been reset")
		else:
			print(self.name," has been reborn and her stats have been reset")
		self.strength=1
		self.perception=1
		self.endurance=1
		self.charisma=1
		self.intelligence=1
		self.luck=1
		self.assigned=0 #Keeps track of whether or not human has been assigned to a room.
	def can_mate_check(self): #Checks if person can have coitus and have children. Perfomed twice when player inputs coitus, once for each proposed parent.
		if len(self.children)==0:
			self.can_mate=1
		if self.age <18:
			self.can_mate=0
		if len(self.children)>5: #Upper limit of children is 5
			self.can_mate=0
		for child in self.children: #Have to wait for a year before parent can have child again.
			if child.age<1:
				self.can_mate=0
				
	def die(self): 
		global end
		global all_people
		global all_rooms
		print(self.name," has died")
		if all_people[0].name==self.name: #Uses first index since player will always be the first person in the list, checks if player has died.
			end=1 #Ends game
		all_rooms[self.allocated_room].remove(self.name) #Removes character from room he was assigned to.
		all_people.remove(self)
		
class room(object): #Basic class for the rooms in the game. NEEDS COMPLETE REWORKING!!!
	def __init__(self,name,group): #Name would be something like "living_room_3" while group would be "living". So all living rooms have the same initial stats.
		self.name=name
		self.group=group #A lot of variables determined by the group.
		if self.group=="living": # Living rooms have no "inhabitants". Number of living rooms just limits the total population of the shelter.
			self.risk=0
			self.can_rush=0 #Stores whether or not room can even be rushed. E.g. living rooms can't be rushed
			self.can_produce=0 #Stores whether or not room actually produces anything.
		elif self.group=="generator":
			self.production= #Should produce power
			self.inhabitants=[] #Everyone working in the room.
			self.can_rush=1 # Generator rooms can be rushed and for a short while, power production will increase
			self.production=100 #Efficiency of the room
			self.rush_count=0 #Number of times room has been rushed
		# Need to add more groups.	
		
	def rush(self): #Needs a lot of work!!! Like nothings done. Like nothing. Should tempoarily improve room production. Need to develop a random chance system whether rushing works or not.
		if self.can_rush==0: #Method should never be called on non-rushable rooms.
			print("Bug with can_rush check. Please contact dev.")
		self.production+=10 
		self.rushed=1 #Let's game know this room has been rushed.
		self.rush_count+=1
		
	def update_production(self): #Calculates prouction level based on number of and skills of inhabitants. 
	#Maybe get the sum of all the inhabitants stats, depending on the room group. E.g. a generator's production may be based on the strength of the workers.
		for name in self.inhabitants:
			pass##
		
	def produce(self): #Needs a lot of work-T.G.
		if self.can_produce==0:
			print("Invalid.", self.name", cannot produce! Please contact dev!")
		else:
			inventory.append(self.benefits*self.production)
			
	def scrap(self):
		print(self.name," has been scrapped and these")
		for item in self.components:
			inventory.append(item)
			print(item,end=",")
		print("have been added to your inventory")
		self.destroy()
		
	def destroy(self):
		global rooms
		rooms.remove(self)
	
class item(object): # Basic model for items in the game.
	#Objects of this class will never be stored.
	def __init__(self,name):
		self.name=name
		#Just needs to get the name, all other attributes are automatically assigned by the following lines.
    	if self.name=="wood":
	    	self.value=10 
	    	self.weight=5 
	    	self.components=[] #This is a basic item and cannot be scrapped.
	        self.rarity=1 #Determines chance of it showing up during scavenging or in the trader's inventory
	    elif self.name=="steel":
	    	self.value=10 	
	    	self.weight=5 
	    	self.components=[]
	        self.rarity=2
	    
	    #Add special cases for every item that can exist in the game
	    
	    self.scrapped=0 #Keeps track of whether item has been scrapped by player.
	    
	def scrap(self): #Destroys the item and adds it's compoenents to the inventory.
		print(self.name," has been scrapped and these")
		for item in self.components:
			inventory.append(item)
			print(item)
		print("have been added to your inventory")
		self.destroy()
		self.scrapped=1 #Differentiate between whether item has been scrapped or just destroyed
	def destroy(self):
		global inventory
		inventory.remove(self.name)
		if self.scrapped!=1:
			print(self.name," has been destroyed!")





#Information system!
# Bunch of functions used by other functions to retrieve information about the shelter, it's inhabitants, rooms and items.

def input_int(x): #Whenever player has to input an integer, this should be used. Catches errors.
	x=input("Input an integer.")
	try:
		int(x)
	else ValueError:
		print("Invalid. Only integer numbers are accepted!")
		x=input("Try again. Input:")
		check_int(x) #Recursion!
	return x

def count_room(room):#Counts total number of a room.
	count=0
	for x in rooms: #Needs testing
		if rooms[x][len(room)]==room: #Only takes part of the room name so living_room_1 and living_room_2 are both counted.
				count+=1
	return count

def count_item(item,target_inventory): #Counts total number of an item present in an inventory
	item=str(item)
	count=0
	if target_inventory=="player":
		for x in inventory:
			if x==item:
				count+=1
		return count
	elif target_inventory=="trader":
		for x in trader_inventory:
			if x==item:
				count+=1
		return count
	else:
		print("Bug with item counting system. Please contact dev!")
		
def count_weight(): #Calculates the sum of the weights of all items currently in the inventory,
	count=0
	for x in inventory:
		count+=item(x).weight #Creates instances of class on the fly. If 5 wood present, tempoarily creates 5 wood, one by one, uses their weight and discards them
	return count
		
def storage_capacity(): #Calculates how much more weight the player can hold.  Used to check if player can take any more items.
	storage_rooms=count_room("storage")
	capacity=storage_rooms*100
	total_weight=count_weight()
	capacity=capacity-total_weight
	return capacity
		


def check_room(x):#Checks if a room exists.
	check=0
	for y in rooms:
		if x[0,len(y)]==y:
			check=1
	if check==1:
		return True
	else:
		print(room, " doesn't exist")
		return False
		
def see_people(): #Displays everyone in the shelter.
	for person in all_people:
		print(person.name,person.age,person.gender,person.hunger,person.thirst)#Add more attributes
		
def see_inventory(inven):#Displays all items in inventory in the form (Log*5.Weight=5.Value=10.Components="Wood". Rarity=1).
	if inven=="player":
		for x in inventory:
			count=count_item(x,"player")
			if count>0: #If there are no instances of the item present, no need to display it.				
				it=item(x) #Creates a tempoary object so it's data can be fetched.
				print(x,"*",count,". Weight: ",it.weight,". Value: ",it.value,". Components: ",it.components,". Rarity: ",it.rarity)

	elif inven=="trader":
		for x in trader_inventory:
			count=count_item(x,"trader")
			if count>0: #If there are no instances of the item present, no need to display it.				
				it=item(x)
				if it.components!=[]
					print(x,"*",count,". Weight: ",it.weight,". Value: ",it.value,". Components: ",it.components,". Rarity: ",it.rarity)
				else:
					print(x,"*",count,". Weight: ",it.weight,". Value: ",it.value,". Components: ",it.components,". Rarity: ",it.rarity)
	else:
		print("Major bug with inventory information system. Please contact dev!")







#Scavenging system. Needs work.
def scavenge(person,var): #Sends people on a scavenging mission. Needs work.
	global all_people
	all_people[person].scavenging=1
	if var=="days": #If player chooses to send player for certain number of days, or until health drops below 20.
		pass
	elif var=="health": #If player chooses to send until health drops below 20.
		pass
	
	
	
	
	
#Construction system. Needs work.
def build(room): #Builds a room once checks are done. Should append to (rooms) list. Third living room should be called living_room_3
	global rooms
	room=str(room)
	
def craft(item):#Crafts an item once checks are done. Just add the name of an item to the inventory name.
	global inventory







#Human management system
def get_player_gender():#Asks player what gender they are.
	gender=input("Please choose a gender.(M/F)")
	gender=gender[0].lower()
	if gender!="m" or "f":
		print("Invalid gender choice!")
		get_player_gender()
	return gender
	
def get_gender(): #Randomly generates a gender. For NPCs
	gender=randint(0,1):
	if gender==0:
		gender="m"
	else:
		gender="f"
	return gender

def birth(parent_1,parent_2): #Creates new NPC.
	global all_people
	name=input("Choose a first name for the new child: ")
	if len(name.split())!=1:
		print("You have to input a single word!)
		birth(parent_1,parent_2)
	all_people.append(human(name,name,day_count,parent_1,parent_2,get_gender)
	if day_count>2: #First few births cost no points
		use_points(50)
		
def first_four(): #Runs once at beginning of game. Creates 4 new people. Costs no Action Points!
	global all_people
	names=["Thompson","Elenor","Codsworth","Sharmak","Luthor","Marhsall","Cole","Diven","Davenport"] #Random surnames for inital 5 inhabitants. All children will inherit their surnames from their parents.	if day_count<2: #Initial 5 inhabitants need to be birthed
	while len(all_people)<6:
		num_1=randint(len(names))
		num_2=randint(len(names))
		if num_1==num_2:
			continue
		birth(names[num_1],names[num_2]) #Passes random names to birth() function.

def create_player():#Only ran at start of game. First inhabitant of vault should be the player.
	global all_people
	name=input("Choose a first name for yourself: ")
	surname=input("Choose a surname for yourself: ")
	parent_1=input("What is the surname of your father?")
	parent_2=input("What is the surname of your mother?")
	all_people.append(human(name,day_count,parent_1,parent_2,get_player_gender)
	

 
 
 
 
 
 
#Inventory managment system!
def rand_item(target_inventory): #Randomly chooses an item and adds it to either the player's or the trader's inventory
	#Used daily with trader inventory, to randomize the items they have on sale.. Used with player inventory when scavenging mission is done.
	global inventory
	global trader_inventory
	#Following lines randomly choose an item, based on rarity
    num=randint(1,1024)
    lst=[2**a for a in range(0,11)]
    count=0
    for chance in lst:
        if num<chance:
            break
        count+=1
    rar=11-count #Determines the rarity of an item. 50% chance it's a level 10, 25% chance it's a level 9, 12.5% chance it's a level 8 and so on.
    possible_items=[]
    for x in all_items:
    	if item(x).rarity==rar: 
    		possible_items.append(x)
    number=randint(len(possible_items))
    actual_item=possible_items[number]
    #Following lines actually store the item in memory
	if target_inventory=="player":
		add_to_inven(actual_item,1,inventory)
	elif target_inventory=="trader":
		add_to_inven(actual_item,1,trader_inventory)
	else:
		print("Bug with random item system. Please contact dev!")
		
def find_rand_item(inven,times): #Finds x items randomly and adds it to an inventory.
	for x in range(times):
		rand_item(inven) #passes iven to rand_item function

def add_to_inven(x,number,inven): # Adds (x) (number) times to (inven) inventory. E.g. wood,5,player
	global trader_inventory
	global inventory
	x=str(x)
	inven=str(inven)
	if x not in all_items:
		print("Invalid item. Major bug with inventory adding system. Please contact dev") #Should never happen, since all checks should be done before this function is called.
	else:
		if inven=="player":
			for y in range(number):
				inventory.append(x)
	
		elif inven=="trader":
			for y in range(number):
				trader_inventory.append(x)

def lose_items(inven,number):
	global inventory
	global trader_inventory
	if iven=="trader":
		for x in range(number):
			rand_number=randint(0,len(trader_inventory))
			inventory.remove(trader_inventory[rand_number])
	elif iven=="player": #Only when shelter has been raided by hostile forces
		print("The raid made off with these items!")
		for x in range(number):
			rand_number=randint(0,len(inventory))
			e=iventory[rand_number]
			print(inventory[e])
			inventory.remove(e)
	else:
		print("Major bug in item losing system. Please contact dev!")
		


		


#Raiding system.
def raid():
	raiders=["Super Mutant","Raider","Synth","Feral Ghoul"]
	raider=raiders[randint(len(raiders))]
	attack_power=randint(1,day_count//10)
	print("There was a ",raider," raid on your shelter!")
	if defense>attack_power:
		print("But your defenses were strong enough to send them packing!")
	else:
		loss=attack_power-defense
		lose_items("player",loss)
		if loss>10:
			death_chance=loss//10
			dice=randint(2,25):
			if death_chance<dice:
				#Death
				possible_deaths=all_people[1,len(all_people)] #The player can't die in a raid!
				death_number=randint(0,len(possible_deaths))
				print(possible_deaths[death_number]," has been killed in a raid")
				possible_deaths[death_number].die()
				



	
#Happiness System.

def avg_hunger(): #Calculates average hunger level.
	total=0
	for x in all_people:
		total+=x.hunger
	avg=total/len(all_people)
	return avg
	
def avg_thirst(): #Calculates average thirst level
	total=0
	for x in all_people:
		total+=x.thirst
	avg=total/len(all_people)
	return avg

def feed(person,food): #Reduces the hunger level of a person. 
#This needs to reduce the thirst level aswell.
	global all_people
	all_people(person).hunger-=food
	if all_people(person).hunger<0:
		all_people(person).hunger=0
	AP-=1 Feeding costs 1 point
	
def happiness_loss(): #Depending on hunger or thirst level, reduces general happiness level.
	global happiness
	loss=0
	for y in range(30,101,10):
		if avg_hunger()<y:
			loss+=y-30
			break
	for y in range(30,101,10):
		if avg_thirst()<y:
			loss+=y-30
			break
	happiness-=loss
	print("Due to your inhabitants being hungry and/or thirsty the shelter's overall happiness has dropped to ",happiness)


#Action Point usage system.
#This system is very important and needs to be developed.
#Should deduct from AP. If Ap gets below 0, stores the difference in (overuse). The next day's Action points should be less then.
#For example, if player has 10 action points left, and perfrom an action that costs 20, a day will pass but instead of 50, they'll have 40 action points
def use_points(point): #Woah this system needs a lot of work. Like it's extremely broken.
	global AP
	global overuse
	usage=AP-point
	overuse=0
	if usage<0:
		usage=50-AP
		overuse=1
	else:
		AP=AP-usage
		

	

#Trading system.	
def trade(): #Trading system. Uses no Action Points
	global inventory
	global trader_inventory
	if "trader" not in built_room_types:
		print("There is no trader built. You can't trade until you set up a trading room.")
		choice()
		
	else: # If trader exists, allows trading.
		while True: #"continue" lets trading continue, "break" stops trading
			print("Here are the traders' items: ")
			see_inventory("trader") 
			print("The trader has ", trader_caps, " caps.")
				
			print("Here are your items: ")
			see_inventory("player")
			print("You have ", caps, " caps.")
			
			print("For instance, input (buy 5 food) if you want to buy 5 units of food. Or input (end) to stop trading.")
			a=("What do you want to do?.")
			
			#Following lines are checks.
			if len(a)!=3:
				print("You have to input 3 words. Buy/sell,amount,item")
				continue
			try:
				int(a.split()[1])
			else ValueError:
				print("You have to input a number as the second word")
				continue
			if a.split()[2] not in all_items:
				print("Sorry. ",a.split()[2]," doesn't exist!")
				continue
			#Checks end here
			
			cost=item(all_items[a.split()[2]]).value #Fetches cost of item by tempoarily creating it's object and retreiving it's value attribute
			total_cost=cost*a.split()[1] #Sums up the money that is exchanging hands
			
			if a.split()[0]=="buy":
				if total_cost>caps:
					print("You can't afford that!")
					continue
				count=count_item(a.split(2),"trader")
				if a.split()[1]>count:
					if count==0:
						print("The trader doesn't have any ",a.split()[2])
					else:
						print("The trader doesn't have ",a.split()[1]," of ",a.split()[2])
					continue
				else:
					for x in range(a.split()[1]):
						trader_inventory[str(a.split()[2])].destroy()
						inventor.append(str(a.split()[2])
					caps-=total_cost
				continue
					
			elif action.split()[0]=="sell":
				if total_cost>trader_caps:
					print("The trader can't afford that!")
					continue
				count=count_item(a.split(2),"player")
				if a.split()[1]>count:
					if count==0:
						print("You don't have any ",a.split()[2])
					else:
						print("You don't have ",a.split()[1]," of ",a.split()[2])
					continue
				else:
					for x in range(a.split()[1]):
						_inventory[str(a.split()[2])].destroy()
						trader_inventory.append(str(a.split()[2])
					trader_caps-=total_cost
				continue
			
			elif action()[0]=="end":
				break
			
			else:
				print("Invalid Input! Try again!")
				continue
			
	elif a.split()[0]=="see":
		if a.split()[1]=="people":
			see_people()
		elif (a.split()[1])[0,4]=="inven":
			see_inventory("player")
		else:
			print("Incorrect input. To see people, input (see people). To view your inventory, input (see inventory) 
		continue
	
#Choice system!
def choice():
	a=input("Choose what to do:")
	
	if a.split()[0]=="build": #Allows player to build new rooms. Checks if player has components to build room.
		if not check_room(a.split()[1]):
			choice()
		for component in all_rooms[a.split()[1].components]:
			component_count=count_item(component)
			for item in inventory:
				if item==component:
					item_count=count_item(item)
				if item_count<component_count:
					print("You don't have the required components to craft this item")
					choice()
		build(a.split[1])
		
	elif a.split()[0]=="craft":#Crafting system. The-9880 assigned to this. Checks to see if player can craft. Maybe want to allow player to craft one item multiple times.
		if a.split()[1] not in all_items:
			print("Invalid item. Try again.")
			choice()
		#Need to check if player has all components. Maybe use count_item() function.
		craft(a.split()[1])
		
	elif a.split()[0]=="rush":#Speeds up room tempoarily. Needs a lot of work. room.Rush() method incomplete.
		
		if not check_room(a.split()[1]):
			choice()
			
		a.split[1].rush()
		

	elif a.split()[0]=="coitus": #Allows player to create new inhabitants
		if len(a)!=3:
			print("You need to input 2 mature people of opposite genders.")
			choice()
		if a.split()[1] not in all_people:
			print("No such",a.split()[1]," exists!")
			choice()
		if a.split()[2] not in all_people:
			print("No such",a.split()[2]," exists!")
			choice()
		if a.split()[1].partner!="" or a.split()[2].partner:
			print("Infedility shall not be allowed!!!")
			print(a.split()[1].name,"  is married to ",a.split()[1].partner)
			print(a.split()[2].name,"  is married to ",a.split()[2].partner)
			
		if a.split()[1].age <18:
			print(a.split()[1]," isn't old enough to copulate.")
			choice()
		if a.split()[2].age <18:
			print(a.split()[2]," isn't old enough to copulate.")
			choice()
		if all_people(a.split()[1]).surname==all_people(a.split()[2]).surname:
			print("Sorry. Incest isn't allowed. At least be ethical!")
			choice()
		if all_people(a.split()[1].gender)==all_people(a.split()[2].gender):
			print("The people need to be different genders! COME ON MAN CAN U EVEN BIOLOGY!")
			choice()
		birth(a.split()[1],a.split()[2])
		
		
		
	elif a.split()[0]=="feed": #Checks if player has enough food to feed person and then calls feed(person) function.
		food_count=count_item("food") #Counts how much food is available for feeding
		print("You have ",food_count," items of food.")
		avg_hunger=avg_hunger() #Fetches average hunger level. Used if player tries to feed everyone.
		if avg_hunger()<2:
			print("You're people are working on full bellies boss!")
			choice()
		if len(a.split())==2: #If player wants to feed only one person
			if a.split()[1] not in all_people: #Checks if chosen human exists
				print("This person doesn't exist.")
				choice()
			hunger=all_people(a.split()[1].hunger) #Fetches hunger level of selected human
			amount=input("Feed ",a.split()[1],"  by how much?")
			if amount<hunger:
				print("You don't have enough food to feed ",a.split()[1])
			else:
				feed(a.split(),amount)
		else: #Meens player may want to feed all people
			if a.split()[1]=="all":
				while food_count>len(all_people):
					for person in range(len(all_people)):
						feed(all_people[person],1)
						
	elif a.split()[0]=="trade": #Needs work
		if "trader" not in built_room_types:
			print("You haven't built a trader room yet!")
			choice()
		elif rooms["trader"].inhabitants==[]:
			print("No one has been assigned to this room! You can't trade untill then.")
			choice()
	elif a.split()[0]=="
		
	else:
		print("Invalid Input. Try again.")
		choice()
		

#Game loop system.
def loop():#Needs work
	global day_count
	global end
	global postition
	global inventory
	global rooms
	global caps
	global trader_inventory
	global trader_caps
	global defense
	global overuse
	global happiness
	
	day_count=0
	end=0 #Can lose postition or die.  This is used for a while loop.
	print("Welcome to the text-based fallout shelter game!")
	print("Welcome, great Overseer!")
	print("It is your great duty to increase the population of your vault and keep your inhabitants happy!")
	create_player()
	player.age=20
	print("Commands:/n")
	#Put Instructions for player here
	print("You have been given 100 caps to start your journey")
	
	
	postition="secure" #Only changed to "lost" when happiness drops below 5.
	inventory=[] #All items that belong to the player
	all_items=[] #Stores every possible item in the inventory. Just names.
	all_room_types=["living","bath","generator","kitchen","trader","storage"] #Stores every possible room type in the game. Just names.
	built_room_types=[] #Each time player builds a room type that they've never built before, it's appended here. Used to keep track of progress. Just names
	rooms=[] #Rooms that player has built. Objects!
	all_people=[] #All the people alive in the shelter. Objects!	
	caps=100
	trader_caps=400
	happiness=100
	trader_inventory=[]
	defense=0 
	overuse=0#Keeps track of whether or not player has used too many action points.
	while end==0 and position=="secure": #Loops the day
		
		AP=50
		if overuse>0:
			AP=50-overuse
		print("Today is day ".day_count)
		day_count+=1
		
		for room in all_rooms: #Causes all buildings to produce. Doesn't work
			room.produce()
		
		#Trader inventory updates with new items and loses some items.
		number=randint(0,len(trader_inventory)/5)
		lose_items("trader",number) 
		number=randint(0,len(trader_inventory)/5) #Finds another random number.
		find_rand_item("trader",number)
		
		#A raid should happen once every 5 days.
		raid_chance=randint(1,10)
		if day_count<11:
			raid_chance=0 #No raids should happen in the early days.
		if raid_chance<3:
			raid()
			
		if happiness<5:
				postition="lost"
		elif happiness<20:
			print("Warning. Your people are unhappy. You could lose your position if you don't improve the situation soon.")
		
				
		for room in rooms: #De-rushes every room that was rushed.
			if room.rushed==1:
				room.production-=10
				room.rushed=0
				
		while AP>0 and overuse==0: #Loops player actions.
			choice()
			if AP<0: #If AP is negative
				overuse=0-AP #This shall be a positive number!
				
		happiness_loss()
		
		for person in all_people: #Increases hunger and thirst level of everyone in the vault.
			person.hunger+=10
			if person.hunger>99:
				person.die()
				print(person.name," has died of hunger")
			elif person.hunger>80:
				print("Warning!",person.name," is starving and may die soon.")
			elif person.hunger>50:
				print(person.name," is hungry.")
			person.thirst+=10
			if person.thirst>99:
				person.die()
				print(person.name," has died of thirst")
			elif person.hunger>80:
				print("Warning!",person.name," is extremely thirsty and may die soon.")
			elif person.hunger>50:
				print(person.name," is thirsty.")
		
			
	else: #Once game ends.
		if end==1:
			print("Too bad. You died.")
		elif postition=="lost":
			print("Too bad. You lost your postition because of your poor leadership skills.")
		again=input("Want to play again?")
		again=again[0].lower()
		if again=="y":
			loop()
		else:
			print("Okay. Thanks for playing!!!")
	
			
