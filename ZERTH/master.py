import os
import names
import random as rand
import place as p
import being as b

WALLS = ['0','#']
LIVING_COLOR = p.m.col(7)
directions = {'w':-24,'x':24,'a':-1,'d':1,'q':-25,'e':-23,'z':23,'c':25}
wall_kind = 'single'
wall_number = 1

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
        except:
            pass
 
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
            
#TEST SCENARIO##########################################################
current_region = p.region(coordinates = [0,0],environment = p.m.GRASS)

test_player = b.player(nickname = 'Evan')

test_person = b.person(nickname = str(genCharName()))
test_person.coord = 58

test_plant = b.plant(name = 'Fern')
test_plant.coord = 60

test_plant2 = b.plant(name = 'Pine Tree')
test_plant2.coord = 83

test_animal = b.animal(name = 'Gopher')
test_animal.coord = 37

current_region.being_list.append(test_player)
current_region.being_list.append(test_person)
current_region.being_list.append(test_plant)
current_region.being_list.append(test_plant2)
current_region.being_list.append(test_animal)
########################################################################
#Main Loop
def main():
    global wall_kind,wall_number
    while True:
        os.system('clear')
        current_region.show()
        direction = raw_input()
        if direction in directions:
            move_regional(test_player,direction)
        else:
            if direction == 'quit': break
            elif direction == 'l':
                check_surrounding_regional(test_player)
            #Build a wall
            elif direction == 'b':
                d = int(raw_input('?'))
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
                place_resource(origin, resource, size, color)
                
                

#Called upon initialization of program
if __name__=='__main__':
    main()
    print('Bye shitface!')
