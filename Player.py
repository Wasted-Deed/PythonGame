import arcade
import os
from math import atan2, sin, cos, sqrt
from variables import *

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


class Player(arcade.Sprite): #класс персанажа
    def __init__(self):
        HERO_SCALING = 1.0 *SPRITE_SCALING #отдельная переменная для размера срайта, если захотим отдельно от всех уменьшить\увеличить
        self.filename = "images/hero.png"
        super().__init__(self.filename, HERO_SCALING, hit_box_algorithm = 'Detailed') #загружаем картинку и выставляем параметр
                                                        #чтобы спрайт блок охватывал именно очертания картинки
        self.max_hp = 15 * 60 #хп
        self.hp = self.max_hp
        self.hp_bar = self.hp // 10
        self.speed = MOVEMENT_SPEED
        self.center = 0
       

        self.bullet_now = 6
        self.first_field = [] #  . . .
                              #  . I . - точки для ближнего боя, где I - перс
                              #  . . .


        self.second_field = [] #  . . . . . . . . .
                               #  .               .
                               #  .               .
                               #  .               .
                               #  .       I       .
                               #  .               .
                               #  .               .
                               #  .               .
                               #  . . . . . . . . .
    
    def update(self): # перемещение перса и проверки, чтобы за экран не выходил
        if abs(self.change_x) > 0 and abs(self.change_y) > 0:
            self.center_x += self.change_x* sqrt(2)/2
            self.center_y += self.change_y* sqrt(2)/2
        else:
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
        
        self.player_field()

    def update_angle(self, mouse_pos):# перс следит за мышкой
        self.radians = atan2(mouse_pos['y'] - self.center_y, mouse_pos['x'] - self.center_x)
        
    def player_field(self):
        self.center= (12.5 + 25 * int(self.center_x / 25), 12.5 + 25 * int(self.center_y / 25))
        self.first_field.clear()
        self.second_field.clear()
        for i in range(-1, 2, 2):
            self.first_field.append((self.center[0] + 25*i, self.center[1] + 25*i))
            self.first_field.append((self.center[0] + 25*i, self.center[1]))
            self.first_field.append((self.center[0], self.center[1] + 25*i))
            self.first_field.append((self.center[0] - 25*i, self.center[1] + 25*i))
        
        for x in range(-4, 5, 8):
            for y in range(-4, 5):
                self.second_field.append((self.center[0] + 25*x, self.center[1] + 25*y))
        for y in range(-4, 5, 8):
            for x in range(-3, 4):
                self.second_field.append((self.center[0] + 25*x, self.center[1] + 25*y))
        for i in self.second_field:
            arcade.draw_point(i[0], i[1], arcade.color.BLUE, 2)