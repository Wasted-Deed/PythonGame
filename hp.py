import arcade
from variables import *

def draw_hp(center_x, center_y, height, max_hp, hp):
        arcade.draw_rectangle_filled(
            center_x = center_x, 
            center_y = center_y - height *SPRITE_SCALING - 10,
            width = hp // 20,
            height = 10 *SPRITE_SCALING,
            color = [255, 0, 0],
        )
        arcade.draw_rectangle_outline(
            center_x = center_x , 
            center_y = center_y - height *SPRITE_SCALING -10,
            width = max_hp // 20,
            height = 10 *SPRITE_SCALING,
            color = [0, 0, 0],
            border_width = 3.0 *SPRITE_SCALING
        )