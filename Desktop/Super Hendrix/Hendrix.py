import arcade

from models import Player, World, Diamond

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model", None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()


class DiamondSprite:
    def __init__(self, model):
        self.model = model
        self.diamond_sprite = arcade.Sprite('images/diamonds.png')

    def draw(self):
        self.diamond_sprite.set_position(self.model.x, self.model.y)
        self.diamond_sprite.draw()


class MeteorbigSprite:
    def __init__(self, model):
        self.model = model
        self.meteor_big_sprite = arcade.Sprite('images/meteor_big.png')

    def draw(self):
        self.meteor_big_sprite.set_position(self.model.x, self.model.y)
        self.meteor_big_sprite.draw()


class MeteorSprite:
    def __init__(self, model):
        self.model = model
        self.meteor_sprite = arcade.Sprite('images/meteor.png')

    def draw(self):
        self.meteor_sprite.set_position(self.model.x, self.model.y)
        self.meteor_sprite.draw()


class HendrixWindow(arcade.Window):
    DELAY = 5
    temp_list = []

    def __init__(self, width, height):
        super().__init__(width, height)

        self.background = arcade.load_texture("images/1.jpeg")

        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dot_sprite = ModelSprite(
            'images/hendrix.png', model=self.world.player)
        self.meteor_sprite = MeteorSprite(model=self.world.meteor)
        self.diamond_sprite = [DiamondSprite(model=self.world.diamond[0]), DiamondSprite(model=self.world.diamond[1]),
                               DiamondSprite(model=self.world.diamond[2]), DiamondSprite(
                                   model=self.world.diamond[3]),
                               DiamondSprite(model=self.world.diamond[4])]
        self.meteor_big_sprite = [MeteorbigSprite(model=self.world.meteorbig[0]), MeteorbigSprite(model=self.world.meteorbig[1]),
                                  MeteorbigSprite(model=self.world.meteorbig[2])]
        self.hp = [arcade.load_texture("images/heart.png"), arcade.load_texture(
            "images/heart.png"), arcade.load_texture("images/heart.png")]
        self.num_hp = 2
        self.menus = {'gameover': arcade.load_texture("images/gameover.png"),
                      'play': arcade.load_texture("images/play.png")}
        self.count = 0
        self.temp_player = 1

    def setup(self):
        self.background = arcade.load_texture("images/1.jpeg")
        self.hp = [arcade.load_texture("images/heart.png"), arcade.load_texture(
            "images/heart.png"), arcade.load_texture("images/heart.png")]
        self.num_hp = 2
        self.world.level = 0
        self.world.score = 0
        self.world.hp = 2
        self.world.level_meteor_big = 5
        self.world.level_meteor = 2
        self.monster_sprite.monster_sprite = arcade.Sprite('images/meteor.png')
        self.dot_sprite = ModelSprite('images/player.png', model=self.world.player)

    def on_key_press(self, key, key_modifiers):
        if not self.world.is_start():
            self.world.start()
        self.world.on_key_press(key, key_modifiers)
        if self.world.level >= 3:
            if self.temp_player == 2:
                self.temp_player = 1
            elif self.temp_player >= 1:
                self.temp_player = 2

    def night_back(self):
        if self.world.level >= 100:
            self.background = arcade.load_texture("images/bg.png")
            self.meteor_sprite.meteor_sprite = arcade.Sprite(
                'images/meteor.png')

    def update(self, delta):
        self.world.update(delta)
        self.world.limit_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.night_back()

    def draw_background(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

    def draw_detail(self):
        if self.world.level < 10:
            color = arcade.color.WHITE
        else:
            color = arcade.color.WHITE

        arcade.draw_text('Score : '+str(self.world.score),
                         self.width - 80,
                         self.height - 30,
                         color,
                         12, )

        arcade.draw_text('Level : '+str(self.world.level),
                         self.width - 400,
                         self.height - 30,
                         color,
                         12, )
        arcade.draw_text('HP : ',
                         self.width - 400,
                         self.height - 60,
                         color,
                         12, )
        temp = 0
        if self.world.hp != self.num_hp:
            self.hp.pop()
            self.num_hp = self.world.hp

        for i in self.hp:
            arcade.draw_texture_rectangle(
                self.width - 360+temp, self.height - 53, 10, 12, i)
            temp += 15

    def on_draw(self):
        arcade.start_render()
        self.draw_background()
        for i in self.diamond_sprite:
            i.draw()
        self.dot_sprite.draw()
        self.draw_detail()
        for j in self.meteor_big_sprite:
            j.draw()
        self.meteor_sprite.draw()

        if len(self.hp) == 0:
            self.world.die()
            texture = self.menus['gameover']
            arcade.draw_texture_rectangle(
                self.width//2, self.height//2 + 50, texture.width, texture.height, texture, 0)
            texture = self.menus['play']
            arcade.draw_texture_rectangle(
                self.width//2, self.height//2 - 100, texture.width, texture.height, texture, 0)

    def on_mouse_press(self, x, y, button, modifiers):
        if len(self.hp) == 0:
            texture = self.menus['play']
            h = self.height//2 - 100
            w = self.width//2
            if w - texture.width//2 <= x <= w + texture.width//2:
                if h - texture.height//2 <= y <= h + texture.height//2:
                    self.world.st = True
                    self.setup()
                    self.world.start()


def main():
    window = HendrixWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
