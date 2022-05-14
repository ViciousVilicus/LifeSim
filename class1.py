import random


class Creature:
    def __init__(self, creature_type, fed, creature_id):
        self.creature_type = creature_type
        self.fed = bool(fed)
        self.creature_id = int(creature_id)
        self.position_x = 0
        self.position_y = 0
        self.dead = False
        if creature_type == "Prey":
            self.speed = 1
        elif creature_type == "Predator":
            self.speed = 1  # 2 for later, when I will be able to implement it
        else:
            self.speed = 0  # cause plants

    consumables_list = []

    def consume(self, Map, CreatureList, landing_x, landing_y):
        raise Exception("Creature has to have a subtype to work")

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


class Pray(Creature):
    consumables_list = ["Plant"]

    def consume(self, Map, CreatureList, landing_x, landing_y):
        #  if Map[landing_x][landing_y] is not None:  I don't think this check is necessary
        if Map[landing_x][landing_y].creature_type in Pray.consumables_list:
            # del CreatureList[CreatureList.index(Map[landing_x][landing_y])] overcomplicated and dumb
            CreatureList.remove(Map[landing_x][landing_y])  # <-- PROBABLE CAUSE OF THE PROBLEM
            #CreatureList(CreatureList.index(Map[landing_x][landing_y])).dead = True


class Predator(Creature):
    consumables_list = ["Pray"]

    def consume(self, Map, CreatureList, landing_x, landing_y):
        if Map[landing_x][landing_y].creature_type in Predator.consumables_list:
            CreatureList.remove(Map[landing_x][landing_y])
            return True
        else:
            return False


class Plant(Creature):  # Bear with me
    # this should be a 'vegetable' aka exist, do nothing and not decide to stop existing by itself
    def move(self, direction, Map, CreatureList):
        raise Exception("A Plant cannot move")
