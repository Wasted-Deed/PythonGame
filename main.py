import arcade
import os
import time
import arcade.gui
from random import randint 
from PIL import Image
from math import atan2, sin, cos, sqrt, pi
from Guard import Guard
from Player import  Player
from variables import *
from Bullet import Bullet
from hp import draw_hp
from Train import Train
from arcade.gui import UIManager
from MenuButton import *

file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)

#добавить охранникам стрельбу
#переработать стрельбу - зависает на первом выстреле
#увеличить хит-боксы, ибо выстрелы взаимодействуют с ними

class MenuView(arcade.View):#меню
    def __init__(self):
        super().__init__()

        self.ui_manager = UIManager()

    def on_show_view(self):
        self.setup()
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Добро пожаловать", 
                        self.window.width / 2, 
                        self.window.height / 1.5,
                        arcade.color.WHITE, 
                        font_size=30, 
                        anchor_x="center")

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def setup(self):
        self.ui_manager.purge_ui_elements()
        self.ui_manager.add_ui_element(PlayButton())
        self.ui_manager.add_ui_element(SettingButton())
        self.ui_manager.add_ui_element(ExitButton())
    
    def on_update(self, delta_time):
        for i in range(3):
            button = self.ui_manager.find_by_id(i)
            button.center_x = self.window.width / 2
            button.center_y = (self.window.height / 2) - (35 * i)
            if button.click and i == 0:
                button.click = False
                game_view = GameView()
                game_view.setup() #загрузка ресурсов
                window.show_view(game_view)
            elif button.click and i == 1:
                button.click = False
            elif button.click and i == 2:
                button.click = False
                window.close()
            


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
        self.recharge = False
        self.textures = []
        self.permission = window.get_size()


    def setup(self):  # предустановки игры
        

        # препятствия
        self.blocks = arcade.SpriteList(use_spatial_hash=True)
        for block in sp_coordinates_obstacles:
            number = randint(1, 2)
            self.blocks.append(arcade.Sprite("images/obstacles/2-%d.png" % number, 1.5, 
                                            center_x=self.permission[0]*block[0], 
                                            center_y=self.permission[1]*block[1],
                                            hit_box_algorithm="Detailed"))
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

        #время
        self.time = 0
        self.start_time = time.time()
        self.time_for_collision = time.time()
        #для работы перезарядки
        self.start_recharge = self.time

        #эта переменная для постоянной смены хитбоксов
        # 0 - нижняя четверть спрайта
        # 1 - весь спрайт
        self.index = 0

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

    def read_train_way(self):   #  читает из файла путь поезда
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
        if window.get_size() != self.permission:
            self.permission = window.get_size()
            for i in range(len(self.blocks)):
                self.blocks[i].center_x = self.permission[0]*sp_coordinates_obstacles[i][0]
                self.blocks[i].center_y = self.permission[1]*sp_coordinates_obstacles[i][1]
            self.blocks.draw()
        else:
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

    def shot(self, shooter_sprite): #функция для стрельбы
        if shooter_sprite == self.player_sprite:
            hero = shooter_sprite
            if hero.bullet_now > 0:
                self.recharge = False   #отмена перезарядки при выстреле
                hero.bullet_now -= 1
                one_bullet = Bullet(shooter_sprite, {'x': hero.center_x, 'y': hero.center_y}, self.mouse_pos)
                self.bullet_list.append(one_bullet)
                self.all_sprites.append(one_bullet)
            elif hero.bullet_now == 0:            #перезарядка при выстреле с пустым магазином
                self.start_recharge = self.time
                self.recharge = True
        else:
            pass
    
    def recharge_move(self):     #перезарядка
        time_recharge = 1.0 #время зарядки одной пули
        if self.time - self.start_recharge > time_recharge+0.03: 
            self.start_recharge = self.time
        if self.player_sprite.bullet_now < 6 and self.recharge:
            if self.time - self.start_recharge >= time_recharge:
                self.player_sprite.bullet_now += 1
                self.start_recharge = self.time
        else:
            self.recharge = False

    def collision(self):  # коллизии
        #коллизии между людьми (взаимное отталкивание) для index = 0
        if self.index == 0:
            for people1 in self.all_sprites:    # Временно стоят все спрайты. Далее заменить на people_list
                people_with_people = arcade.check_for_collision_with_list(people1, self.people_list)
                for people2 in people_with_people: 
                    rad = atan2(people1.center_y - people2.center_y, people1.center_x - people2.center_x)
                    
                    people1.hitbox_y = people1.center_y - 3* people1.height//8
                    people2.hitbox_y = people2.center_y - 3* people2.height//8

                    # отталкивание по горизонтали и вертикали раздельно. По горизонтали, при нецентральном ударе
                    # может происходить смещение по горизонтальи до пракращения взаимодействия
                    if abs(people1.hitbox_y - people2.hitbox_y) >= abs(people1.height - people2.height)//2: 
                        people2.center_y += -sin(rad)/abs(sin(rad)) * people1.speed
                        people1.center_y += sin(rad)/abs(sin(rad)) * people2.speed
                    elif abs(people1.center_x - people2.center_x) >= abs(people1.width - people1.width)//2:    
                        people2.center_x += -cos(rad)/abs(cos(rad)) * people1.speed
                        people1.center_x += cos(rad)/abs(cos(rad)) * people2.speed
        
        if self.index == 1: # проверка взаимодейсвия пуль и охраны для полных спрайтов index = 1 
            # исчезает при столкновении. Если столкновение с живым спрайтом, то отномает жизни
            for bullet in self.bullet_list: 
                all_shot_list = arcade.check_for_collision_with_list(bullet, self.all_sprites)
                guards_shot_list = arcade.check_for_collision_with_list(bullet, self.people_list)
                for item in all_shot_list:
                    if item != bullet.shooter_sprite:
                        self.bullet_list.remove(bullet)
                        self.all_sprites.remove(bullet)
                        if item in guards_shot_list:
                            guard = item
                            guard.hp -= bullet.atk
                            if guard.hp < 1:
                                self.people_list.remove(guard)
                                self.all_sprites.remove(guard)
                        break
                    
                if bullet.center_x > SCREEN_WIDTH + 10 or bullet.center_x < -10 or \
                    bullet.center_y > SCREEN_HEIGHT + 10 or bullet.center_y < -10:
                    self.bullet_list.remove(bullet)
                    self.all_sprites.remove(bullet)

    def on_update(self, delta_time):    # рабочий цикл 
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

        #self.player_sprite.update_angle(self.mouse_pos) #передаём координаты мыши персу если требуется
        
        # выстрел по нажитию левой кнопки мыши
        if self.mouse_pos['button'] == 1:
            self.shot(self.player_sprite)
        self.bullet_list.update()
        if self.paint_reils_way_flag:
           self.paint_reils_way(update=True)

        # собственно коллизии
        self.collision()
        
        # перезарядка
        self.recharge_move()
        self.time = time.time()
        self.mouse_pos['button'] = 0

        
        # смена хитбокса раз в n*0.016 секунд, где n - колличество циклов системы
        if time.time() - self.time_for_collision >= 0.048:
            self.index = (self.index+1)%2
            for thing in self.people_list:
                change_hit_box(thing, self.index)
            self.time_for_collision = time.time()
        

    def on_key_press(self, key, modifiers): #передвижение перса wsad или стрелочками при нажатии
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.y_sp.append(1)
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.y_sp.append(-1)

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.x_sp.append(-1)
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.x_sp.append(1)

        if key == arcade.key.M:
            self.paint_reils_way_flag = True
            self.way_list = []

        if key == arcade.key.SPACE:
            game_over_view = MenuView()
            self.window.show_view(game_over_view)

    def on_key_release(self, key, modifiers):#обработка, если клавишу отпустили
        player = self.player_sprite
        if key == arcade.key.UP or key == arcade.key.W :
            del player.y_sp[player.y_sp.index(1)]
        if key == arcade.key.DOWN or key == arcade.key.S:
            del player.y_sp[player.y_sp.index(-1)]
        if key == arcade.key.LEFT or key == arcade.key.A :
            del player.x_sp[player.x_sp.index(-1)]
        if key == arcade.key.RIGHT or key == arcade.key.D:
            del player.x_sp[player.x_sp.index(1)]
        if key == arcade.key.M:
            self.paint_reils_way_flag = False
            self.paint_reils_way(end=True)
        if key == arcade.key.R:
            self.start_recharge = self.time
            self.recharge = True

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

def change_hit_box(this_sprite, index=0): 
    #print(this_sprite)
    width, height = Image.open(this_sprite.image).size#this_sprite.width, this_sprite.height
    #this_sprite.width, this_sprite.height = width, height
    if index == 0:
        this_sprite.set_hit_box([(width//2, -height//2), (-width//2, -height//2), (-width//2, -2.5*height//10), (width//2, -2.5*height//10)])
    elif index == 1:
        this_sprite.set_hit_box([(width//2, -height//2), (-width//2, -height//2), (-width//2, height//2), (width//2, height//2)])
    #print(this_sprite.center_x, this_sprite.center_y)
    #self.center_hit_box = (this_sprite.center_x, this_sprite.center_y-2*height//5)


def main():# собственно запуск
    global window 
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True, fullscreen=False)

    window.center_window()
    window.set_min_size(SCREEN_WIDTH, SCREEN_HEIGHT) # вырубить, если нужно перейти в полный экран и поменять местами True and False в конструкторе
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":# проверка, что запускаем именно из main
    main()
