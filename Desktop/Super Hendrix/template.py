import arcade

from models import Ship,World

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            self.angle = self.model.angle

    def draw(self):
        self.sync_with_model()
        super().draw()


class DiamondsSprite:
    def __init__(self,model):
        self.model = model
        self.diamond_sprite = arcade.Sprite('images/diamonds.png')

    def draw(self):
        self.diamond_sprite.set_position(self.model.x, self.model.y)
        self.diamond_sprite.draw()


class Window(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.background = arcade.load_texture("images/space.png")

        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dot_sprite = ModelSprite('images/player.png', model=self.world.player)
        self.diamond_sprite = [DiamondSprite(model=self.world.diamond[0]),DiamondSprite(model=self.world.diamond[1]),
                            DiamondSprite(model=self.world.diamond[2]),DiamondSprite(model=self.world.diamond[3]),
                            DiamondSprite(model=self.world.diamond[4])]

    def on_key_press(self, key, key_modifiers):
        if not self.world.is_start():
            self.world.start()
        self.world.on_key_press(key, key_modifiers)

    def update(self, delta):
        self.world.update(delta)
        self.world.limit_screen(SCREEN_WIDTH)

    def draw_background(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
    def draw_score(self):
        arcade.draw_text('Score : '+str(self.world.score),
                         self.width - 140,
                         self.height - 30,
                         arcade.color.BLACK,
                         20, )
    def draw_level(self):
        arcade.draw_text('Level : '+str(self.world.level),
                         self.width - 400,
                         self.height - 30,
                         arcade.color.BLACK,
                         20, )

    def on_draw(self):
        arcade.start_render()
        # Draw the background texture
        self.draw_background()
        for i in self.coin_sprite:
            i.draw()
        self.dot_sprite.draw()
        # Draw the score
        self.draw_score()
        #Draw level
        self.draw_level()



def main():
    window = KurbyWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()

def is_hit_diamonds(player_x, player_y, diamond_x, diamond_y):
    if diamond_y - 20 <= player_y + 20:
        if diamond_y + 20 <= player_y - 20:
            return False
        if player_x - 20 <= diamond_x +20 and diamond_x - 20 <= player_x + 20:
            return True
    return False


if __name__ == '__main__':
    main()