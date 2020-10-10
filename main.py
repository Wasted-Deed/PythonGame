import arcade
import os
from math import atan2, sin, cos, sqrt
SPRITE_SCALING = 0.5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Play"
sp_coordinates_guards = [(80, 430),(130, 430),
                        (80, 370),(130, 370)]

MOVEMENT_SPEED = 10 *SPRITE_SCALING 


class Player(arcade.Sprite):
    def __init__(self):
        HERO_SCALING = 1.0 *SPRITE_SCALING
        super().__init__("images/hero.png", SPRITE_SCALING, hit_box_algorithm = 'Detailed')
        self.hp = 15 * 60
        
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

    def update_angle(self, mouse_pos):
        self.radians = atan2(mouse_pos['y'] - self.center_y, mouse_pos['x'] - self.center_x)

class Guard(arcade.Sprite):
    def __init__(self, x, y, player_x, player_y):
        GUARD_SCALING = 0.25 *SPRITE_SCALING
        super().__init__("images/guard.png", GUARD_SCALING, hit_box_algorithm = 'Detailed')
        self.center_x = x
        self.center_y = y
        self.hp = 60 * 5
        self.player_x = player_x
        self.player_y = player_y
    
    def update(self):
        x = self.center_x - self.player_x
        y = self.center_y - self.player_y
        r = sqrt(x * x + y * y)
        if self.center_x < 450:
            self.center_x += 10/60

class Bullet(arcade.Sprite):
    global BULLET_SCALING, DISTANCE_FROM_PLAYER, SPEED_BULLET, BULLET_DAMAGE
    BULLET_DAMAGE = 150 
    BULLET_SCALING = 0.15 *SPRITE_SCALING
    DISTANCE_FROM_PLAYER = 30 *SPRITE_SCALING
    SPEED_BULLET = 10 *SPRITE_SCALING
    
    def __init__(self, hero_pos, mouse_pos):
        super().__init__("images/bullet.png", BULLET_SCALING, hit_box_algorithm = 'Detailed')
        self.angle_rad = atan2(mouse_pos['y'] - hero_pos['y'], mouse_pos['x'] - hero_pos['x'])
        self.center_x = hero_pos['x'] + DISTANCE_FROM_PLAYER * cos(self.angle_rad)
        self.center_y = hero_pos['y'] + DISTANCE_FROM_PLAYER * sin(self.angle_rad)
        self.radians = self.angle_rad
        
    def update(self):
        self.center_x += SPEED_BULLET * cos(self.angle_rad)
        self.center_y += SPEED_BULLET * sin(self.angle_rad)

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
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        self.guards_list = arcade.SpriteList()
        for i in range(len(sp_coordinates_guards)):
            x, y = sp_coordinates_guards[i]
            self.guards_sprite = Guard(x, y, self.player_sprite.center_x, self.player_sprite.center_y)
            self.guards_list.append(self.guards_sprite)

        self.bullet_list = arcade.SpriteList()
        hero = self.player_sprite
        self.mouse_pos = {'x': hero.center_x, 'y': hero.center_y, 'dx': 0, 'dy': 0, 'button': 0}


        self.all_sprites = arcade.SpriteList()
        self.all_sprites.extend(self.player_list)
        self.all_sprites.extend(self.guards_list)
        self.all_sprites.extend(self.bullet_list)
        print(self.all_sprites)

    def on_draw(self):
        arcade.start_render()
        self.all_sprites.draw()
        #self.guards_list.draw()
        #self.player_list.draw()
        #self.bullet_list.draw()

    def shot(self):
        if self.mouse_pos['button'] == 1:
            hero = self.player_sprite
            one_bullet = Bullet({'x': hero.center_x, 'y': hero.center_y}, self.mouse_pos)
            self.bullet_list.append(one_bullet)
            self.all_sprites.append(one_bullet)

    def on_update(self, delta_time):
        self.player_list.update()
        self.guards_list.update()
        for guard in self.guards_list:
            guard.player_x = self.player_sprite.center_x
            guard.player_y = self.player_sprite.center_y
        self.player_sprite.update_angle(self.mouse_pos)
        self.shot()
        self.bullet_list.update()

        guards_punch_list = arcade.check_for_collision_with_list(self.player_sprite, self.guards_list)
    
        for guard in guards_punch_list:
            guard.hp -= 1  
            self.player_sprite.hp -= 1
            if guard.hp < 1:
                self.guards_list.remove(guard)
                self.all_sprites.remove(guard)

        for bullet in self.bullet_list:
            all_shot_list = arcade.check_for_collision_with_list(bullet, self.all_sprites)
            guards_shot_list = arcade.check_for_collision_with_list(bullet, self.guards_list)
            for item in guards_shot_list:
                self.bullet_list.remove(bullet)
                self.all_sprites.remove(bullet)
            for guard in guards_shot_list:
                guard.hp -= 150
                if guard.hp < 1:
                    self.guards_list.remove(guard)
                    self.all_sprites.remove(guard)
                
        self.mouse_pos['button'] = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = {'x': x, 'y': y, 'dx': dx, 'dy': dy, 'button': 0}

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_pos['button'] = button


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
