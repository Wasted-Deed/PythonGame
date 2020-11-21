import arcade
from variables import *

class Rails(arcade.Sprite):
    def __init__(self):
        
        sp_rails = arcade.SpriteList()


    def update(self):
        pass

class Rail(arcade.Sprite):
    def __init__(self):
        RAILS_SCALING = 1.0 * SPRITE_SCALING
        super().__init__("images/rail.png", RAILS_SCALING, hit_box_algorithm = 'Detailed')
        