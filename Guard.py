import arcade
import os
from math import sqrt, ceil
from variables import *

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

class Guard(arcade.Sprite):#класс охранников
    def __init__(self, x, y, player_x, player_y):
        GUARD_SCALING = 0.25 *SPRITE_SCALING
        super().__init__("images/guard.png", GUARD_SCALING, hit_box_algorithm = 'Detailed')
        self.center_x = x
        self.center_y = y
        self.max_hp = 60 * 5
        self.hp = self.max_hp
        self.player_x = player_x
        self.player_y = player_y
        print(self.height, self.width)
    
    def update(self):
        x = self.center_x - self.player_x
        y = self.center_y - self.player_y
        r = sqrt(x * x + y * y)
        if r > 220:
            if self.center_x < 450:
                self.center_x += 30/60
        elif r > 40 and r < 220: #  гг в зоне видимости
            #if x > y and (x != 0 and y != 0):
                if self.center_x > self.player_x: #влево
                    self.center_x -= 30/60
                if self.center_x < self.player_x: #вправо
                    self.center_x += 30/60
            #elif y > x and (x != 0 and y != 0):
                if self.center_y > self.player_y: #вверх
                    self.center_y -= 30/60
                if self.center_y < self.player_y: #вниз
                    self.center_y += 30/60                
        else: # гг на расстоянии рукопашного боя
            pass 
