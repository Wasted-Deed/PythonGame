import arcade
import os
import time
from random import randint 
from PIL import Image
from math import atan2, sin, cos, sqrt, pi
from Guard import Guard
from Player import  Player
from variables import *
from Bullet import Bullet
from hp import draw_hp
from Train import Train

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)
#изменить отсчёт времени
#изменить стенки для героя 
#добавить охранникам стрельбу
#переработать стрельбу - зависает на первом выстреле
#увеличить хит-боксы, ибо выстрелы взаимодействуют с ними 

class MenuView(arcade.View):#меню

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Кликни, чтобы начать играть", window.get_size()[0]/2, window.get_size()[1]/2,
                         arcade.color.WHITE, font_size=30, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        game_view.setup() #загрузка ресурсов
        self.window.show_view(game_view)

class GameView(arcade.View):#игра

    def __init__(self):
        super().__init__()
        self.field = window.get_size()
        self.background = None
        self.player_sprite = None
        self.people_list = None
        self.guards_sprite = None
        self.blocks = None
        self.land = None
        self.time = 0
        self.start_time = time.time()
        self.recharge = False
        self.textures = []

    def setup(self):
        # препятствия
        self.blocks = arcade.SpriteList(use_spatial_hash=True, is_static=True)
        for block in sp_coordinates_obstacles:
            number = randint(1, 2)
            self.blocks.append(arcade.Sprite("images/obstacles/2-%d.png" % number, 1, center_x=block[0], center_y= block[1],
                                            hit_box_algorithm = "Detailed"))
            


        #путь поезда
        self.paint_reils_way_flag = False
        self.way_file = 'train_way.txt'
        self.way_list = []
        self.read_train_way()
        
        #поезд
        self.train = Train(0, 150, 12)

        #поле
        self.background = arcade.load_texture("images/земля.png")

        #персонаж
        self.people_list = arcade.SpriteList()
        self.player_sprite = Player() 
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 50       
        self.people_list.append(self.player_sprite)

        #охрана
        self.guards_list = arcade.SpriteList()
        for i in range(len(sp_coordinates_guards)):
            x, y = sp_coordinates_guards[i]
            self.guards_sprite = Guard(x, y)
            self.guards_sprite.barrier_list = arcade.AStarBarrierList(self.guards_sprite,
                                                                    self.blocks,
                                                                    20,
                                                                    0,
                                                                    window.get_size()[0],
                                                                    0,
                                                                    window.get_size()[1])
            self.guards_list.append(self.guards_sprite)
            self.people_list.append(self.guards_sprite)

        #пули
        self.bullet_list = arcade.SpriteList()
        hero = self.player_sprite
        self.mouse_pos = {'x': hero.center_x, 'y': hero.center_y, 'dx': 0, 'dy': 0, 'button': 0} #задаём координаты мышки

        #общий список
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.extend(self.people_list)
        self.all_sprites.extend(self.bullet_list)
        self.train.append_all(self.all_sprites)
        for thing in self.all_sprites:
            change_hit_box(thing)

    def paint_reils_way(self, update=False, end=False):  #длинная функция создания пути поезда - мы рисуем примерный путь поезда
        if update:
            list1 = self.way_list
            if len(list1) == 0:
                self.way_list.append([self.mouse_pos['x'], self.mouse_pos['y']])
            delta_x = (self.mouse_pos['x']-list1[-1][0])
            delta_y = (self.mouse_pos['y']-list1[-1][1])
            if sqrt((delta_x)**2 + (delta_y)**2) > 25:
                angle = atan2(delta_y, delta_x)
                self.way_list.append([25*cos(angle) + list1[-1][0], 25*sin(angle) + list1[-1][1]])
        if end:
            list_map = []
            file = open(self.way_file, 'w')
            for x, y in self.way_list:
                coord = (12.5 + 25 * int(x / 25), 12.5 + 25 * int(y / 25))
                if coord not in list_map:
                    if len(list_map) > 1:
                        if abs(list_map[-2][0] - coord[0]) == 25 and  abs(list_map[-2][1] - coord[1]) == 25:
                            print(F'между {list_map[-2]} {coord} del list_map[-1]')
                            del list_map[-1] 
                    list_map.append(coord)
            for coord in list_map:
                file.write(F'{coord[0]} {coord[1]}\n')
            file.close()
            print('Завершено создание карты')
            list_map.clear()
            self.way_list = []

    def read_train_way(self):
        try:
            way_file = open(self.way_file, 'r')
            for line in way_file:
                self.way_list.append(list(map(float, line.split())))
            print('good read')
        except: 
            print('ошибка чтения')

    def on_draw(self): #рисуем!))
        arcade.start_render()# эта команда начинает процесс рисовки
        
        #отрисовка пути поезда
        arcade.draw_line_strip(self.way_list, (255, 0, 0))

        #отрисовка всего что есть от нижних слоёв к верхним

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            window.get_size()[0], window.get_size()[1],
                                            self.background)
        self.bullet_list.draw()
        self.people_list.draw()
        self.blocks.draw()

        #for i in range(1, len(self.way_list)):
        #    arcade.draw_line(self.way_list[i-1][0], self.way_list[i-1][1], self.way_list[i][0], self.way_list[i][1], (255, 0, 255), 2)

        #отрисовка времени и кол-ва пуль в обойме. Позже запихну это в отдельный класс Интерфейса
        arcade.draw_text(F'{int(self.time-self.start_time)//60}:{int(self.time-self.start_time)%60}', SCREEN_WIDTH - 100, 20, arcade.color.WHITE, 16)
        arcade.draw_text(F':{self.player_sprite.bullet_now}', 40, 20, arcade.color.WHITE, 16)
        
        #отображение жизней
        hero = self.player_sprite
        draw_hp(hero.center_x, hero.center_y, hero._height, hero.max_hp, hero.hp)
        for guard in self.people_list:
            draw_hp(guard.center_x, guard.center_y, guard._height, guard.max_hp, guard.hp)
        for thing in self.all_sprites:
            thing.draw_hit_box()
        #отображение пути до гг
        for guard in self.guards_list:
            if guard.path:
                    arcade.draw_line_strip(guard.path, arcade.color.BLUE, 2)

        self.train.draw_all()

    def shot(self): #функция для стрельбы
        if self.mouse_pos['button'] == 1:
            hero = self.player_sprite
            if hero.bullet_now > 0:
                self.recharge = False   #отмена перезарядки при выстреле
                hero.bullet_now -= 1
                one_bullet = Bullet({'x': hero.center_x, 'y': hero.center_y}, self.mouse_pos)
                self.bullet_list.append(one_bullet)
                self.all_sprites.append(one_bullet)
                if hero.bullet_now == 0:            #авто-перезарядка, когда закончились патроны
                    self.start_recharge = self.time
                    self.recharge = True
    
    def recharge_move(self):     #перезарядка
        time_recharge = 1.0 #время зарядки одной пули
        if self.player_sprite.bullet_now < 6 and self.recharge:
            if self.time - self.start_recharge > time_recharge:
                self.player_sprite.bullet_now += 1
                self.start_recharge = self.time
        else:
            self.recharge = False

    def on_update(self, delta_time):
        self.train.update()
        self.people_list.update()

        for guard in self.guards_list:
            distant = int(sqrt((guard.center_x - self.player_sprite.center_x)**2 + (guard.center_y - self.player_sprite.center_y)**2))
            if (distant > 100 and distant < 150) and arcade.has_line_of_sight(guard.position, self.player_sprite.position, self.blocks, 200):
                guard.path = arcade.astar_calculate_path(guard.position,
                                                        self.player_sprite.position,
                                                        guard.barrier_list,
                                                        diagonal_movement=False)
            else:
                guard.path = []


        #self.player_sprite.update_angle(self.mouse_pos)#передаём координаты мыши персу
        self.shot()
        self.bullet_list.update()
        if self.paint_reils_way_flag:
           self.paint_reils_way(update=True)


        #коллизии между людьми
        for people1 in self.people_list:
            people_with_people = arcade.check_for_collision_with_list(people1, self.people_list)#проверяем взаимодейсвие 
            #спрайта перса и спрайты охранников, если они косаются, то мы получаем список тех охранников, кто коснулся
            for people2 in people_with_people: 
                rad = atan2(people1.center_y - people2.center_y, people1.center_y - people2.center_x)
                if abs(people1.width - people1.width)//2 <= abs(people1.center_x - people2.center_x): 
                    # people2.change_x = -cos(rad) * people2.speed
                    people2.flag_change_x = 0 #-sin(rad) * people2.speed
                    people2.center_x += -sin(rad)/abs(sin(rad)) * people1.speed
                    #people1.change_x = cos(rad) * people1.speed
                    people1.flag_change_x = 0#sin(rad) * people1.speed
                    people1.center_x += sin(rad)/abs(sin(rad)) * people2.speed
                if abs(people1.height - people1.height)//2 <= abs(people1.center_y - people2.center_y): 
                    # people2.change_x = -cos(rad) * people2.speed
                    people2.flag_change_y = 0 #-sin(rad) * people2.speed
                    people2.center_y += -sin(rad)/abs(sin(rad)) * people1.speed
                    #people1.change_x = cos(rad) * people1.speed
                    people1.flag_change_y = 0#sin(rad) * people1.speed
                    people1.center_y += sin(rad)/abs(sin(rad)) * people2.speed
                '''
                people1.change_x = 0
                people1.change_y = 0
                people2.change_x = 0
                people2.change_y = 0
                '''
        for bullet in self.bullet_list: # проверка взаимодейсвия пуль и охраны
            all_shot_list = arcade.check_for_collision_with_list(bullet, self.all_sprites)
            guards_shot_list = arcade.check_for_collision_with_list(bullet, self.people_list)
            for item in all_shot_list:
                self.bullet_list.remove(bullet)
                self.all_sprites.remove(bullet)
                break
            for guard in guards_shot_list:
                guard.hp -= bullet.atk
                if guard.hp < 1:
                    self.people_list.remove(guard)
                    self.all_sprites.remove(guard)
            if bullet.center_x > SCREEN_WIDTH + 10 or bullet.center_x < -10 or \
                bullet.center_y > SCREEN_HEIGHT + 10 or bullet.center_y < -10:
                self.bullet_list.remove(bullet)
                self.all_sprites.remove(bullet)
        self.recharge_move()
        self.time = time.time()
        self.mouse_pos['button'] = 0

    def on_key_press(self, key, modifiers): #передвижение перса wsad или стрелочками при нажатии
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.flag_change_y = 1
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.flag_change_y = -1

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.flag_change_x = -1
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.flag_change_x = 1

        if key == arcade.key.M:
            self.paint_reils_way_flag = True
            self.way_list = []

        if key == arcade.key.SPACE:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)

    def on_key_release(self, key, modifiers):#обработка, если клавишу отпустили
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.flag_change_y = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.flag_change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.flag_change_x = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.flag_change_x = 0
        if key == arcade.key.M:
            self.paint_reils_way_flag = False
            self.paint_reils_way(end=True)

    def on_mouse_motion(self, x, y, dx, dy):#если мышка двигается, то запоминаем её координаты 
        self.mouse_pos = {'x': x, 'y': y, 'dx': dx, 'dy': dy, 'button': 0}

    def on_mouse_press(self, x, y, button, modifiers):# считывает нажатие кнопок мыши. стрелям при нажатии
        self.mouse_pos['button'] = button

class GameOverView(arcade.View):#последнее окно

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Ты слаб! Нажми ESCAPE для рестарта",  window.get_size()[0]/2, window.get_size()[1]/2,
                         arcade.color.WHITE, 30, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)

def change_hit_box(this_sprite): 
    #print(this_sprite)
    width, height = Image.open(this_sprite.image).size#this_sprite.width, this_sprite.height
    #this_sprite.width, this_sprite.height = width, height
    this_sprite.set_hit_box([(width//2, -height//2), (-width//2, -height//2), (-width//2, -2.5*height//10), (width//2, -2.5*height//10)])
    #print(this_sprite.center_x, this_sprite.center_y)
    #self.center_hit_box = (this_sprite.center_x, this_sprite.center_y-2*height//5)

def main():# собственно запуск
    global window 
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    window.center_window()
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":# проверка, что запускаем именно из main
    main()