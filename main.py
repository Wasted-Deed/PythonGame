import arcade
import os
from math import atan2
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Play"

MOVEMENT_SPEED = 5 


class Player(arcade.Sprite):
    def __init__(self):
        HERO_SCALING = 3.0
        super().__init__("hero.png", SPRITE_SCALING*HERO_SCALING)
        
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

    def update_angle(self, mouse_list):
        self.radians = atan2(mouse_list['y'] - self.center_y, mouse_list['x'] - self.center_x)

class Guard(arcade.Sprite):
    def __init__(self):
        GUARD_SCALING = 0.5
        super().__init__("guard.png", SPRITE_SCALING*GUARD_SCALING)
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
    
    def update(self):
        pass

class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("guard.png", SPRITE_SCALING)

    def update(self):
        pass

class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.player_list = None
        self.player_sprite = None

        self.guards_list = None
        self.guards_sprite = None
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):

        self.player_list = arcade.SpriteList()
        self.player_sprite = Player()
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        self.guards_sprite = Guard()
        self.guards_list = arcade.SpriteList()
        self.guards_list.append(self.guards_sprite)

        self.mouse =arcade.View()
        self.mouse_pos = {'x': self.player_sprite.center_x, 'y': self.player_sprite.center_y, 'dx': 0, 'dy': 0}

    def on_draw(self):
        arcade.start_render()
        self.guards_list.draw()
        self.player_list.draw()
    

    def on_update(self, delta_time):
        self.guards_list.update()
        self.player_list.update()

        self.player_sprite.update_angle(self.mouse_pos)

        guards_hit_list = arcade.check_for_collision_with_list(self.player_sprite, 
          self.guards_list)
        for guard in guards_hit_list:
            guard.kill()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = {'x': x, 'y': y, 'dx': dx, 'dy': dy}


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
