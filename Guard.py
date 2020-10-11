import arcade
import os
from math import sqrt
from variables import *

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

class Guard(arcade.Sprite):#класс охранников
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
            self.center_x += 30/60