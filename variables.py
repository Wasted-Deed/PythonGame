#общие переменные

SPRITE_SCALING = 0.5 #берём 50% размера от исходного файла
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Play"
MOVEMENT_SPEED = 200 /60 *SPRITE_SCALING #скорость перса
GUARD_SPEED = 60 / 30 *SPRITE_SCALING

sp_coordinates_guards = [(337, 337)]  #координаты охранников
sp_coordinates_field = [] #координаты всего поля
for i in range(int(SCREEN_WIDTH/25) + 1):
    for j in range(int(SCREEN_HEIGHT/25) + 1):
        sp_coordinates_field.append((25*i, 25*j))