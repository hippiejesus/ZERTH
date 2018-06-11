import os
import sys
import names
import random as rand
import place as p
import being as b
import objects as o
import combat as c
import importItems as im
import importBeings as imb
import copy
import pygame
import inputbox
from PyQt4 import QtGui, QtCore, uic
from pygame.locals import *
from menu import menu

pygame.init()
pygame.display.set_caption("ZERTH")
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
Surface = pygame.display.set_mode((420,480))

Font = pygame.font.Font("mksanstallx.ttf",14)

Items = [('Abc', 'abc', 'button'),
         ('Do something', 'x', 'slider', (2, 0, 10)),
         ('Done', 'p', 'checkbox', True),
         ('Test', 'name', 'disabled'),
         ('Cancel', 'cancel', 'cancelbutton'),
         ('Quit', 'exit', 'button'),
         ('Useless button 1', 'btn', 'button'),
         ('Useless button 2', 'btn', 'button'),
         ('Useless button 3', 'btn', 'button'),
         ('Useless button 4', 'btn', 'button'),
         ('Useless button 5', 'btn', 'button'),
         ('Useless button 6', 'btn', 'button'),
         ('Useless button 7', 'btn', 'button'),
         ('Useless button 8', 'btn', 'button'),
        ]
        
InventoryOptions = [('Examine', 'e','button'),
                    ('Drop', 'd', 'button'),
                    ('Equip', 'q', 'button'),
                    ('Unequip','u', 'button'),
                    ('Rename', 'n', 'button'),
                   ]

ResourceOptions = [('Use', 'use','button'),
                   ('Drop', 'drop', 'button'),
                   ('Rename', 'rename', 'button'),
                  ]
                   
Continue = [('Continue', 'c', 'button')]

"""pygame.init()
pygame.display.set_caption('ZERTH')
size = [320,240]
screen = pygame.display.set_mode(size)
game_name = 'ZERTH'"""

clock = pygame.time.Clock()

im.listImport()
imb.listImport()
itemList = im.getItemList()
beingList = imb.getBeingList()
print(itemList)
print(beingList)

WALLS = ['0','#']
LIVING_COLOR = p.m.col(7)
dir_ref = {'n':'w','nw':'q','w':'a','sw':'z','s':'x','se':'c','e':'d','ne':'e'}
directions = {'w':-24,'x':24,'a':-1,'d':1,'q':-25,'e':-23,'z':23,'c':25}
wall_kind = 'single'
wall_number = 1
changes = True

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('UI/zerthUI/zerthmain.ui', self)
        
        self.show()

def menuOption(menuChoice):
    result = menu(Surface, menuChoice, 30, 200, 30, 30, 50, 300, Font)
    Surface.fill((0,0,0))
    pygame.display.update()
    return result

#Function for moving ANY object on the current_region map
def move_regional(target,direction):
    if direction in directions:
        target_index= target.coord
        destination_index = target_index + directions[direction]
        #Block movement if destination is a wall or living being
        try:
            if current_region.rMap.checkI(destination_index)[0] in WALLS or current_region.tMap.checkI(destination_index)[1] == LIVING_COLOR:
                print('Wall in way!')
            else:
                target.coord += directions[direction]
        except: pass

#Fetches Inventory dictionary from particular target actor.
def take_inventory(target):
    return target.stats['Inventory']

