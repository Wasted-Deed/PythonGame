import arcade
import os
from math import atan2, sin, cos, sqrt
from variables import *

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

class Bullet(arcade.Sprite): #стрельба перса, путём сложных вычислений перс теперь стреляет
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
        self.atk = 150
        
    def update(self):
        self.center_x += SPEED_BULLET * cos(self.angle_rad)
        self.center_y += SPEED_BULLET * sin(self.angle_rad)