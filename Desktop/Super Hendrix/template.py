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
        self.coin_sprite = arcade.Sprite('images/diamonds.png')

    def draw(self):
        self.coin_sprite.set_position(self.model.x, self.model.y)
        self.coin_sprite.draw()


if __name__ == '__main__':
    window = SpaceGameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()