def loot(actor):
    possibleTargets = []
    targetButtons = []
    around = current_region.getThings(actor)
    if around == []: return
    try:
        for item in around:
            if isinstance(item,b.being):
                if item.isDead:
                    possibleTargets.append(item)
                    targetButtons.append((item.nickname,possibleTargets.index(item),'button'))
        choice = menuOption(targetButtons)
        item = possibleTargets[int(choice[0])]
        if item.stats['Inventory'] == {} and item.stats['Resources'] == {}:
            print('Nothing to loot!')
            return
        for i in item.stats['Resources'].values():
            actor.stats['Resources'].update({i.name:i})
            print(actor.nickname+' got '+i.name+'!')
        for i in item.stats['Inventory'].values():
            actor.stats['Inventory'].update({i.name:i})
            print(actor.nickname+' got '+i.name+'!')
        item.stats['Inventory'] = {}
        item.stats['Resources'] = {}
    except:
        pass

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
        
    inn = menuOption(InventoryOptions)
    
    if inn == '': return
    
    if inn[0] == 'n':
        ItemButtons = []
        for i in inv.keys():
            ItemButtons.append((str(i),i,'button'))
        itemName = menuOption(ItemButtons)[0]
        if itemName in inv.keys():
            item = inv[itemName]
            newName = inputbox.ask(Surface, "New Name")
            item.name = newName
            inv.update({item.name:item})
            inv.pop(itemName)
            print('Renamed to '+newName+'.')
            menuOption(Continue)
            display_inventory(target)
    elif inn[0] == 'u':
        ItemButtons = []
        for i in inv.keys():
            ItemButtons.append((str(i),i,'button'))
        itemName = menuOption(ItemButtons)[0]
        if itemName in inv.keys():
            item = inv[itemName]
            if item.isEquipped == True:
                item.isEquipped = False
                print(str(item.name)+' unequipped.')
                menuOption(Continue)
                display_inventory(target)
    elif inn[0] == 'q':
        ItemButtons = []
        for i in inv.keys():
            ItemButtons.append((str(i),i,'button'))
        itemName = menuOption(ItemButtons)[0]
        if itemName in inv.keys():
            item = inv[itemName]
            if item.isEquipped == True:
                print('That item is already equipped!')
                menuOption(Continue)
                display_inventory(target)
            else:
                SlotButtons = []
                for i in item.slots:
                    SlotButtons.append((str(i),i,'button'))
                slot = menuOption(SlotButtons)[0]
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
                menuOption(Continue)
                display_inventory(target)
    #Drop object in inventory.
    elif inn[0] == 'd':
        ItemButtons = []
        for i in inv.keys():
            ItemButtons.append((str(i),i,'button'))
        itemName = menuOption(ItemButtons)[0]
        if itemName in inv.keys():
            item = inv[itemName]
            if item.isEquipped == True:
                print('Unequip first!')
                menuOption(Continue)
                display_inventory(target)
            else:
                current_region.object_list.append(item)
                item.coord = target.coord
                inv.pop(itemName)
                print(str(item.name)+' dropped...')
                menuOption(Continue)
                display_inventory(target)
            
    #Examine object in inventory.
    elif inn[0] == 'e':
        ItemButtons = []
        for i in inv.keys():
            ItemButtons.append((str(i),i,'button'))
        itemName = menuOption(ItemButtons)[0]
        if itemName in inv.keys():
            item = inv[itemName]
            os.system('clear')
            item.report()
            menuOption(Continue)
        else: print('No such item!') ; menuOption(Continue)
        display_inventory(target)

#Function for getting an item from the current_region
#The actor(target) must be on the same coord as the item.
def get_item_regional(target):
    item = None
    for person in current_region.being_list:
        print(str(person.stats['Resources']))
    for i in current_region.object_list:
        if i.coord == target.coord:
            item = i
    if item != None:
        if item.name in target.stats['Inventory'].keys():
            tail = raw_input('Already have item of that type. Supply an identifier...')
            item.name = str(item.name) + tail
        target.stats['Inventory'].update({item.name:item})
        current_region.object_list.remove(item)
        print(str(target.nickname)+' gets '+str(item.name))
 
#Function for player to see all surrounding objects in better detail.
def check_surrounding_regional(target):
    around_target = current_region.getThings(target)
    names = {}
    for thing in around_target:
        try:
            names.update({'A '+thing.name+' called '+thing.nickname:thing})
        except:
            names.update({'A '+thing.name:thing})
    raw_input(str(names.keys()))
 
def check_equipped(target):
    os.system('clear')
    equipped = target.stats['Equipped']
    for i in equipped.keys():
        print(i+': '+equipped[i].name)
    menuOption(Continue)
 
def giveObj(code,actor,equip = False):
    test_object = copy.deepcopy(itemList[code])
    clist = test_object.durability.split('-')
    dur = rand.randint(int(clist[0]),int(clist[1]))
    test_object.durability = dur
    actor.stats['Inventory'].update({test_object.name:test_object})
    if equip != False:
        actor.stats['Equipped'].update({equip:test_object})
        test_object.isEquipped = True
     
 
#Place object from imported library and randomize durability.
def placeObj(code,coord):
    test_object = copy.deepcopy(itemList[code])
    clist = test_object.durability.split('-')
    dur = rand.randint(int(clist[0]),int(clist[1]))
    test_object.durability = dur
    test_object.materialize(current_region,coord)
    current_region.object_list.append(test_object)
 
