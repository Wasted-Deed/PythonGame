import arcade
import os
from variables import SPRITE_SCALING, GUARD_SPEED
from math import sqrt

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

class Guard(arcade.Sprite):#класс охранников
    def __init__(self, x, y, player_x, player_y, blocks=None, sprite=None, wall=None):
        GUARD_SCALING = 0.25 *SPRITE_SCALING
        super().__init__("images/guard.png", GUARD_SCALING, hit_box_algorithm = 'Detailed')
        self.center_x = x
        self.center_y = y
        self.max_hp = 5 * 60
        self.hp = self.max_hp
        self.pos_player = (player_x, player_y)
        self.speed = GUARD_SPEED
        self.atk = 90 / 60
        self.count = 0
        self.barrier_list = blocks
        self.moving_sprite = sprite
        self.wall = wall
        self.path = None                                            
    
    def update(self):
        r = int(sqrt((self.center_x - self.pos_player[0])**2 + (self.center_y - self.pos_player[1])**2))
        if r <= 100:
            self.path = []
            self.count = 0
        elif r < 212:
            if arcade.has_line_of_sight(self.position, self.pos_player, self.wall, 1000):
                self.path = arcade.astar_calculate_path((self.center_x, self.center_y),
                                                    self.pos_player,
                                                    self.barrier_list,
                                                    diagonal_movement=False)
            else:
                self.path = []
                self.count = 0
        elif r >= 212:
            self.path = []
            self.count = 0
        if self.path != None:
            if len(self.path) > 2 and self.count <  len(self.path):
                if self.position != self.path[self.count]:
                    a = self.path[self.count]
                elif self.position == self.path[self.count]:
                    self.count += 1
                    a = self.path[self.count]
                if (a[0] - self.position[0]) > 0: # d
                    self.center_x += self.speed
                elif (a[0] - self.position[0]) < 0: # a
                    self.center_x -= self.speed
                if (a[1] - self.position[1]) > 0: # w
                    self.center_y += self.speed
                elif (a[1] - self.position[1]) <0: # s
                    self.center_y -= self.speed

