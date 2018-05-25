import objects as o
import random as r
import copy

global itemListPath,itemList
itemListPath = '/storage/emulated/0/qpython/ZERTH/itemList1.txt'
itemList = dict()
global current,currentTag
current = o.item('blank')
currentTag = None

name = None
kind = None
durability = None
description = None
buffs = None


reffie = {'name':current.name,'kind':current.kind,
       'durability':current.durability,
       'description':current.description,
       'buffs':current.buffs, 'debuffs':current.debuffs,
       'damage':current.damage, 'damageType':current.damageType,
       'damageReductions':current.damageReductions,
       'coverage':current.coverage, 'weight':current.weight,
       'speed':current.speed,'slots':current.slots,'whole':current}

def ref(stem,change):
    if stem == 'name':
        current.name = change
    elif stem == 'kind':
        current.kind = change
    elif stem == 'durability':
        current.durability = change
    elif stem == 'description':
        current.description = change
    elif stem == 'buffs':
        current.buffs = change
    elif stem == 'debuffs':
        current.debuffs = change
    elif stem == 'damage':
        current.damage = change
    elif stem == 'damageType':
        current.damageType = change
    elif stem == 'damageReductions':
        current.damageReductions = change
    elif stem == 'coverage':
        current.coverage = change
    elif stem == 'weight':
        current.weight = change
    elif stem == 'speed':
        current.speed = change
    elif stem == 'slots':
        current.slots = change.split(',')
    elif stem == 'icon':
        current.icon = change
        
def listImport():
    f = open(itemListPath,'r')
    for line in f.readlines():
        ls = line.split()
        if ls == []: pass
        elif ls[0] == 'vvv':
            currentTag = ls[1]
        elif ls[0] == '...':
                 
            save = copy.deepcopy(current)
            itemList.update({currentTag:save})
            currentTag = None
        else:
            le = line.split('=')
            tar = le[0].strip(' ')
            #print(tar)
            #print(tar in ref.keys())
            re= le[1][1:][:-1]
            ref(tar,re)
    f.close

"""print(itemList)
for item in itemList.values():
    print('\n\n')
    item.report()"""
    
def getItemList(): return itemList
