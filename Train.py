import arcade
from variables import *

'''
Поведение поезда
1) едет по намеченному пути 
2) всё, что находится внутри двигается стой же скоростью
3) останавливается при некотором условии
4) при столкновении в движении наносит урон.
5) звенья состава двигаются друг ха другом
'''
class Train(arcade.Sprite):

    def __init__(self):
        TRAIN_SCALING = 1.0 * SPRITE_SCALING
        super().__init__("images/train.png", TRAIN_SCALING, hit_box_algorithm = 'Detailed')
        self.moved = True

    def update(self):
        pass