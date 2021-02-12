#общие переменные

SPRITE_SCALING = 0.5 #берём 50% размера от исходного файла
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
SCREEN_TITLE = "Play"
MOVEMENT_SPEED = 200 /60 *SPRITE_SCALING #скорость перса
TRAIN_SPEED = 400 / 60 * SPRITE_SCALING
GUARD_SPEED = 60 / 30 *SPRITE_SCALING
s = (SCREEN_WIDTH, SCREEN_HEIGHT)

sp_coordinates_guards = [(337, 337), (450, 450)]  #координаты охранников
sp_coordinates_obstacles = [(0.5, 0.7), (0.5, 0.8)]

#def render_field(size):
#    a = []
#    for i in range(int(size[0]/10) + 1):
#        for j in range(int(size[1]/10) + 1):
#            a.append((10*i, 10*j))
#   return a
    
#sp_coordinates_field = render_field(s)