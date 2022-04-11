import random

class Creature:
  def __init__(self, type, fed, id):
    self.type = type
    self.fed = bool(fed)
    self.id = int(id)
    self.position_x = 0
    self.position_y = 0
    self.position_x_wanted = 0
    self.position_y_wanted = 0
    if type == "Prey":
        self.speed = 1
    elif type == "Predator":
        self.speed = 1 # 2 for later, when i will be able to implement it


  def move(self, direction, creature_list, map):
    # 0 north, 1 east, 2 south, 3 west, 4 do not move
    if direction == 4:
        return

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

    def pick_a_spot(direction):
        direction_list = []
        direction_list.append(direction)
        while True:
            # select wanted coordinates
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
            

            print(type(map[wanted_x][wanted_y]))
            # if on the wanted coordinates there is something
            if type(map[wanted_x][wanted_y]) is not type(None):
                # try all directions (replacement directions)
                while True:
                    random_direction = random.randrange(4)  # OPTIMISE THIS
                    # if the new direction is unique
                    if not random_direction in direction_list:
                        direction_list.append(random_direction)
                        direction = direction_list[direction_list.__len__()-1]  # then it becomes the direction
                        break
                    if direction_list.__len__() == 4: # if all possible random numbers were tried, return from pick_a_spot with positon_taken
                        return (True, )

                continue
            else:
                return (False, direction)

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


#class Prey(Creature):
#  def():



#class Predator(Creature):
