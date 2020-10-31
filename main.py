import arcade
import os
from time import clock as time
from math import atan2, sin, cos, sqrt, pi
from Guard import Guard
from Player import  Player
from variables import *
from Bullet import Bullet
from hp import draw_hp


class MyGame(arcade.Window):#самый главный класс

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        #без библиотеки os спрайты почему-то не хотят браться из нашей директории, они как-то привязаны к своему сайту
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        #переменные спрайта для перса
        self.player_sprite = None
        #переменные спрайта для охраны
        self.people_list = None
        self.guards_sprite = None
        #arcade.set_background_color(arcade.color.AMAZON) #цвет фона
        self.land = None
        self.time = 0     
        self.recharge = False

    def setup(self): # функция нужна для создания всех и всего
        self.land = arcade.SpriteList() #создаём поле
        for i in sp_coordinates_field:
            #self.land.append(arcade.Sprite("images/земля.png", 0.5, center_x = i[0], center_y = i[1]))
            pass


        self.people_list = arcade.SpriteList() # присваиваем Sprite_List, чтобы обрабатывать как спрайт
        self.player_sprite = Player() #создаём перса и кидаем ему координаты
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 50
        self.people_list.append(self.player_sprite)#кидаем перса в наш список спратов для перса

        self.guards_list = arcade.SpriteList() # создвём охрану
        for i in range(len(sp_coordinates_guards)):
            x, y = sp_coordinates_guards[i]
            self.guards_sprite = Guard(x, y, self.player_sprite.center_x, self.player_sprite.center_y)
            self.guards_list.append(self.guards_sprite)
            self.people_list.append(self.guards_sprite)

        self.bullet_list = arcade.SpriteList()#также создаём пули
        hero = self.player_sprite
        self.mouse_pos = {'x': hero.center_x, 'y': hero.center_y, 'dx': 0, 'dy': 0, 'button': 0} #задаём координаты мышки


        self.all_sprites = arcade.SpriteList() #делаем общий для всех список, чтобы было легче обрабатывать
        self.all_sprites.extend(self.people_list)
        self.all_sprites.extend(self.bullet_list)

    def on_draw(self): #рисуем!))
        arcade.start_render()# эта команда начинает процесс рисовки

        #отрисовка всего что есть от нижних слоёв к верхним
        self.player_sprite.player_field()
        for guard in self.guards_list: #временная функция, для отображения точек вокруг охраны, надо чтобы наглядно видеть действие 
            guard.guard_field()

        self.land.draw()
        self.bullet_list.draw()
        self.people_list.draw()

        #отрисовка времени и кол-ва пуль в обойме. Позже запихну это в отдельный класс Интерфейса
        arcade.draw_text(F'{int(self.time)//60}:{int(self.time)%60}', SCREEN_WIDTH - 100, 20, arcade.color.WHITE, 16)
        arcade.draw_text(F':{self.player_sprite.bullet_now}', 40, 20, arcade.color.WHITE, 16)
        #отображение жизней
        hero = self.player_sprite
        draw_hp(hero.center_x, hero.center_y, hero._height, hero.max_hp, hero.hp)
        for guard in self.people_list:
            draw_hp(guard.center_x, guard.center_y, guard._height, guard.max_hp, guard.hp)

    def shot(self): #функция для стрельбы
        if self.mouse_pos['button'] == 1:
            hero = self.player_sprite
            if hero.bullet_now > 0:
                self.recharge = False   #отмена перехарядки при выстреле
                hero.bullet_now -= 1
                one_bullet = Bullet({'x': hero.center_x, 'y': hero.center_y}, self.mouse_pos)
                self.bullet_list.append(one_bullet)
                self.all_sprites.append(one_bullet)
                if hero.bullet_now == 0:            #авто-перезарядка, когда закончились патроны
                    self.start_recharge = self.time
                    self.recharge = True
    
    def recharge_move(self):     #перезарядка
        if self.player_sprite.bullet_now < 6 and self.recharge:
            if self.time - self.start_recharge > 1.0:
                self.player_sprite.bullet_now += 1
                self.start_recharge = self.time
        else:
            self.recharge = False

    def on_update(self, delta_time):# одна из самых важных функций, запускается 60 раз в секунду
        self.people_list.update()#обновляем все спрайты

        for guard in self.people_list:#передаю координаты перса охранникам
            if isinstance(guard, Player):
                continue
            guard.player_x = self.player_sprite.center_x
            guard.player_y = self.player_sprite.center_y
            if guard.r <= 25:
                self.player_sprite.hp -= guard.atk

        self.player_sprite.update_angle(self.mouse_pos)#передаём координаты мыши персу
        self.shot()
        self.bullet_list.update()

        print(self.player_sprite.speed)
        #коллизии между людьми
        for people1 in self.people_list:
            people_with_people = arcade.check_for_collision_with_list(people1, self.people_list)#проверяем взаимодейсвие 
            #спрайта перса и спрайты охранников, если они косаются, то мы получаем список тех охранников, кто коснулся
            for people2 in people_with_people: 
                rad = atan2(people1.center_y - people2.center_y, people1.center_y - people2.center_x)
                people2.center_x -= cos(rad) * people2.speed
                people2.center_y -= sin(rad) * people2.speed
                people1.center_x += cos(rad) * people1.speed
                people1.center_y += sin(rad) * people1.speed

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
        self.time = time()
        self.mouse_pos['button'] = 0

    def on_key_press(self, key, modifiers): #передвижение перса wsad или стрелочками при нажатии
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
        if abs(self.player_sprite.change_x) > 0 and abs(self.player_sprite.change_y) > 0:
            self.player_sprite.change_x *= sqrt(2)/2
            self.player_sprite.change_y *= sqrt(2)/2

    def on_key_release(self, key, modifiers):#обработка, если клавишу отпустили
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0
        if abs(self.player_sprite.change_x) > 0 and abs(self.player_sprite.change_y) > 0:
            self.player_sprite.change_x *= sqrt(2)/2
            self.player_sprite.change_y *= sqrt(2)/2

    def on_mouse_motion(self, x, y, dx, dy):#если мышка двигается, то запоминаем её координаты 
        self.mouse_pos = {'x': x, 'y': y, 'dx': dx, 'dy': dy, 'button': 0}

    def on_mouse_press(self, x, y, button, modifiers):# считывает нажатие кнопок мыши. стрелям при нажатии
        self.mouse_pos['button'] = button


def main():# собственно запуск
    global window 
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":# проверка, что запускаем именно из main
    main()