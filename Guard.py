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
        self.max_hp = 5 * 60
        self.hp = self.max_hp
        self.player_x = player_x
        self.player_y = player_y
        self.speed = GUARD_SPEED
        x = self.center_x - self.player_x
        y = self.center_y - self.player_y
        self.r = sqrt(x * x + y * y)
        self.atk = 90 / 60
        self.a = []   # 2 5 8   
                      # 1 4 7   - порядок индексов направления в списке
                      # 0 3 6 
        self.pos = (self.center_x, self.center_y)

    def guard_field(self):
        for i in self.a:
            arcade.draw_point(i[0], i[1], arcade.color.RED, 3)
    
    def update(self):
        if (self.center_x, self.center_y) in sp_coordinates_field:
            self.a.clear()
            for i in sp_coordinates_field:
                if (i[0] - self.center_x) > -37.5 and (i[0] - self.center_x) < 37.5:
                    if (i[1] - self.center_y) > -37.5 and (i[1] - self.center_y) < 37.5:
                        if len(self.a) < 9:
                            self.a.append(i)
                


        self.r = 0
        if self.r > 220:
            if self.center_x < 462.5:
                self.center_x += self.speed
        elif self.r > 25 and self.r < 220: #  гг в зоне видимости
            if self.center_x > self.player_x and self.center_y == self.player_y: #влево
                self.center_x -=  self.speed
            elif self.center_x > self.player_x:
                self.center_x -= self.speed
            if self.center_x < self.player_x and self.center_y == self.player_y: #вправо
                self.center_x +=  self.speed
            elif self.center_x < self.player_x:
                self.center_x += self.speed
            if self.center_y > self.player_y and self.center_x == self.player_x : #вверх
                self.center_y -=  self.speed
            elif self.center_y > self.player_y: 
                self.center_y -= self.speed
            if self.center_y < self.player_y and self.center_x == self.player_x: #вниз
                self.center_y +=  self.speed 
            elif self.center_y < self.player_y: 
                self.center_y += self.speed              