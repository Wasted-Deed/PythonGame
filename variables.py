#общие переменные

SPRITE_SCALING = 0.5 #берём 50% размера от исходного файла
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Play"
MOVEMENT_SPEED = 200 /60 *SPRITE_SCALING #скорость перса
GUARD_SPEED = 60 / 60 *SPRITE_SCALING

sp_coordinates_guards = [(337.5, 337.5)]  #координаты охранников
sp_coordinates_field = [] #координаты всего поля
sp_field = []
for i in range(int(SCREEN_WIDTH/25)):
    for j in range(int(SCREEN_HEIGHT/25)):
        sp_coordinates_field.append((12.5+25*i, 12.5+25*j)) 
for i in range(int(SCREEN_WIDTH/25)):
    for j in range(int(SCREEN_HEIGHT/25)):
        sp_field.append((i, j))
#print(sp_coordinates_field, end = " ")
#print(sp_field, end = " ")