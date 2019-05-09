from random import randint

import arcade.key

DIR_STILL = 0
DIR_UP = 1
DIR_DOWN = 3
DIR_RIGHT = 2
DIR_LEFT = 4

DIR_OFFSETS = {DIR_STILL: (0, 0), DIR_RIGHT: (1, 0), DIR_LEFT: (-1, 0), DIR_UP: (0, 1), DIR_DOWN: (0, -1)}

MOVEMENT_SPEED = 7

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

def is_hit(player_x, player_y, diamond_x, diamond_y):
    if diamond_y - 20 <= player_y + 20:
        if diamond_y + 20 <= player_y - 20:
            return False
        if player_x - 20 <= diamond_x +20 and diamond_x - 20 <= player_x + 20:
            return True
    return False


class Player:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.directon = DIR_STILL

    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]        

    def update(self, delta):
        self.move(self.directon)

class MeteorBig:
    METEOR_SPEED = 2

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vy = 0.2

    def up_speed(self):
        MeteorBig.METEOR_SPEED += self.vy    

    def update(self, delta):
        self.y -= MeteorBig.METEOR_SPEED
        if self.y < -20:
            self.y = SCREEN_HEIGHT
            self.x = randint(50, 400)
    def hit(self, player):
        return is_hit(player.x, player.y, self.x, self.y)

class Meteor:
    METEOR_SPEED = 1
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.temp = 200

    def update(self,delta):
        self.y -= Meteor.METEOR_SPEED
        if self.y < -20:
            self.y = SCREEN_HEIGHT
            self.x = randint(50, 350)

    def hit(self, player):
        return is_hit(player.x, player.y, self.x, self.y)

class World:
    STATE_STOP = 1
    STATE_START = 2
    STATE_DEAD = 3

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(self, width // 2, height // 6)
        self.state = World.STATE_STOP
        self.diamond = [
            Diamond(self, width - 100, height),
            Diamond(self, width - 200, height + 100),
            Diamond(self, width - 250, height + 200),
            Diamond(self, width - 300, height + 300),
            Diamond(self, width - 200, height + 400)]

        self.meteorbig = [MeteorBig(self, width // 4, height + 100),
                    MeteorBig(self, width // 2, height + 300),
                    MeteorBig(self, width // 6, height + 400)]

        self.meteor = [Meteor(self,width//2 ,height + 50), 
                    Meteor(self,width//4 ,height + 200)]

        self.score = 0
        self.level = 1
        self.level_meteor_big = 5
        self.level_meteor = 1
        self.hp = 4
        self.st = False

    def increase_score(self):
        self.score += 1

    def get_score(self):
        return self.score

    def get_level(self):
        return self.level

    def up_level(self):
        if self.get_score() % 7 == 0:
            self.level += 1
            for i in self.diamond:
                i.up_speed()

    def start(self):
        self.state = World.STATE_START

    def freeze(self):
        self.state = World.STATE_STOP

    def is_start(self):
        return self.state == World.STATE_START
    
    def start_new_game(self):
        if self.st == True:
            Diamond.DIAMOND_SPEED = 1
            for i in self.diamond:
                temp = randint(100, 400)
                i.y = SCREEN_HEIGHT+temp
            for i in self.meteorbig:
                temp_meteorbig = randint(100, 400)
                i.y = SCREEN_HEIGHT+temp_meteorbig
            for i in self.meteor:
                temp_meteor = randint(100, 350)
                i.y = SCREEN_HEIGHT+temp_meteor
            self.st = False

    def limit_screen(self, width, height):
        if self.player.x >= width:
            self.player.x = 0
        elif self.player.x <= 0:
            self.player.x = width

        if self.player.y >= height:
            self.player.y = 0
        elif self.player.y <= 0:
            self.player.y = height


    def die(self):
        self.state = World.STATE_DEAD

    def is_dead(self):
        return self.state == World.STATE_DEAD
    
    def player_hit(self):
        if not self.hp < 0:
            self.hp -= 1

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.RIGHT:
            self.player.directon = DIR_RIGHT
        if key == arcade.key.LEFT:
            self.player.directon = DIR_LEFT
        if key == arcade.key.UP:
            self.player.directon = DIR_UP
        if key == arcade.key.DOWN:
            self.player.directon = DIR_DOWN
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.directon = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.directon = 0

    def update(self, delta):
        if self.state in [World.STATE_STOP, World.STATE_DEAD]:
            return

        self.player.update(delta)
        
        if self.get_level() >= self.level_meteor_big:
            for j in self.meteorbig:
                j.update(delta)
                if j.hit(self.player):
                    j.y = SCREEN_HEIGHT
                    self.player_hit()

        for i in self.diamond:
            i.update(delta)
            if i.hit(self.player):
                self.increase_score()
                self.up_level()
                i.y = SCREEN_HEIGHT
                i.random_position()

        if self.get_level() >= self.level_meteor:
            for k in self.meteor:
                k.update(delta)
                if k.hit(self.player):
                    k.y = SCREEN_HEIGHT
                    self.player_hit()
        
        self.start_new_game()


class Diamond:
    DIAMOND_SPEED = 1

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vy = 0.1

    def up_speed(self):
        Diamond.DIAMOND_SPEED += self.vy

    def is_position_negative(self):
        if self.y < 0:
            self.y = 0

    def update(self, delta):
        self.y -= Diamond.DIAMOND_SPEED
        if self.y < -20:
            self.y = SCREEN_HEIGHT
            self.x = randint(50, 400)

    def hit(self, player):
        return is_hit(player.x, player.y, self.x, self.y)

    def random_position(self):
        self.x = randint(50, 400)