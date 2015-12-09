"""Item class needs to be modified
class item(object):
  def __init__(self,name,number,value,weight,components):
    self.name=name
    self.number=number
    self.value=value
    self.weight=weight
    self.components=self.components
  #Other methods to be added here#
"""
def add_to_inven(x,number):
  x=str(x)
  if x not in all_items:
    print("Invalid item. Major bug. Please contact dev")
  if x=="wood": 
    for x in range(0,number):
      inventory.append(item("wood",number,10,[])
  elif x=="gun":
    for x in range(0,number):
      inventory.append(item("gun",number,50,["metal","metal","sight"])
  #Add special cases for all in-game items, with their own seperate values, weights and components#
