#Place.py
#intimate information for each region, room, overworld, settlement
import random as rand
import map as m

directions = {'w':-24,'x':24,'a':-1,'d':1,'q':-25,'e':-23,'z':23,'c':25}


class region:
    def __init__(self,environment=rand.choice([m.FOREST,m.DESERT,m.TUNDRA,m.GRASS]),
                 coordinates=[],roomFrom=[],dirFrom=''):
        if roomFrom == []:
            if coordinates != []:
                self.coordinates = coordinates
            else: print('Can not discern location of region.')
        else:
            if dirFrom == 'South':
                self.coordinates = roomFrom
                self.coordinates[1] -= 1
            elif dirFrom == 'North':
                self.coordinates = roomFrom
                self.coordinates[1] +=1
            elif dirFrom == 'East':
                self.coordinates = roomFrom
                self.coordinates[0] -= 1
            elif dirFrom == 'West':
                self.coordinates = roomFrom
                self.coordinates[0] +=1
            else: print('Can not discern location of region.')
                
        self.being_list = []
        self.object_list = []
        self.resources = {}
        
        self.rMap = m.regional_map()
        self.rMap.gen(environment)
        print('test region')
        
    def getThing(self,target):
        for being in self.being_list:
            if being.coord == target: return being
        for item in self.object_list:
            if item.coord == target: return item
        return None
        
    def getThings(self,target):
        around_target = []
        target_indices = []
        origin = target.coord
        for i in directions:
            target_index = origin + directions[i]
            target_indices.append(target_index)
        #target_indices.append(origin)
        for i in target_indices:
            if self.getThing(i) != None:
                around_target.append(self.getThing(i))
        return around_target
        
    def show(self):
        self.tMap = self.rMap.copySelf()
        for o in self.object_list:
            self.tMap.setI(o.coord,o.icon,37)
        for b in self.being_list:
            self.tMap.setI(b.coord,b.icon,7)
        self.tMap.display()
        
        print(self.coordinates)
        
        if self.being_list != []:
            persons_present = {}
            animals_present = {}
            for b in self.being_list:
                if 'person' in b.amI: persons_present.update({b.nickname:b})
                elif 'animal' in b.amI: animals_present.update({b.name:b})
            if persons_present != {}: print('Persons: '+str(persons_present.keys()))
            if animals_present != {}: print('Animals: '+str(animals_present.keys()))
        if self.object_list != []:
            print('Objects: ')
            for item in self.object_list:
                print('    '+str(item.name))
        if self.resources != {}:
            print('Resources(and severity): '+str(self.resources))
        
class room:
    def __init__(self):
        print('test room')
        
class overworld:
    def __init__(self):
        print('test overworld')
        
class settlement:
    def __init__(self):
        print('test settlement')
        

