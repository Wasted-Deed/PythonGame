import arcade
import os
from variables import SPRITE_SCALING, GUARD_SPEED
import time
from math import sqrt

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

class Guard(arcade.Sprite):#класс охранников
    def __init__(self, x, y, player_x, player_y, blocks, sprite=None):
        GUARD_SCALING = 0.25 *SPRITE_SCALING
        self.image = "images/guard.png"
        super().__init__(self.image, GUARD_SCALING, hit_box_algorithm = 'Detailed')
        self.center_x = x
        self.center_y = y
        self.max_hp = 5 * 60
        self.hp = self.max_hp
        self.pos_player = (player_x, player_y)
        self.speed = GUARD_SPEED
        self.atk = 90 / 60
        self.sp = []
        self.count = 0
        self.start_time = time.time()
        self.blocks = blocks
        self.guard_sprite = sprite
        self.center_hit_box = (self.center_x, self.center_y)
    
    def update(self):
        if int(sqrt((self.center_x - self.pos_player[0])**2 + (self.center_y - self.pos_player[1])**2)) < 50:
            self.sp = []
            self.count = 0
        elif int(sqrt((self.center_x - self.pos_player[0])**2 + (self.center_y - self.pos_player[1])**2)) <= 212:
            if (time.time() - self.start_time) > 1:
                self.start_time = time.time()
                if (self.pos_player[0] - self.center_x) > 0:#d
                    self.a = arcade.AStarBarrierList(self.guard_sprite, self.blocks, 50, self.position[0], self.pos_player[0], self.position[1] - 150, self.pos_player[1] + 150)
                if (self.pos_player[0] - self.center_x) < 0:#a
                    self.a = arcade.AStarBarrierList(self.guard_sprite, self.blocks, 50, self.pos_player[0], self.position[0],  self.position[1] - 150, self.pos_player[1] + 150)
                if (self.pos_player[1] - self.center_y) > 0:#w
                    self.a = arcade.AStarBarrierList(self.guard_sprite, self.blocks, 50, self.position[0] - 150, self.pos_player[0] + 150, self.position[1], self.pos_player[1])
                if (self.pos_player[1] - self.center_y) < 0:#s
                    self.a = arcade.AStarBarrierList(self.guard_sprite, self.blocks, 50, self.position[0] - 150, self.pos_player[0] + 150, self.pos_player[1], self.position[1])
                self.sp = arcade.astar_calculate_path(self.position, self.pos_player, self.a)
        elif int(sqrt((self.center_x - self.pos_player[0])**2 + (self.center_y - self.pos_player[1])**2)) > 212:
            self.sp = []
            self.count = 0
        if self.sp != None:
            if len(self.sp) > 2 and self.count <  len(self.sp):
                if self.position != self.sp[self.count]:
                    a = self.sp[self.count]
                elif self.position == self.sp[self.count]:
                    self.count += 1
                    a = self.sp[self.count]
                if (a[0] - self.position[0]) > 0: # d
                    self.center_x += self.speed
                elif (a[0] - self.position[0]) < 0: # a
                    self.center_x -= self.speed
                if (a[1] - self.position[1]) > 0: # w
                    self.center_y += self.speed
                elif (a[1] - self.position[1]) <0: # s
                    self.center_y -= self.speed

