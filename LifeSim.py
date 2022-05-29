import random
import time

from class1 import Creature, Prey, Predator, Plant

MapDimensions = 10
Map = [[None for col in range(MapDimensions)] for row in range(MapDimensions)]
CreatureList = []
overgrowth = True
#TODO
# CURRENT   plants randomly spawning *, DeathAndDecay *, Overgrowth on/off *
# PRIORITY  "Rozmnazanie"

# done: allow for change of MapDimensions by user,
cls_cleanup = lambda: print('\n' * 150)

# https://stackoverflow.com/questions/19326004/access-a-function-variable-outside-the-function-without-using-global
# do this ^^^^

# WARNING, ID COUNTING IS OBSOLETE


def UpdateMap():
    global Map

    Map.clear()
    Map = [[None for col in range(MapDimensions)] for row in range(MapDimensions)]

    for i in range(CreatureList.__len__()):
        # No checks are needed here, they are made by the creature
        Map[CreatureList[i].position_x][CreatureList[i].position_y] = CreatureList[i]


# noinspection PyUnresolvedReferences
def DisplayMap():
    for col in range(len(Map)):
        if MapDimensions <= 10:
            print(f"{col}", end=" ")
        for row in range(len(Map[col])):
            # Big problem/security flaw here. What if the error will be a valid one?
            # Re-do this with a check that bools only when it is a creature type | in not None might just work
            if Map[col][row] is not None:
                if Map[col][row].creature_type == "Prey":
                    print("X", end=" ")
                elif Map[col][row].creature_type == "Predator":
                    print("Z", end=" ")
                elif Map[col][row].creature_type == "Plant":
                    print("P", end=" ")
                elif Map[col][row].creature_type == "Corpse":
                    print("")
                else:
                    print("?", end=" ")
            elif Map[col][row] is None:
                print(" ", end=" ")
            else:  # I know this is dumb
                print("?", end=" ")
        print()


def GenerateCreatures():
    while True:
        prey_amount = int(input("Amount of prey? "))
        predator_amount = int(input("Amount of predators? "))
        # safety check so the map will not be over 100% of the amount of map tiles
        plant_amount = prey_amount  # for now 1 to 1 ratio
        if prey_amount + predator_amount + plant_amount > MapDimensions * MapDimensions:
            print("Too many creatures")
            continue
        if prey_amount > 0 or predator_amount > 0:
            print(f"{prey_amount + predator_amount + plant_amount} Objects to be initialised")
            break

    for i in range(prey_amount):
        CreatureList.append(Prey("Prey"))

    for i in range(predator_amount):
        CreatureList.append(Predator("Predator"))

    for i in range(plant_amount):
        CreatureList.append(Plant("Plant"))

    global Map

    for i in range(CreatureList.__len__()):
        while True:
            CreatureList[i].position_x = random.randint(0, MapDimensions-1)
            CreatureList[i].position_y = random.randint(0, MapDimensions-1)
            # do it using the creature position instead of map field

            # If it is something else than a None field, aka creature
            # re-roll positions, if not break and put it on the map
            if Map[CreatureList[i].position_x][CreatureList[i].position_y] is not None:
                continue
            else:
                break
            # ^ why did I implement this twice, but in a different way?
        Map[CreatureList[i].position_x][CreatureList[i].position_y] = CreatureList[i]

    global overgrowth
    YNbool = str(input(f'Overgrowth [y/n] '))

    if YNbool == 'y' or YNbool == 'Y' or YNbool == 'yes':
        overgrowth = True
    elif YNbool == 'n' or YNbool == 'N' or YNbool == 'no':
        overgrowth = False


