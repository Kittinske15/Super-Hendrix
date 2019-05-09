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

class ObjectSprite:
    def __init__(self, image, model):
        self.model = model
        self.object_sprite = arcade.Sprite(image)
    
    def draw(self):
        self.object_sprite.set_position(self.model.x, self.model.y)
        self.object_sprite.draw()

class HendrixWindow(arcade.Window):
    DELAY = 5
    diamonds_path = 'images/diamonds.png'
    meteor_path = 'images/meteor.png'
    meteor_big_path = 'images/meteor_big.png'
    superman_path = 'images/hendrix.png'
    first_back = 'images/1.jpeg'
    heart_path = 'images/heart.png'

    def __init__(self, width, height):
        print("init")
        super().__init__(width, height)
        self.background = arcade.load_texture(self.first_back)
        print("pass background")
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        print("pass world")
        self.dot_sprite = ModelSprite(self.superman_path, model=self.world.player)
        print("pass player")
        self.meteor_sprite = self.create_object(2,self.meteor_path)
        print("pass meteor")
        self.diamond_sprite = self.create_object(5,self.diamonds_path)
        print("pass diamond")
        self.meteor_big_sprite = self.create_object(3,self.meteor_big_path)
        print("pass big meteor")
        self.hp = self.create_hearts()
        print("pass heart")
        self.num_hp = 4
        print("pass num hp")
        self.menus = {'gameover': arcade.load_texture("images/gameover.png"),
                      'play': arcade.load_texture("images/play.png")}
        self.count = 0
        self.temp_player = 1
        print("exit init")

    def create_object(self, amount, image_path):
        print("create object")
        temp = []
        for i in range(amount):
            if image_path == self.diamonds_path:
                print("create diamond")
                temp.append(ObjectSprite(image_path,model=self.world.diamond[i]))
            elif image_path == self.meteor_path:
                print("create meteor")
                temp.append(ObjectSprite(image_path,model=self.world.meteor[i]))
            elif image_path == self.meteor_big_path:
                print("create big meteor")
                temp.append(ObjectSprite(image_path,model=self.world.meteorbig[i]))
        print("exit create object")
        return temp

    def create_hearts(self):
        print("enter create heart")
        temp = []
        for i in range(5):
            print("load heart")
            arcade.load_texture("images/heart.png")
        print("exit create heart")
        return temp

    def setup(self):
        print("enter set up")
        self.background = arcade.load_texture(self.first_back)
        self.hp = self.create_hearts()
        self.num_hp = 4
        self.world.level = 1
        self.world.score = 0
        self.world.hp = 4
        self.world.level_meteor_big = 5
        self.world.level_meteor = 1
        self.meteor_sprite = self.create_object(2,self.meteor_path)
        self.dot_sprite = ModelSprite(self.superman_path, model=self.world.player)
        print("exit set up")

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
        for k in self.meteor_sprite:
            k.draw()


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

    def start():
        window = HendrixWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.set_window(window)
        arcade.run()