def spawnBeing(code,coord,passable = False):
    test_being = copy.deepcopy(beingList[code])
    if passable == True:
        test_being.passable = True
    test_being.coord = coord
    current_region.being_list.append(test_being)
#Place being in current_region
def placeBeing(being,coord,passable = False):
    if passable == True:
        being.passable = True
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
    
def takeTurn(actor):
    global changes
    action = actor.act()
    if actor.inCombat:
        combatants = actor.currentCombat.combatants
        attacking = True
        for combatant in combatants:
            if combatant not in current_region.getThings(actor) and combatant != actor:
                print('not near')
                if 'player' in actor.amI: return
                else: attacking = False
        if attacking == True:
            actor.currentCombat.turn(actor,'attack')
            return
        else:
            pass
            
    if action != None:
        if action[0] == 'move':
            move_regional(actor,action[1])
        elif action[0] == 'seek':
            kinds = ['food','water','shelter']
            if action[1] in kinds:
                if action[1] == 'food':
                    for item in actor.stats['Resources'].values():
                        if item.resourceType == 'food':
                            actor.stats['Resources'].pop(item.name)
                            actor.satiation += item.satiation
                            print(actor.nickname+' snacks on a '+item.name)
                            return
                            
                targetCoord = 0
                actorCoord = actor.coord
                resourceList = []
                for being in current_region.being_list:
                    if being.isResource:
                        resourceList.append(being)
                for item in current_region.object_list:
                    if item.isResource:
                        resourceList.append(item)
                if resourceList == []: return
                targetCoord = None
                for resource in resourceList:
                    if resource.resourceType == action[1]:
                        targetCoord = resource.coord
                if targetCoord == None: return
                if abs(actorCoord-targetCoord) == 1 or abs(actorCoord-targetCoord)== 24:
                    harvest_regional(actor)
                direction = ''
                if actorCoord-targetCoord > 0:
                    if actorCoord-targetCoord > 24:
                        direction = 'w'
                    else:
                        direction = 'a'
                if actorCoord-targetCoord < 0:
                    if actorCoord-targetCoord < -24:
                        direction = 'x'
                    else:
                        direction = 'd'
                move_regional(actor,direction)
        changes = True
    actor.consider()

def check_status(actor):
    status = ['Hydration: '+str(actor.hydration),
              'Satiation: '+str(actor.satiation),]
    print('Status:')
    for item in status:
        print('    '+item)
    menuOption(Continue)
        

def check_resources(target):
    resourceList = target.stats['Resources']
    os.system('clear')
    print('Resources:')
    for item in resourceList.keys():
        print('    '+item+' : '+resourceList[item].resourceType)
    choice = menuOption(ResourceOptions)
    
    if choice[0] == 'use':
        ResourceButtons = []
        for i in resourceList.keys():
            ResourceButtons.append((str(i),i,'button'))
        resourceName = menuOption(ResourceButtons)[0]
        resource = resourceList[resourceName]
        if resource.resourceType == 'food':
            resourceList.pop(resourceName)
            target.satiation += resource.satiation
            print(resourceName + ' consumed.')
            menuOption(Continue)
            
    if choice[0] == 'rename':
        ResourceButtons = []
        for i in resourceList.keys():
            ResourceButtons.append((str(i),i,'button'))
        resourceName = menuOption(ResourceButtons)[0]
        resource = resourceList[resourceName]
        newName = inputbox.ask(Surface,'New Name')
        resourceList.update({newName:resource})
        resourceList.pop(resourceName)
        print('name changed to '+newName+'.')
        menuOption(Continue)
        
    if choice[0] == 'drop':
        ResourceButtons = []
        for i in resourceList.keys():
            ResourceButtons.append((str(i),i,'button'))
        resourceName = menuOption(ResourceButtons)[0]
        resource = resourceList[resourceName]
        found = False
        if isinstance(resource,b.being):
            placeBeing(resource, target.coord,passable = True)
            found = True
        elif isinstance(resource,o.item):
            resource.materialize(current_region,coord)
            current_region.object_list.append(resource)
            found = True
        if found == True:
            resourceList.pop(resourceName)
            resource.coord = target.coord
        

