import arcade
import os
from variables import SPRITE_SCALING, GUARD_SPEED
from math import sqrt

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

class Guard(arcade.Sprite):#класс охранников
    def __init__(self, x, y):
        GUARD_SCALING = 0.25 *SPRITE_SCALING
        self.image = "images/guard.png"
        super().__init__(self.image, GUARD_SCALING, hit_box_algorithm = 'None')
        self.center_x = x
        self.center_y = y
        self.max_hp = 5 * 60
        self.hp = self.max_hp
        self.speed = GUARD_SPEED
        self.atk = 90 / 60
        self.count = 0
        self.barrier_list = None
        self.path = []                                           
    
    def update(self):
        if self.path != None:
            self.speed = GUARD_SPEED
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
        else:
            self.speed = 0

