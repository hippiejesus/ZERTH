#Map.py
#generation of overworld, regional, settlement, and room maps
import random as rand

region_list = []
room_dict = {} #Key = region, Value = room object
settlement_dict = {} #Key = region, Value = settlement object

def col(c):
	return "\033[38;5;"+str(c)+"m"  

#Regional map presets
FOREST = {(col(226)+"/"):4,(col(10)+","):30,(col(251)+"0"):1,(col(155)+"*"):12}
TUNDRA = {(col(231)+"~"):30,(col(14)+","):5,(col(195)+"-"):15,(col(117)+"*"):2}
DESERT = {(col(227)+"~"):30,(col(178)+"^"):5,(col(229)+"-"):15,(col(40)+"*"):2}
GRASS =  {(col(10)+","):30,(col(46)+"."):5,(col(156)+"'"):15,(col(191)+","):2}

class overworld_map:
    def __init__(self):
        print('test overworld')
        
class regional_map:
    def __init__(self):
        region_list.append(self)
        
    def gen(self,options):
        self.map_dict = {}
        self.map_dictIndex = 0
        op = []
        for i in options:
            for n in range(options[i]):
                op.append(i)
        line1 = "\033[37;40m++++++++++++++++++++++++++"
        def getLine():
            line = "\033[37;40m+"
            for i in range(24):
                choice = rand.choice(op)
                ch = {self.map_dictIndex:[choice[-1],choice[:-1]]}
                self.map_dict.update(ch)
                self.map_dictIndex += 1
        for i in range(14):
            getLine()
        
    def display(self):
        self.map_dictIndex = 0
        dmap = '\033[37;40m++++++++++++++++++++++++++\n'+'\033[37;40m'
        for r in range(14):
            line = '\033[37;40m+'
            for i in range(24):
                target = self.map_dict[self.map_dictIndex]
                self.map_dictIndex += 1
                line += target[1]+target[0]
            dmap += line+'\033[37;40m+\n'
        dmap += '\033[37;40m++++++++++++++++++++++++++'
        print dmap
            
    def checkI(self,index):
        return self.map_dict[index]
        
    def setI(self,index,icon,color):
		self.map_dict[index] = [icon,col(color)]
        
    def copySelf(self):
        self2 = regional_map()
        self2.map_dict = self.map_dict.copy()
        return self2

class settlement_map:
    def __init__(self):
        print('test settlement')
        
class room_map:
    def __init__(self):
        print('test room')


#Test 1 of each regional map
def regional_test():
    for i in [FOREST,TUNDRA,DESERT,GRASS]:
        nmap = regional_map()
        nmap.gen(i)
        
    for i in region_list:
        i.display()
        print('')

#An example of using the copySelf function of the regional map.
#This function allows for a copy to be created for local map exploration
#while only making permanent changes when necessary.
"""
nmap = regional_map()
nmap.gen(FOREST)
nmap.display()
tmap = nmap.copySelf()
tmap.display()
"""
