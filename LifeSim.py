import random
import time

from class1 import Creature

# tried arrays, they suck
# lists are just too cool

# Proper clear doesn't want to work, used the 'print a lot of lines' solution:
# Works but meh, on a bigger map it will be better
# Random doesn't want to work, no idea what is wrong, it worked on the monopoly one:
# My dumb ass was adding onto the list, but displaying only the first generation
# so great, made my first memory leak...
MapDimensions = 10
Map = [[None] * MapDimensions] * MapDimensions
CreatureList = []
# add creature id somewhere in the code later on
# PRIORITY - random restart seed
# CURRENT - add replacing of maps Nulls when creature is not present. Make a check on Out Of Bounds error when wanted coordinates are OoB

clearConsole = lambda: print('\n' * 150)

# do this --> https://stackoverflow.com/questions/19326004/access-a-function-variable-outside-the-function-without-using-global



def GenerateFirstMapGeneration():
    # why is this 'if' here? what scenario does it cover?
    # after 2 weeks I remember, this clears the map beforehand so there won't be a memory leak
    global Map

    if Map.__len__ != 0:
        Map.clear()
        Map = [[None] * MapDimensions] * MapDimensions  # this may not be necessary if I will make this solely for the first map generation

    for i in range(CreatureList.__len__()):
        while True:
            CreatureList[i].position_x = random.randrange(10)
            CreatureList[i].position_y = random.randrange(10) # do it using the creature position instead of map field

            # If it is something else than a None field, aka creature re-roll positions, if not break and put it on the map
            if type(Map[CreatureList[i].position_x][CreatureList[i].position_y]) is not type(None):
                continue
            else:
                break
            # ^ why did i implement this twice, but in a different way?

        Map[CreatureList[i].position_x][CreatureList[i].position_y] = CreatureList[i]



def DisplayMap():
    for col in range(MapDimensions):
        print(f"{col}", end=" ")
        for row in range(MapDimensions):
            # Big problem/security flaw here. What if the error will be a valid one?
            try:
                if Map[col][row].type == "Prey":
                    print("X", end=" ")
                if Map[col][row].type == "Predator":
                    print("Z", end=" ")
            except:
                print(" ", end=" ")
        print()



def GenerateCreatures(CreatureIdOuter):
    while True:
        pray_amount = int(input("Amount of pray? "))
        predator_amount = int(input("Amount of predators? "))
        # safety check so the map will not be over 100% of the amount of map tiles
        if pray_amount + predator_amount > MapDimensions * MapDimensions:
            print("Too many creatures")
            continue
        if pray_amount > 0 or predator_amount > 0:
            break
    GenerateCreatures.CreatureId = CreatureIdOuter

    for i in range(pray_amount):
        CreatureList.append(Creature("Prey", False, GenerateCreatures.CreatureId))
        GenerateCreatures.CreatureId += 1


def CreatureActions():
    #CreatureList = sorted(CreatureList, key=lambda item: item.id)  # is this actually necessary
    for i in range(CreatureList.__len__()):
        CreatureList[i].move(random.randrange(5), CreatureList, Map)
        Map[CreatureList[i].position_x][CreatureList[i].position_y] = CreatureList[i]



# how I can do this,
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
while True:
    random.seed(time.localtime())
    test_iterator += 1
    if test_iterator == 100:
        break
    GenerateCreatures(CreatureIdOuter)
    CreatureIdOuter = GenerateCreatures.CreatureId  # gets out the creature id from the function
    # GenerateCreatures.CreatureId = GenerateCreatures.CreatureId + 100  # THIS works, but does it work how I think it works?
    # GenerateCreatures(GenerateCreatures.CreatureId)
    GenerateFirstMapGeneration()
    DisplayMap()
    # CreatureActions()
    # DisplayMap()
    time.sleep(1)
    clearConsole()