def TeamTrees():
    global CreatureList
    plant_amount = 0
    plant_list = []
    for element in CreatureList:
        if element.creature_type == "Plant":
            plant_amount += 1
            plant_list.append(element)

    # Not a serious bug here, sometimes one plant is not counted

    # add new plants # might wanna do a check if the plant amount is too low
    for i in range(int(plant_amount/2)):
        CreatureList.append(Plant("Plant"))
        plant_list.append(CreatureList[-1])

    # Randomly Replant Plants
    # Plant already planted plants and plant new plants in random coordinates.
    # Do not retry if failed to plant new plants
    for i in range(plant_list.__len__()):
        # If plant has default init position, give them new
        if plant_list[i].position_x == -1 or plant_list[i].position_y == -1:
            plant_list[i].position_x = random.randint(0, MapDimensions-1)
            plant_list[i].position_y = random.randint(0, MapDimensions-1)

        # if not field_free or field_not_taken_by_self
        if Map[plant_list[i].position_x][plant_list[i].position_y] is not None \
                and Map[plant_list[i].position_x][plant_list[i].position_y] is not plant_list[i]:
            continue
        else:
            CreatureList[CreatureList.index(plant_list[i])] = plant_list[i]


def CreatureActions():
    # Iterate through every creature that is NOT a plant - use move action
    for creature in CreatureList:
        if creature.creature_type != "Plant" and creature.creature_type != "Corpse":
            creature.move(random.randint(0, 4), Map, CreatureList)
        Map[creature.position_x][creature.position_y] = creature  # Place that creature on the map // TEST W/O THIS
    # after all moves are done, use DeathAndDecay
    for creature in CreatureList:
        if overgrowth:
            if creature.creature_type != "Plant":  # Plants do not decay (TODO) if overgrowth is true
                creature.death_and_decay(CreatureList, Map, MapDimensions)  # Death and decay
        else:
            creature.death_and_decay(CreatureList, Map, MapDimensions)


def EndPrint(generation):
    # EndPrint is for decorative purposes
    # if map is larger than 10 then don't bother incrementing
    if 10 < Map.__len__():
        bridge_line = "___"
        bridge_line = bridge_line + "__" * MapDimensions
        print(bridge_line)
        print(generation)
    else:
        string = "  "
        bridge_line = ""
        for i in range(Map.__len__()):
            string = string + str(i) + " "
            bridge_line = "_"*string.__len__()
        print(bridge_line)
        print(generation)
        print(string)


def clear_console():
    cls_bool = str(input("Clear console after a generation? [y/n]"))
    if cls_bool == 'y' or cls_bool == 'Y' or cls_bool == 'yes':
        cls_bool = True
        print(f'Clear_console: {cls_bool}')
    elif cls_bool == 'n' or cls_bool == 'N' or cls_bool == 'no':
        cls_bool = False
        print(f'Clear_console: {cls_bool}')
    else:
        cls_bool = False
        print(f'Unrecognised answer, now using default')
        print(f'Clear_console: {cls_bool}')
    return cls_bool


def select_MapDimensions():
    global MapDimensions
    global Map
    while True:
        MapDimensions = int(input("Map dimensions (a^2): "))
        print(f'Number of fields: {MapDimensions * MapDimensions}')
        YNbool = str(input("Confirm [y/n] "))
        if YNbool == 'y' or YNbool == 'Y' or YNbool == 'yes':
            Map = [[None for col in range(MapDimensions)] for row in range(MapDimensions)]
            return


def EndSimulationCheck():
    if len(CreatureList) >= MapDimensions*MapDimensions:
        print("Overpopulation, stopping simulation")
        raise Exception("Overpopulation, stopping simulation")
    elif len(CreatureList) == 0:
        print("No life remaining, stopping simulation")
        raise Exception("No life remaining, stopping simulation")
    else:
        return

# how it works
# do a list of object creatures
# put them on the map
# cycle the list of creatures to find out where the specific creature is
# possible idea of making initiative as a stat
# that creature makes their action
# put it on the map
# after every creature has done their action
# display that map
# cycle all


test_iterator = 0
CreatureIdOuter = 0

select_MapDimensions()
GenerateCreatures()  # generate creatures before going into the game loop
clear_console = clear_console()  # synonyms not found
print("X-Prey, Z-Predator, P-Plant, C-Corpse")
time.sleep(5)
while True:
    test_iterator += 1
    CreatureActions()
    TeamTrees()
    UpdateMap()
    DisplayMap()
    time.sleep(1)
    EndSimulationCheck()
    EndPrint(test_iterator)
    if clear_console:
        cls_cleanup()