def harvest_regional(actor):
    possibleTargets = current_region.getThings(actor)
    TargetButtons = []
    for being in possibleTargets:
        TargetButtons.append((being.name,possibleTargets.index(being),'button'))
    if 'player' in actor.amI: 
        result = menuOption(TargetButtons)
        target = possibleTargets[int(result[0])]
    else:
        if actor.targetResource != None:
            for i in possibleTargets:
                if i.isResource == True:
                    if i.resourceType == actor.targetResource:
                        target = i
    if target.isResource == False: print('Not a resource!') ; menuOption(Continue) ; return
    try:
        actor.stats['Resources'].update({target.name:copy.deepcopy(target)})
        current_region.being_list.remove(target)
        print(target.name+' harvested by '+actor.nickname+'.')
        menuOption(Continue)
    except:
        pass
        
def combative(actor):
    possibleTargets = [('Attack whom?','aw','disabled')]
    if 'player' in actor.amI:
        for i in current_region.being_list:
            if isinstance(i,b.person): name = i.nickname
            else: name = i.name
            possibleTargets.append((name,current_region.being_list.index(i),'button'))
        choice = menuOption(possibleTargets)
    else: pass #npc targetting process goes here
    target = current_region.being_list[int(choice[0])]
    battle = c.combat([actor,target],current_region)
   
#Main Loop
def main():
    global wall_kind,wall_number,changes,Surface
    placeObj('wep_011',27)
    #app = QtGui.QApplication(sys.argv)
    #mainWindow = MainWindow()
    turn = 0
    while True:
        
        #set the speed
        clock.tick(10)
        
        if changes == True:
            os.system('clear')
            current_region.show()
            changes = False
        else: pass
        
        #check events
        for event in pygame.event.get():
            if event.type == QUIT:
                finished = True
            if event.type == KEYDOWN:
                if test_player.isDead : print('You are dead!') ; break 
                if event.key == K_KP6 or event.key == K_d:
                    move_regional(test_player,'d') ; changes = True
                if event.key == K_KP3 or event.key == K_c:
                    move_regional(test_player,'c') ; changes = True
                if event.key == K_KP2 or event.key == K_x:
                    move_regional(test_player,'x') ; changes = True
                if event.key == K_KP1 or event.key == K_z:
                    move_regional(test_player,'z') ; changes = True
                if event.key == K_KP4 or event.key == K_a:
                    move_regional(test_player,'a') ; changes = True
                if event.key == K_KP7 or event.key == K_q:
                    move_regional(test_player,'q') ; changes = True
                if event.key == K_KP8 or event.key == K_w:
                    move_regional(test_player,'w') ; changes = True
                if event.key == K_t:
                    combative(test_player)
                if event.key == K_KP9 or event.key == K_e:
                    move_regional(test_player,'e') ; changes = True
                if event.key == K_s:
                    check_status(test_player)
                if event.key == K_r:
                    check_resources(test_player) ; changes = True
                if event.key == K_l:
                    loot(test_player)
                if event.key == K_h and current_region.getThings(test_player) != []:
                    harvest_regional(test_player) ; changes = True
                if event.key == K_o:
                    check_equipped(test_player) ; changes = True
                if event.key == K_g:
                    get_item_regional(test_player)
                if event.key == K_i:
                    display_inventory(test_player) ; changes = True
        if turn == 10:
            turn = 0
            for actor in current_region.being_list:
                if 'player' not in actor.amI and not (actor.isDead):
                    takeTurn(actor)
                else: 
                    if test_player.inCombat:
                        takeTurn(test_player)
        turn += 1
        """direction = raw_input()
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
                d = raw_input('?')
                if d == '': d = 1
                d = int(d)
                place_wall(test_player.coord+d,wall_kind,wall_number)
            #Set the kind of wall layout to be built
            elif direction == 'bk':
                wall_kind = raw_input('set wall_kind: ')
            #Set the number of units of wall to be layed upon building.
            elif direction == 'bn':
                wall_number = int(raw_input('set wall_number: '))
            elif direction == 'pr':
                origin = int(raw_input('?'))
                origin += test_player.coord
                resource = raw_input('resource: ')
                size = int(raw_input('size: '))
                color = int(raw_input('color: '))
                place_resource(origin, resource, size, color)"""
                
                

#Called upon initialization of program
if __name__=='__main__':
    current_region = p.region(coordinates = [0,0],environment = p.m.GRASS)

    test_player = b.player(nickname = 'Evan')
    current_region.being_list.append(test_player)
    main()
    print('Bye shitface!')
