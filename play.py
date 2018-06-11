import master as m
import place as p
import being as b
import objects as o

name = m.inputbox.ask(m.Surface,'What be thy name?')
print('Ye shall be known as ... '+name+' !!!')
m.menuOption(m.Continue)
m.current_region = p.region(coordinates = [0,0],environment = p.m.GRASS)

m.test_player = b.player(nickname = name)
m.placeBeing(m.test_player,0)

m.test_plant = b.plant(name = 'lilly')
m.test_plant.stats['Edible'] = True
m.test_plant.isResource = True
m.test_plant.resourceType = 'food'
m.test_plant.satiation = 20
m.placeBeing(m.test_plant, 29,passable = True)

"""m.test_person = b.person(nickname = str(m.genCharName()))
m.test_person.priorities.append('wander')
m.giveObj('wep_002',m.test_person,'rightHand')
m.placeBeing(m.test_person,58)"""

m.spawnBeing('npc_001',99)
being = m.current_region.being_list[-1]
being.nickname = str(m.genCharName())
m.giveObj('wep_002',being,'rightHand')

m.spawnBeing('npc_002',17)

m.placeObj('wep_011',98)
m.placeObj('wep_007',74)

m.main()
