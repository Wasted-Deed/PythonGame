import arcade
from variables import *
from random import randrange, getrandbits
import time 

'''
Поведение поезда
1) едет по намеченному пути 
3) останавливается при некотором условии
4) при столкновении в движении наносит урон.
5) звенья состава двигаются друг ха другом
'''

class Train(arcade.Sprite):

    def __init__(self, x_start, y_start, num):
        TRAIN_SCALING = 1.0 * SPRITE_SCALING
        self.image = "images/train.png"
        super().__init__(self.image, TRAIN_SCALING, hit_box_algorithm = 'Detailed', flipped_horizontally=True)
        self.center_x, self.center_y = x_start, y_start
        self.moved = True
        self.speed = TRAIN_SPEED
        self.wagon_list = arcade.SpriteList()
        self.create_wagons(num)
        self.draw()
        self.wagon_list.draw()

    def create_wagons(self, quantity: int):
        for i in range(1, quantity+1):
            distance = self.width * i # дистанция между центрами
            num = randrange(3) # вместо рандома потом здесь фиксироованные значения из списка для данного поезда 
            vagon = self.Wagon(num)
            vagon.center_x = self.center_x - distance
            vagon.center_y = self.center_y
            self.wagon_list.append(vagon)
    
    def go(self):
        self.speed = TRAIN_SPEED
        for wagon in self.wagon_list:
            wagon.speed = TRAIN_SPEED

    def stop(self):
        self.speed = 0
        for wagon in self.wagon_list:
            wagon.speed = 0

    def update(self):
        #if self.left >= SCREEN_WIDTH: self.stop()
        self.center_x += self.speed
        self.wagon_list.update()


    def draw_all(self):
        self.draw()
        self.wagon_list.draw()
    
    def append_all(self, list):
        list.append(self)
        list.extend(self.wagon_list)



    class Wagon(arcade.Sprite):
        def __init__(self, num): #передаём число от 0 до 3 (см. картинки)
            TRAIN_SCALING = 1.0 * SPRITE_SCALING
            self.image = F"images/vagon_{num}.png"
            super().__init__(self.image, TRAIN_SCALING, hit_box_algorithm = 'Detailed')     
            self.speed =  TRAIN_SPEED     
            self.jump = 0

        def update(self):
            if self.speed > 0:
                if not self.jump and randrange(1000)<20:
                    self.jump = time.time()
                    self.center_y += 2
                elif self.jump and time.time() - self.jump > 0.5:
                    self.center_y -= 2
                    self.jump = 0
                
            else:
                self.jump = 0
            self.center_x += self.speed