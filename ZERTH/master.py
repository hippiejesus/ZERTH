import os
import names
import random as rand
import place as p
import being as b
import objects as o
import importItems as im
import copy

im.listImport()
itemList = im.getItemList()

WALLS = ['0','#']
LIVING_COLOR = p.m.col(7)
dir_ref = {'n':'w','nw':'q','w':'a','sw':'z','s':'x','se':'c','e':'d','ne':'e'}
directions = {'w':-24,'x':24,'a':-1,'d':1,'q':-25,'e':-23,'z':23,'c':25}
wall_kind = 'single'
wall_number = 1

#Function for moving ANY object on the current_region map
def move_regional(target,direction):
    if direction in directions:
        target_index= target.coord
        destination_index = target_index + directions[direction]
        #Block movement if destination is a wall or living being
        if current_region.rMap.checkI(destination_index)[0] in WALLS or current_region.tMap.checkI(destination_index)[1] == LIVING_COLOR:
            print('Wall in way!')
        else:
            target.coord += directions[direction]

#Fetches Inventory dictionary from particular target actor.
def take_inventory(target):
    return target.stats['Inventory']

#Displays inventory of target actor.
def display_inventory(target):
    inv = take_inventory(target)
    items = list()
    for i in inv.keys():
        tail = '(E)'
        if inv[i].isEquipped == False: tail = ''
        items.append(str(i)+tail)
    os.system('clear')
    print('Inventory: ')
    for i in items:
        print('    '+i)
    inn = input('e to examine, then type item.\nd to drop...\nq to equip...\nu to unequip...\nn to rename...')
    if inn == '': return
    
    if inn[0] == 'n':
        itemName = inn[2:]
        if itemName in inv.keys():
            item = inv[itemName]
            newName = input('New name: ')
            item.name = newName
            inv.update({item.name:item})
            inv.pop(itemName)
            print('Renamed to '+newName+'.')
            input()
            display_inventory(target)
    elif inn[0] == 'u':
        itemName = inn[2:]
        if itemName in inv.keys():
            item = inv[itemName]
            if item.isEquipped == True:
                item.isEquipped = False
                print(str(item.name)+' unequipped.')
                input()
                display_inventory(target)
    elif inn[0] == 'q':
        itemName = inn[2:]
        if itemName in inv.keys():
            item = inv[itemName]
            if item.isEquipped == True:
                print('That item is already equipped!')
                input()
                display_inventory(target)
            else:
                slot = input('Which slot?\n'+str(item.slots))
                equipped = target.stats['Equipped']
                slot2 = 'Hand'
                if slot2 in slot:
                   for i in copy.deepcopy(equipped).keys():
                       if slot2 in i:
                           print(str(equipped[i].name)+' unequipped.')
                           equipped[i].isEquipped = False
                           equipped.pop(i)
                if slot in equipped.keys():
                    print(str(equipped[slot].name)+' unequipped.')
                    equipped[slot].isEquipped = False
                    equipped.pop(slot)
                equipped.update({slot:item})
                print(str(item.name)+' equipped to '+slot+'.')
                item.isEquipped = True
                input()
                display_inventory(target)
    #Drop object in inventory.
    elif inn[0] == 'd':
        itemName = inn[2:]
        if itemName in inv.keys():
            item = inv[itemName]
            if item.isEquipped == True:
                print('Unequip first!')
                input()
                display_inventory(target)
            else:
                current_region.object_list.append(item)
                item.coord = target.coord
                inv.pop(itemName)
                print(str(item.name)+' dropped...')
                input()
                display_inventory(target)
            
    #Examine object in inventory.
    elif inn[0] == 'e':
        itemName = inn[2:]
        if itemName in inv.keys():
            item = inv[itemName]
            os.system('clear')
            item.report()
            input()
        else: print('No such item!') ; input()
        display_inventory(target)

#Function for getting an item from the current_region
#The actor(target) must be on the same coord as the item.
def get_item_regional(target):
    item = None
    for i in current_region.object_list:
        if i.coord == target.coord:
            item = i
    if item != None:
        if item.name in target.stats['Inventory'].keys():
            tail = input('Already have item of that type. Supply an identifier...')
            item.name = str(item.name) + tail
        target.stats['Inventory'].update({item.name:item})
        current_region.object_list.remove(item)
        print(str(target.nickname)+' gets '+str(item.name))
        input()
 
#Function for player to see all surrounding objects in better detail.
def check_surrounding_regional(target):
    around_target = current_region.getThings(target)
    names = {}
    for thing in around_target:
        try:
            names.update({'A '+thing.name+' called '+thing.nickname:thing})
        except:
            names.update({'A '+thing.name:thing})
    input(str(names.keys()))
 
def check_equipped(target):
    os.system('clear')
    equipped = target.stats['Equipped']
    for i in equipped.keys():
        print(i+': '+equipped[i].name)
    input()
 
#Place object from imported library and randomize durability.
def placeObj(code,coord):
    test_object = copy.deepcopy(itemList[code])
    clist = test_object.durability.split('-')
    dur = rand.randint(int(clist[0]),int(clist[1]))
    test_object.durability = dur
    test_object.materialize(current_region,coord)
    current_region.object_list.append(test_object)
 
#Place being in current_region
def placeBeing(being,coord):
    being.coord = coord
    current_region.being_list.append(being)
    
#Place wall-kinds(single,square,lineDOWN,lineRIGHT), origin=starting index
def place_wall(origin,kind,length,color=214):
    if kind == 'single':
        current_region.rMap.setI(origin,'#',color)
    elif kind == 'lineRIGHT':
        for i in range(length):
            place_wall(origin+i,'single',1)
    elif kind == 'lineDOWN':
        for i in range(length):
            place_wall(origin+i*24,'single',1)
    
#Place a certain resource, starting at an origin index, of a certain shape and size
def place_resource(origin,resource,size,color,shape='random'):
    adjustment = 0
    for row in range(size):
        for column in range(size):
             target_index = origin + adjustment + column
             if rand.choice([True,True,False]):
                 current_region.rMap.setI(target_index,resource,color)
        adjustment += 24

def move_overworld(target,direction):
    print('test move_overworld')
    
def genCharName():
    name = names.get_full_name()
    return name
            
#Main Loop
def main():
    global wall_kind,wall_number
    while True:
        os.system('clear')
        current_region.show()
        direction = input()
        if direction in directions:
            move_regional(test_player,direction)
        else:
            if direction == 'quit': break
            elif direction == 'l':
                check_surrounding_regional(test_player)
            elif direction == 'g':
                get_item_regional(test_player)
            elif direction == 'i':
                display_inventory(test_player)
            elif direction == 'eq':
                check_equipped(test_player)
            #Build a wall
            elif direction == 'b':
                d = input('?')
                if d == '': d = 1
                d = int(d)
                place_wall(test_player.coord+d,wall_kind,wall_number)
            #Set the kind of wall layout to be built
            elif direction == 'bk':
                wall_kind = input('set wall_kind: ')
            #Set the number of units of wall to be layed upon building.
            elif direction == 'bn':
                wall_number = int(input('set wall_number: '))
            elif direction == 'pr':
                origin = int(input('?'))
                origin += test_player.coord
                resource = input('resource: ')
                size = int(input('size: '))
                color = int(input('color: '))
                place_resource(origin, resource, size, color)
                
                

#Called upon initialization of program
if __name__=='__main__':
    current_region = p.region(coordinates = [0,0],environment = p.m.GRASS)

    test_player = b.player(nickname = 'Evan')
    current_region.being_list.append(test_player)
    main()
    print('Bye shitface!')
