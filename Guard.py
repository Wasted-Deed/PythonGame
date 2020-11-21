import arcade
import os
from math import sqrt
from variables import sp_field, SPRITE_SCALING, GUARD_SPEED
from A_star_search import *
import time

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

class Guard(arcade.Sprite):#класс охранников
    def __init__(self, x, y, player_x, player_y):
        GUARD_SCALING = 0.25 *SPRITE_SCALING
        super().__init__("images/guard.png", GUARD_SCALING, hit_box_algorithm = 'Detailed')
        self.center_x = x
        self.center_y = y
        self.pos = (x, y)
        self.posf = ((x - 12.5) / 25, (y - 12.5) / 25)
        self.max_hp = 5 * 60
        self.hp = self.max_hp
        self.pos_player = (player_x, player_y)
        self.speed = GUARD_SPEED
        self.r = 0
        self.atk = 90 / 60
        self.start_time = time.time()
        self.sp = []
        self.count = 0
        self.flag_time = False
    
    def update(self):
        self.pos = (int(self.center_x) + 0.5, int(self.center_y) + 0.5)

        x = self.center_x - self.pos_player[0]
        y = self.center_y - self.pos_player[1]
        self.r = sqrt(x * x + y * y)
        if self.r < 220:
            if int(time.time() - self.start_time) == 1:
                self.start_time = time.time()
                self.asd()
                self.count = 0
            if len(self.sp) != 0:
                if self.posf != self.sp[self.count]:
                    a = self.sp[0]
                elif self.posf == self.sp[0]:
                    self.count += 1
                    a = self.sp[self.count]
                if (a[0] - self.posf[0]) > 0: # d
                    self.center_x += self.speed
                elif (a[0] - self.posf[0]) < 0: # a
                    self.center_x -= self.speed
                elif (a[1] - self.posf[1]) > 0: # w
                    self.center_y += self.speed
                elif (a[1] - self.posf[1]) <0: # s
                    self.center_y -= self.speed
        else:
            self.start_time = time.time()

    def asd(self):
        self.posf = (int((self.pos[0] - 12.5) / 25), int((self.pos[1] - 12.5) / 25))
        player = (int((self.pos_player[0] - 12.5) / 25), int((self.pos_player[1] -12.5) / 25))
        self.sp = reconstruct_path(a_star_search(field, self.posf, player), self.posf, player)
        del self.sp[0], self.sp[0]
