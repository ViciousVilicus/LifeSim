import random
import time

from class1 import Creature, Pray, Predator, Plant

# Proper clear doesn't want to work, used the 'print a lot of lines' solution:
# Works but meh, on a bigger map it will be better
# Random doesn't want to work, no idea what is wrong, it worked on the monopoly one:
# My dumb ass was adding onto the list, but displaying only the first generation
# so great, made my first memory leak...
MapDimensions = 3
Map = [[None for col in range(MapDimensions)] for row in range(MapDimensions)]
CreatureList = []
# CURRENT   Implement new features - predators eating prey, prey eating plants, plants randomly spawning
# PRIORITY  or rework some old stuff
# Potential methods - divide predators and prey into subclasses of Creature

# FIXED
# BUG Found - Creatures have always very specific coordinates at the beginning of the simulation
# reconsider first map generation - picking creatures coordinates might be better to be done elsewhere
# what - GenerateFirstMapGeneration - does this even do anything

clearConsole = lambda: print('\n' * 150)

# https://stackoverflow.com/questions/19326004/access-a-function-variable-outside-the-function-without-using-global
# do this ^^^^


def GenerateFirstMapGeneration():
    # why is this 'if' here? what scenario does it cover?
    # after 2 weeks I remember, this clears the map beforehand so there won't be a memory leak
    global Map

    if Map.__len__ != 0:
        Map.clear()
        Map = [[None for col in range(MapDimensions)] for row in range(MapDimensions)]
        # this may not be necessary if I will make this solely for the first map generation


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
                else:
                    print("?", end=" ")
            elif Map[col][row] is None:
                print(" ", end=" ")
            else:  # I know this is dumb
                print("?", end=" ")
        print()


def GenerateCreatures(creature_id):
    while True:
        pray_amount = int(input("Amount of pray? "))
        predator_amount = int(input("Amount of predators? "))
        # safety check so the map will not be over 100% of the amount of map tiles
        plant_amount = pray_amount  # for now 1 to 1 ratio
        if pray_amount + predator_amount + plant_amount > MapDimensions * MapDimensions:
            print("Too many creatures")
            continue
        if pray_amount > 0 or predator_amount > 0:
            print(f"{pray_amount + predator_amount + plant_amount} Objects to be initialised")
            break
    GenerateCreatures.CreatureId = creature_id

    for i in range(pray_amount):
        CreatureList.append(Pray("Prey", False, GenerateCreatures.CreatureId))
        GenerateCreatures.CreatureId += 1

    for i in range(predator_amount):
        CreatureList.append(Predator("Predator", False, GenerateCreatures.CreatureId))
        GenerateCreatures.CreatureId += 1

    for i in range(plant_amount):
        CreatureList.append(Plant("Plant", False, GenerateCreatures.CreatureId))
        GenerateCreatures.CreatureId += 1

    global Map

    for i in range(CreatureList.__len__()):
        while True:
            CreatureList[i].position_x = random.randint(0, MapDimensions-1)
            CreatureList[i].position_y = random.randint(0, MapDimensions-1)  # do it using the creature position instead of map field

            # If it is something else than a None field, aka creature
            # re-roll positions, if not break and put it on the map
            if Map[CreatureList[i].position_x][CreatureList[i].position_y] is not None:
                continue
            else:
                break
            # ^ why did I implement this twice, but in a different way?
        Map[CreatureList[i].position_x][CreatureList[i].position_y] = CreatureList[i]


def CreatureActions():
    # CreatureList = sorted(CreatureList, key=lambda item: item.id)  # is this actually necessary or wanted
    for i in range(CreatureList.__len__()):
        if CreatureList[i].creature_type is not "Plant":
            CreatureList[i].move(random.randint(0, 4), Map, CreatureList)
        # don't know if this should be included
        Map[CreatureList[i].position_x][CreatureList[i].position_y] = CreatureList[i]


def EndPrint(generation):
    string = "  "
    bridge_line = ""
    for i in range(Map.__len__()):
        string = string + str(i) + " "
        bridge_line = "_"*string.__len__()
    print(bridge_line)
    print(generation)
    print(string)

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

# GenerateFirstMapGeneration()
GenerateCreatures(CreatureIdOuter)  # generate creatures before going into the game loop
while True:
    test_iterator += 1
    # CreatureIdOuter = GenerateCreatures.CreatureId  # gets out the creature id from the function
    # GenerateCreatures.CreatureId = GenerateCreatures.CreatureId + 100
    # ^THIS works, but does it work how I think it works?
    # GenerateCreatures(GenerateCreatures.CreatureId)
    CreatureActions()
    UpdateMap()
    DisplayMap()
    time.sleep(1)
    EndPrint(test_iterator)
    # clearConsole()
