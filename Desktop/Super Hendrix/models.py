import arcade.key
from random import randint

class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0

    def hit(self, other, hit_size):
        return (abs(self.x - other.x) <= hit_size) and (abs(self.y - other.y) <= hit_size)

class Ship(Model):
    DIR_HORIZONTAL = 0
    DIR_VERTICAL = 1

    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)

        self.direction = Ship.DIR_VERTICAL

    def switch_direction(self):
        if self.direction == Ship.DIR_HORIZONTAL:
            self.direction = Ship.DIR_VERTICAL
            self.angle = 0
        else:
            self.direction = Ship.DIR_HORIZONTAL
            self.angle = -90

    def update(self, delta):
        if self.direction == Ship.DIR_VERTICAL:
            if self.y > self.world.height:
                self.y = 0
            self.y += 5
        else:
            if self.x > self.world.width:
                self.x = 0
            self.x += 5


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ship = Ship(self,100, 100)
        self.gold = Gold(self, 400, 400)
        self.score = 0

    def update(self, delta):
        self.ship.update(delta)

        if self.ship.hit(self.gold, 10):
            self.gold.random_location()
            self.score += 1

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            self.ship.switch_direction()


class Gold(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)

    def random_location(self):
        self.x = randint(0, self.world.width - 1)
        self.y = randint(0, self.world.height - 1)