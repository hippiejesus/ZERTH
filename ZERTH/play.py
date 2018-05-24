import master as m
import place as p
import being as b
import objects as o

m.current_region = p.region(coordinates = [0,0],environment = p.m.GRASS)

m.test_player = b.player(nickname = 'Evan')

m.test_person = b.person(nickname = str(m.genCharName()))
m.test_person.coord = 58

m.test_plant = b.plant(name = 'Fern')
m.test_plant.coord = 60

m.test_plant2 = b.plant(name = 'Pine Tree')
m.test_plant2.coord = 83

m.test_animal = b.animal(name = 'Gopher')
m.test_animal.coord = 37

m.test_object = o.item('knife','weapon',25,'Your standard full tang blade. Nice and sharp!',
	                      None,None,'1d4+str','P/S',None,10,1,1,
	                      icon='/')
m.test_object.materialize(m.current_region,27)
m.current_region.object_list.append(m.test_object)

m.current_region.being_list.append(m.test_player)
m.current_region.being_list.append(m.test_person)
m.current_region.being_list.append(m.test_plant)
m.current_region.being_list.append(m.test_plant2)
m.current_region.being_list.append(m.test_animal)

m.main()