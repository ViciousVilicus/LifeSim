import random


class Creature:
    starvationMAX = 6  # maximum amount of time before starvation

    def __init__(self, creature_type):
        self.creature_type = creature_type
        self.fed = True
        self.starvation = Creature.starvationMAX
        self.position_x = -1
        self.position_y = -1
        if creature_type == "Prey":
            self.speed = 1
        elif creature_type == "Predator":
            self.speed = 1  # 2 for later, when I will be able to implement it
        else:
            self.speed = 0  # cause plants and corpses

    consumables_list = []

    def reproduce(self, CreatureList, Map, MapDimensions):
        raise Exception("Creature has to have a subtype for this method to work")

    def consume(self, Map, CreatureList, landing_x, landing_y):
        raise Exception("Creature has to have a subtype for this method to work")

    def move(self, direction, Map, CreatureList):
        # 0 north, 1 east, 2 south, 3 west, 4 do not move
        if direction == 4:
            return

        def pick_a_spot(direction):
            direction_list = [direction]

            while True:
                # select wanted coordinates || REMEMBER !! wanted coordinates DO NOT BECOME actual coordinates !!
                if direction == 0:
                    wanted_y = self.position_y - self.speed
                    wanted_x = self.position_x
                elif direction == 1:
                    wanted_x = self.position_x - self.speed
                    wanted_y = self.position_y
                elif direction == 2:
                    wanted_y = self.position_y + self.speed
                    wanted_x = self.position_x
                elif direction == 3:
                    wanted_x = self.position_x + self.speed
                    wanted_y = self.position_y
                else:
                    raise ValueError("No such direction")

                wanted_x = wanted_x % Map.__len__()
                wanted_y = wanted_y % Map.__len__()

                # if on the wanted coordinates there is something
                if Map[wanted_x][wanted_y] is not None:
                    position_freed = self.consume(Map, CreatureList, wanted_x, wanted_y)
                    # try all directions (replacement directions)
                    if not position_freed:
                        while True:
                            random_direction = random.randint(0, 3)  # OPTIMISE THIS
                            # if the new direction is unique
                            if random_direction not in direction_list:
                                direction_list.append(random_direction)
                                direction = direction_list[direction_list.__len__() - 1]  # then it becomes the direction
                                break
                            # if all possible random numbers were tried, return from pick_a_spot with position_taken
                            if direction_list.__len__() == 4:
                                return (True,)
                    else:
                        return False, direction
                    continue  # comprehend this continue, when and what purpose it fulfills
                else:
                    return False, direction

        position_taken = pick_a_spot(direction)

        if not position_taken[0]:
            if position_taken[1] == 0:
                self.position_y = self.position_y - self.speed
            elif position_taken[1] == 1:
                self.position_x = self.position_x - self.speed
            elif position_taken[1] == 2:
                self.position_y = self.position_y + self.speed
            elif position_taken[1] == 3:
                self.position_x = self.position_x + self.speed

        self.position_x = self.position_x % Map.__len__()
        self.position_y = self.position_y % Map.__len__()

    def death_and_decay(self, CreatureList, Map, MapDimensions):
        # Death and decay is a timer before eventual death
        if self.fed:
            self.starvation = Creature.starvationMAX
            self.fed = False
            # TODO self.reproduce(CreatureList, Map, MapDimensions)
        else:
            if self.starvation <= 0:
                CreatureList.remove(self)  # will this work?  # Creature dies
            else:
                self.starvation -= 1


# Based of Predator
class Prey(Creature):
    consumables_list = ["Plant"]

    # Check if creature is allowed to eat target other creature type
    def consume(self, Map, CreatureList, landing_x, landing_y):
        if Map[landing_x][landing_y].creature_type in Prey.consumables_list:
            CreatureList.remove(Map[landing_x][landing_y])  # remove that creature from existence
            self.fed = True
            return True  # T or F if the spot was freed
        return False

    def reproduce(self, CreatureList, Map, MapDimensions):
        if self.starvation > Creature.starvationMAX / 2:
            if len(CreatureList) >= MapDimensions * MapDimensions:
                CreatureList.append(Prey("Prey"))
                while True:
                    CreatureList[-1].position_x = random.randint(0, MapDimensions - 1)
                    CreatureList[-1].position_y = random.randint(0, MapDimensions - 1)

                    # if not field_free or field_not_taken_by_self
                    if Map[CreatureList[-1].position_x][CreatureList[-1].position_y] is not None:
                        continue
                    else:
                        return


# Based of Prey
class Predator(Creature):
    consumables_list = ["Prey"]

    # Check if creature is allowed to eat target other creature type
    def consume(self, Map, CreatureList, landing_x, landing_y):
        if Map[landing_x][landing_y].creature_type in Predator.consumables_list:
            # Unknown cause of error: Predator attempts to remove a Prey that does not exist(somehow) but is on the map
            # I may have an idea, but I need more time to try that
            try:
                CreatureList.remove(Map[landing_x][landing_y])  # remove that creature from existence
                # if it was real, then
                self.fed = True
            except ValueError:
                pass
            return True  # T or F if the spot was freed
        return False

    def reproduce(self, CreatureList, Map, MapDimensions):
        if self.starvation > Creature.starvationMAX / 2:
            if len(CreatureList) >= MapDimensions*MapDimensions:
                CreatureList.append(Predator("Predator"))
                while True:
                    CreatureList[-1].position_x = random.randint(0, MapDimensions - 1)
                    CreatureList[-1].position_y = random.randint(0, MapDimensions - 1)

                    # if not field_free or field_not_taken_by_self
                    if Map[CreatureList[-1].position_x][CreatureList[-1].position_y] is not None:
                        continue
                    else:
                        return


class Plant(Creature):  # Bear with me
    # this should be a 'vegetable' aka exist, do nothing and not decide to stop existing by itself
    def move(self, direction, Map, CreatureList):
        raise Exception("A Plant cannot move")

    def reproduce(self, CreatureList, Map, MapDimensions):
        pass

    def death_and_decay(self, CreatureList, Map, MapDimensions):
        # Death and decay is a timer before eventual death
        if self.starvation <= 0:
            CreatureList.remove(self)  # will this work?  # Creature dies
        else:
            self.starvation -= 2


class Corpse(Creature):  # Copy of plant
    def move(self, direction, Map, CreatureList):
        raise Exception("A Corpse cannot move")
