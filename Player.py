import arcade
import os
from math import atan2, sin, cos, sqrt
from variables import *

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


class Player(arcade.Sprite): #класс персанажа
    def __init__(self):
        HERO_SCALING = 1.0 *SPRITE_SCALING #отдельная переменная для размера срайта, если захотим отдельно от всех уменьшить\увеличить
        super().__init__("images/hero.png", HERO_SCALING, hit_box_algorithm = 'Detailed') #загружаем картинку и выставляем параметр
                                                        #чтобы спрайт блок охватывал именно очертания картинки
        self.max_hp = 15 * 60 #хп
        self.hp = self.max_hp
        self.hp_bar = self.hp // 10
    
    def update(self): # перемещение перса и проверки, чтобы за экран не выходил
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

    def update_angle(self, mouse_pos):# перс следит за мышкой
        self.radians = atan2(mouse_pos['y'] - self.center_y, mouse_pos['x'] - self.center_x)