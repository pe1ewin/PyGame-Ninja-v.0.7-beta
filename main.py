# Подгружаем библиотеки
import pygame
import sys
from button import Button   # наша собственная библиотека для рисования кнопок
import linecache
import re

pygame.init()   # Инициализируем pygame
pygame.mixer.init()     # Инициализируем блок для звуков и музыки
clock = pygame.time.Clock()     # Инициализируем внутриигровое время
fps = 30  # Frames per Second(частота кадров) задаёт скорость игры

# Настройки экрана и окна
screen_width = 1280     # Ширина окна
screen_height = 720     # Высота окна
screen = pygame.display.set_mode((screen_width, screen_height))     # Устанавливаем выше указанные параметры окна
pygame.display.set_caption('Путь ниндзя: Тайна древнего храма')     # Меняем название окна
icon = pygame.image.load('img/icon/0.png')      # Подгружаем изображение иконки
pygame.display.set_icon(icon)   # Меняем иконку окна

# Загрузка шрифтов
menu_font = pygame.font.Font('FONTS/menu/rbnaftalin.otf', 24)   # Подключаем шрифт для меню паузы
dialog_font = pygame.font.Font('FONTS/dialogs/Bartina Regular.ttf', 38)    # Подключаем шрифт для диалогов
interface_font = pygame.font.Font('FONTS/menu/aoudax-cyrillic.otf', 32)  # Подключаем шрифт для интерфейса

# Загрузка звуков и музыки
menu_music = pygame.mixer.Sound('sounds/music/')    # Загружаем трек для меню
menu_music.set_volume(0.1)  # Устанавливаем громкость трека для меню
hero_pain_sound = pygame.mixer.Sound('sounds/hit/hero_pain.mp3')  # Загружаем звук получения урона героем
hero_pain_sound.set_volume(1)  # Устанавливаем громкость звука
enemy_pain_sound = pygame.mixer.Sound('sounds/hit/enemy_pain.mp3')  # Загружаем звук получения урона врагом
enemy_pain_sound.set_volume(1)  # Устанавливаем громкость звука

#  Переменные необходимые для работы игры и её логики
attack_cooldown = 0  # Задержка между атаками
player_x = 20  # координата Х спавна персонажа
player_y = 465  # координата Y спавна персонажа
player_walking_speed = 5  # скорость перемещения героя
cooldown = 0    # Задержка между атаками героя
hero_health = 100   # Здоровье героя
enemy_health = 100  # Здоровье противника
enemy_x = 700   # координата x спавна врага
enemy_animate_cooldown = 0
player_width = 160  # Переменная с шириной героя, нужна для загрузки кадра анимации
player_height = 140  # Переменная с высотой героя, нужна для загрузки кадра анимации
side = 0    # Сторона в которую повёрнут персонаж
gravity = 1     # гравитация
jump_count = 20     # Сила прыжка
y_velocity = jump_count  # Задаёт расстояние изначального прыжка
active_lvl = 1  # Номер активного уровня

# Флаги(логические переменные)
attack_flag = False  # Флаг атаки героя
enemy_attack = False    # Флаг атаки врага
fl_left = fl_right = fl_attack = False  # флаги действий, когда действие выполняется, принимают значение True
fl_nothing = True   # флаг не нажатых клавиш

# Логические переменные для циклов
run_game = False  # Переменная для работы основного цикла игры
run_settings = False    # Переменная для работы цикла while в def settings
pause = False   # Переменная для работы цикла while в def pause
run_menu = True  # Переменная для работы цикла while в def menu
run = True  # Переменная для цикла

#  Массивы для загрузки текстур(спрайтов)
enemy_animation = []    # Сюда помещается спрайт с героем
end = []    # Тут хранятся картинки выигрыша и проигрыша
maps = []   # Тут хранятся карты

#  Счётчики для анимаций и диалогов
enemy_walk_anim = 0  # Счётчик для анимаций ходьбы врага
enemy_attack_anim = 0   # Счётчик для анимаций атаки врага
frame_index = 6    # Переменная для обращения к спрайту героя(6-стоит, 5-прыжок вправо, 4-прыжок влево, 3-иди вправо, 2-влево, 1-атака вправо, 0- атака влево)
frame_count = 0  # Переменная-счётчик для переключения кадров анимации героя
line_number = 1     # Переменная-счётчик для чтения диалогов на уровне 1
frame_count_idle = 0    # Счётчик для анимации покоя героя
frame_count_attack = 0  # Счётчик для анимации атаки героя
frame_count_jump = 0    # Счётчик для анимации прыжка героя

#  Загрузка карт и npc
npc = pygame.image.load('img/npc/0.png')     # Загружаем NPC(Лису)
npc = pygame.transform.scale(npc, (111, 110))   # Подгоняем размер
takeshi_animation = pygame.image.load('img/hero/hero_sprite.png')   # Загружаем спрайт с героем
menu_bg = pygame.image.load('img/menu/bg.png')  # Загружаем фон меню

#  Переменные содержащие коды цветов
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
dark_blue = (34, 44, 105)
green = (0, 205, 0)
gray = (178, 178, 178)

# Создание кнопок
# класс кнопок принимает на вход последовательные значения:
# расположение x и y ; ширину и высоту кнопки; текст на кнопке, если нужен;
# ссылка на картинку кнопки или переменная содержащая её;
# ссылка на изображения выделенной кнопки; звук, цвет(если не надо - чёрный)
# КНОПКИ МЕНЮ
play_button = Button(880, 515, 360, 180, "", "img/menu/buttons_bg/no_hover.png", "img/menu/buttons_bg/hovered.png",
                     None, black)
exit_button = Button(30, 525, 310, 180, "", "img/menu/buttons_bg/exit_no_hover.png",
                     "img/menu/buttons_bg/exit_hover.png", None, black)

# КНОПКИ НАСТРОЕК
back_button = Button(557, 435, 166, 166, "", "img/pause/buttons/back_no_hover.png",
                     "img/pause/buttons/back_hover.png", None, black)

# КНОПКИ ПАУЗЫ
resume_button = Button(715, 435, 166, 166, "", "img/pause/buttons/resume_no_hover.png",
                       "img/pause/buttons/resume_hover.png", None, black)
menu_button = Button(557, 435, 166, 166, "", "img/pause/buttons/menu_no_hover.png", "img/pause/buttons/menu_hover.png",
                     None, black)
conf_button = Button(400, 435, 166, 166, "", "img/pause/buttons/settings_no_hover.png",
                     "img/pause/buttons/settings_hover.png", None, black)

#  КНОПКА ДИАЛОГА
further_button = Button(880, 515, 360, 180, "", "img/dialogs/further_no_hover.png", "img/dialogs/further_hover.png",
                        None, black)
menu_music.play()   # Включаем музыку меню

def menu():  # Функция с окном меню
    global run_game, run_menu  # даём функции понять что используем переменные вне функции
    while run_menu:     # Запускаем цикл, условие пока run_menu = True
        screen.blit(menu_bg, (0, 0))  # Рисуем фон
        for event in pygame.event.get():    # Проверка событий окна
            if event.type == pygame.QUIT:   # Если нажали выход, то закрываем приложение
                run_menu = False    # Останавливаем цикл
                pygame.quit()    # выходим из pygame
                sys.exit()    # Закрываем
            if event.type == pygame.USEREVENT and event.button == play_button:  # Если была нажата кнопка начать
                run_game = True  # Запускаем цикл игры
                upload_textures()   # Вызываем функцию для загрузки текстур
                menu_music.stop()   # Выключаем музыку
                lvl1()  # Вызываем функцию с 1 уровнем
            elif event.type == pygame.USEREVENT and event.button == exit_button:  # Если была нажата кнопка выход
                run_menu = False    # Останавливаем цикл
                pygame.quit()    # выходим из pygame
                sys.exit()    # Закрываем
            #  проверка события
            play_button.handle_event(event)    # см строчку 137
            exit_button.handle_event(event)    # см строчку 142
            #  Проверяем положение мыши относительно кнопки
        play_button.check_hover(pygame.mouse.get_pos())
        exit_button.check_hover(pygame.mouse.get_pos())
        #  рисуем кнопки
        play_button.draw(screen)
        exit_button.draw(screen)
        # обновление экрана
        pygame.display.flip()


def settings():  # Функция с окном настроек
    global run_settings, pause  # даём функции понять что используем переменные вне функции
    settings_bg = pygame.image.load('img/pause/settings.png')   # Загружаем фон
    while run_settings:     # Запускаем цикл, условие пока run_settings = True
        screen.blit(settings_bg, (0, 0))    # Рисуем фон
        for event in pygame.event.get():    # Проверка событий окна
            if event.type == pygame.QUIT:   # Если нажали выход, то закрываем приложение
                run_settings = False    # Останавливаем цикл
                pygame.quit()    # выходим из pygame
                sys.exit()    # Закрываем
            if event.type == pygame.USEREVENT and event.button == back_button:  # Если была нажата кнопка назад
                pause_menu()    # вызываем функцию паузы
                pause = True    # снова запускаем цикл
                run_settings = False  # останавливаем цикл настроек
            #  проверка события
            back_button.handle_event(event)
            #  Проверяем положение мыши относительно кнопки
            back_button.check_hover(pygame.mouse.get_pos())
            #  рисуем кнопку
            back_button.draw(screen)
            # обновление экрана
            pygame.display.flip()


def pause_menu():   # Функция паузы
    global run_game, run_settings, pause, active_lvl    # даём функции понять что используем переменные вне функции
    pause_bg = pygame.image.load('img/pause/pause_window.png')  # Загружаем фон
    temp_text = ''  # Переменная хранящая текст(см 190 и 192 строчки)
    while pause:    # Запускаем цикл, условие пока run_settings = True
        screen.blit(pause_bg, (0, 0))   # Рисуем фон
        if active_lvl == 1:  # Условие, если активный уровень - 1
            temp_text = menu_font.render('Выслушайте рассказ', True, gray)  # передаём в переменную подпись для 1 уровня
        elif active_lvl == 2:   # Условие, если активный уровень - 2
            temp_text = menu_font.render('Победите противника', True, gray)  # передаём в переменную подпись для 2 ур
        for event in pygame.event.get():    # Проверка событий окна
            if event.type == pygame.QUIT:   # Если нажали выход, то закрываем приложение
                pause = False   # Останавливаем цикл
                pygame.quit()   # выходим из pygame
                sys.exit()  # Закрываем
            if event.type == pygame.USEREVENT and event.button == resume_button:    # Если была нажата кнопка продолжить
                pause = False   # Останавливаем цикл
            elif event.type == pygame.USEREVENT and event.button == menu_button:    # Если была нажата кнопка меню
                pause = False   # Останавливаем цикл
                menu()  # Вызываем меню
            elif event.type == pygame.USEREVENT and event.button == conf_button:    # Если была нажата кнопка настроек
                pause = False   # Останавливаем цикл
                run_settings = True  # Запускаем цикл настроек
                settings()  # Вызываем настройки
            #  проверка события
            resume_button.handle_event(event)
            menu_button.handle_event(event)
            conf_button.handle_event(event)

        #  Проверяем положение мыши относительно кнопки
        resume_button.check_hover(pygame.mouse.get_pos())
        menu_button.check_hover(pygame.mouse.get_pos())
        conf_button.check_hover(pygame.mouse.get_pos())
        #  рисуем кнопки
        resume_button.draw(screen)
        menu_button.draw(screen)
        conf_button.draw(screen)
        screen.blit(temp_text, (500, 330))  # Рисуем текст
        pygame.display.flip()   # Обновляем экран


def upload_textures():  # функция загрузки текстур и картинок
    global maps   # берём переменные из вне функции
    map1 = pygame.image.load('img/maps/2.jpg')  # Загружаем карту
    map1 = pygame.transform.scale(map1, (screen_width, screen_height))  # Подгоняем размер
    map2 = pygame.image.load('img/maps/0.jpg')  # Загружаем карту
    map2 = pygame.transform.scale(map2, (screen_width, screen_height))  # Подгоняем размер
    map3 = pygame.image.load('img/maps/3.jpg')  # Загружаем карту
    map3 = pygame.transform.scale(map3, (screen_width, screen_height))  # Подгоняем размер
    maps = [map1, map2, map3]   # помещаем картинки карт в массив
def get_image(sheet, width, height, frame_ind, frame_c, color):  # Функция отвечает за выбор картинки со спрайта героя
    # на вход функция получает:
    # спрайт, ширину, высоту, индекс анимации(зависит от действия героя), порядковый номер кадра, цвет хромакея
    image = pygame.Surface((width, height)).convert_alpha()  # Создаём область с размерами героя
    image.blit(sheet, (0, 0), (width*frame_c, height*frame_ind, width, height))  # рисуем эту область
    image.set_colorkey(color)   # убираем обводку или фон хромакеем
    return image    # возвращаем готовую картинку персонажа

def draw_bg(lvl_count):  # Функция рисования карт
    # На вход функция получает: номер уровня
    if lvl_count == 1:  # Если уровень 1
        screen.blit(maps[0], (0, 0))    # Рисуем уровень 1
    elif lvl_count == 2:    # Если уровень 2
        screen.blit(maps[1], (0, 0))    # Рисуем уровень 2
    elif lvl_count == 3:    # Если уровень 3
        screen.blit(maps[2], (0, 0))    # Рисуем уровень 3

class Enemy:    # Класс противника
    def __init__(self, p_x):    # Функция инициализации
        self.anim_count = 0  # Переменная счётчик для анимаций
        self.y = 448    # Позиция врага по y
        self.side = 0   # В какую сторону повёрнут 0 - влево, 1 - вправо
        self.action = 0  # Переменная с кодом действия врага
        self.player_x = p_x  # Переменная для отслеживания перемещений героя
        temp_img = ['0.png', '1.png', '2.png', '3.png', '4.png', '5.png', '6.png']  # Переменная с именами картинок
        # Загружаем картинки анимаций врага
        # Логика такая, в конце строки цикл и последовательно в массив помещается файл с указанным названием
        self.walk_left = [pygame.image.load('img/enemy/walk_left/'+path) for path in temp_img]
        self.walk_right = [pygame.image.load('img/enemy/walk_right/' + path) for path in temp_img]
        self.attack_left = [pygame.image.load('img/enemy/attack_left/'+path) for path in temp_img]
        self.attack_right = [pygame.image.load('img/enemy/attack_right/' + path) for path in temp_img]
        # загрузка картинки покоя врага
        self.idle = pygame.image.load('img/enemy/idle/idle_enemy.png')

    def update_position(self, attack_fl):   # Функция обновления позиции врага и логика действий
        global enemy_x, enemy_animate_cooldown  # переменные из вне класса
        if enemy_x > self.player_x:     # Если координата x врага больше героя
            self.action = 1     # Действие 1 (идём влево)
            enemy_x -= 1    # уменьшаем x врага, двигаем
            self.side = 0   # враг смотрит влево
        elif enemy_x < self.player_x:  # Если координата x врага больше героя
            self.action = 2     # Действие 2 (идём вправо)
            enemy_x += 1    # увеличиваем x врага, двигаем
            self.side = 1   # враг смотрит вправо
        elif enemy_x == player_x:   # Если координата x врага = героя
            self.action = 0  # Действие 0 (стоим)
        if attack_fl:   # если получили значение флага True
            if self.side == 0:  # Если враг смотрит влево
                self.action = 3  # Действие 3 (атакуем влево)
            elif self.side == 1:    # Если враг смотрит вправо
                self.action = 4  # Действие 4 (атакуем вправо)

    def drawing(self):  # Функция отрисовки анимаций
        global enemy_walk_anim, enemy_attack_anim   # переменные из вне класса
        if self.action == 1:    # Если действие 1 (идём влево)
            temp_image = self.walk_left[enemy_walk_anim // 4]   # передаём в переменную нужную в данный момент картинку
        elif self.action == 2:  # Если действие 2 (идём вправо)
            temp_image = self.walk_right[enemy_walk_anim // 4]  # передаём в переменную нужную в данный момент картинку
        elif self.action == 3:  # Если действие 3 (атакуем влево)
            temp_image = self.attack_left[enemy_attack_anim]    # передаём в переменную нужную в данный момент картинку
        elif self.action == 4:  # Если действие 4 (атакуем вправо)
            temp_image = self.attack_right[enemy_attack_anim]   # передаём в переменную нужную в данный момент картинку
        else:   # Если действие 0 (стоим)
            temp_image = self.idle  # передаём в переменную нужную в данный момент картинку
        screen.blit(temp_image, (enemy_x, self.y))  # рисуем нужную в данный момент картинку

def interface_lvl1():   # Функция отрисовки интерфейса 1 уровня
    global run_game     # переменная из вне
    dialog_fox_bg = pygame.image.load('img/dialogs/fox/fox_talk.png')   # диалоговое окно Кицунэ
    dialog_fox_bg = pygame.transform.scale(dialog_fox_bg, (670, 200))   # преобразуем размеры
    dialog_hero_bg = pygame.image.load('img/dialogs/hero/ninja_talk.png')   # диалоговое окно Такеши
    dialog_hero_bg = pygame.transform.scale(dialog_hero_bg, (670, 200))  # преобразуем размеры
    if line_number == 4 or line_number == 8 or line_number == 12:   # Если читаем 4,8, 12 строчку
        screen.blit(dialog_hero_bg, (305, 50))  # показываем диалоговое окно Такеши
    else:  # Если нет
        screen.blit(dialog_fox_bg, (305, 50))   # показываем диалоговое окно Кицунэ
    if line_number != 16:  # Если не дошли до 16й строчки
        temp_text = linecache.getline("dialogs/lvl1.txt", line_number).strip()  # Временно помещаем прочтённую строчку
        if len(temp_text) > 30:  # Если число символов в строке больше 30
            y_text = 95  # Координата начальной точки Y вывода текста
            part = re.split('[|]', temp_text)   # помещаем часть текста в массив, если встретили разделитель |
            # Если встретили | переходим на следующий индекс массива
            for i in range(len(part)):  # Цикл для вывода массива текста
                show_text_1 = dialog_font.render(part[i], True, black)  # каким будем шрифтом и что выводить и цвет
                screen.blit(show_text_1, (500, y_text))  # рисуем текст
                y_text += 30    # как нарисовали текст отступ
        else:   # Если длина строки не превысила 30 символов
            show_text_1 = dialog_font.render(temp_text, True, black)  # каким будем шрифтом и что выводить и цвет
            screen.blit(show_text_1, (500, 95))  # рисуем текст
    elif line_number >= 16:  # если дошли до конца диалогов, завершаем уровень 1
        run_game = True  # запускаем цикл 2го уровня
        upload_textures()   # загружаем текстуры
        lvl3()  # вызываем следующий уровень


def lvl1():  # функция 1го уровня
    global run_game, line_number, pause, active_lvl  # переменные из вне
    active_lvl = 1  # активный уровень 1
    line_number = 1  # активная строчка 1
    while run_game:  # запускаем цикл
        clock.tick(fps)  # устанавливаем скорость переключения кадров 30
        draw_bg(2)  # рисуем карту
        screen.blit(npc, (615, 320))    # рисуем npc
        frame0 = get_image(takeshi_animation, player_width, player_height, frame_index, frame_count, black)  # герой AFK
        screen.blit(frame0, (player_x, player_y))   # рисуем героя
        interface_lvl1()  # вызываем интерфейс 1 уровня
        key_pressed = pygame.key.get_pressed()  # переменная получает данные о нажатых клавишах
        if key_pressed[pygame.K_ESCAPE]:    # если нажали ESC
            pause = True    # запускаем цикл паузы
            pause_menu()    # вызываем меню паузы
        for event in pygame.event.get():    # обрабатываем события
            if event.type == pygame.USEREVENT and event.button == further_button:  # если нажали далее
                line_number += 1    # переходим на следующую строчку диалога
            elif event.type == pygame.QUIT:  # если нажали крестик
                run_game = False    # останавливаем цикл
                pygame.quit()   # выходим из pygame
                sys.exit()   # закрываем
            #  проверка события
            further_button.handle_event(event)
        #  Проверяем положение мыши относительно кнопки
        further_button.check_hover(pygame.mouse.get_pos())
        #  рисуем кнопку
        further_button.draw(screen)
        #  обновляем экран
        pygame.display.flip()

temp_time = pygame.time.get_ticks()  # переменная для хранения времени на момент обращения

def end_of_game(flag):  # функция вывода экрана в конце игры
    ending = True
    clock.tick(fps)
    global run, run_menu, enemy_health, hero_health, player_x
    return_button = Button(880, 515, 360, 180, "", "img/lose/try_again_no_hover.png", "img/lose/try_hover.png",
                        None, black)
    main_button = Button(80, 515, 300, 180, "", "img/lose/menu_no_hover.png", "img/lose/menu_hover.png",
                           None, black)
    while ending:
        for event in pygame.event.get():    # Проверка событий окна
            if event.type == pygame.QUIT:   # Если нажали выход, то закрываем приложение
                ending = False   # Останавливаем цикл
                pygame.quit()   # выходим из pygame
                sys.exit()  # Закрываем
            if event.type == pygame.USEREVENT and event.button == return_button:    # Если была нажата кнопка продолжить
                run = True
                enemy_health = 100
                hero_health = 100
                player_x = 20
                lvl3()
            elif event.type == pygame.USEREVENT and event.button == main_button:    # Если была нажата кнопка меню
                run_menu = True   # Останавливаем цикл
                menu()  # Вызываем меню
            #  проверка события
            return_button.handle_event(event)
            main_button.handle_event(event)

        if flag == 'win':
            image = pygame.image.load('img/win/win.png')
            image = pygame.transform.scale(image, (screen_width, screen_height))
            screen.blit(image, (0, 0))
            #  Проверяем положение мыши относительно кнопки
            main_button.check_hover(pygame.mouse.get_pos())
            #  рисуем кнопки
            main_button.draw(screen)

        elif flag == 'lose':
            image = pygame.image.load('img/lose/lose.png')
            image = pygame.transform.scale(image, (screen_width, screen_height))
            screen.blit(image, (0, 0))
            #  Проверяем положение мыши относительно кнопки
            return_button.check_hover(pygame.mouse.get_pos())
            main_button.check_hover(pygame.mouse.get_pos())
            #  рисуем кнопки
            return_button.draw(screen)
            main_button.draw(screen)
        pygame.display.flip()
def interface_lvl3(hero_hp, enemy_hp):  # функция интерфейса 2 уровня
    pygame.draw.rect(screen, blue, (30, 80, hero_hp * 2, 30))   # рисуем здоровье героя
    pygame.draw.rect(screen, green, (27, 120, cooldown * 2, 20))    # рисуем задержку атаки
    pygame.draw.rect(screen, red, (1058, 80, enemy_hp * 2, 30))  # рисуем здоровье врага
    pygame.draw.rect(screen, dark_blue, (27, 77, 203, 33), 3)   # рисуем рамку здоровья героя
    pygame.draw.rect(screen, dark_blue, (1055, 77, 203, 33), 3)  # рисуем рамку здоровья врага
    hero_name = interface_font.render('Такеши', True, dark_blue)    # задаём шрифт и цвет для имени героя
    screen.blit(hero_name, (28, 40))    # рисуем имя героя
    enemy_name = interface_font.render('Кадзуо', True, dark_blue)   # задаём шрифт и цвет для имени врага
    screen.blit(enemy_name, (1120, 40))  # рисуем имя врага

is_jump = False     # Проверка нахождения в прыжке
def lvl3():
    # переменные из вне
    global player_x, player_y, frame_index, frame_count, fl_left, fl_right, fl_nothing, fl_attack, side, \
        frame_count_idle, frame_count_attack, frame_count_jump, jump_count, frame, enemy_health, is_jump, y_velocity, \
        cooldown, pause, enemy_walk_anim, attack_flag, enemy_attack, hero_health, attack_cooldown, \
        active_lvl, enemy_attack_anim, run, enemy_x
    # переменные из вне
    active_lvl = 2  # активный уровень 2
    while run:  # запускаем цикл
        clock.tick(fps)     # устанавливаем скорость переключения кадров 30
        draw_bg(3)  # рисуем карту
        interface_lvl3(hero_health, enemy_health)   # Вызываем интерфейс
        for event in pygame.event.get():    # обрабатываем события
            if event.type == pygame.QUIT:   # если нажали крестик
                pygame.quit()   # выходим из pygame
                sys.exit()  # закрываем
            elif event.type == pygame.KEYDOWN:  # если нажали клавишу
                if event.key == pygame.K_d and not fl_attack:   # если нажали клавишу D и не атакуем
                    fl_nothing = False  # флаг AFK больше не работает
                    fl_right = True  # флаг идти направо работает
                    side = 0   # 0 - вправо
                elif event.key == pygame.K_a and not fl_attack:  # если нажали клавишу A и не атакуем
                    fl_nothing = False  # флаг AFK больше не работает
                    fl_left = True  # флаг идти налево работает
                    side = 1    # 1 - влево
                elif event.key == pygame.K_e and cooldown == 0 and enemy_x > player_x:  # если нажали клавишу E и прошла задержка
                    fl_nothing = False  # флаг AFK больше не работает
                    frame_index = 1     # Нам нужен индекс 1
                    fl_attack = True    # флаг атаки работает
                    frame = get_image(takeshi_animation, player_width, player_height, frame_index,
                                      frame_count_attack, black)    # берём нужный нам кадр
                elif event.key == pygame.K_q and cooldown == 0 and enemy_x < player_x:  # если нажали клавишу Q и прошла задержка
                    fl_nothing = False  # флаг AFK больше не работает
                    frame_index = 0     # Нам нужен индекс 0
                    fl_attack = True    # флаг атаки работает
                    frame = get_image(takeshi_animation, player_width, player_height, frame_index,
                                      frame_count_attack, black)    # берём нужный нам кадр
                elif event.key == pygame.K_SPACE:   # если нажали клавишу пробел
                    fl_nothing = False  # флаг AFK больше не работает
                    is_jump = True  # флаг прыжка работает
                elif event.key == pygame.K_ESCAPE:  # если нажали клавишу ESC
                    pause = True    # запускаем цикл паузы
                    pause_menu()    # вызываем паузу
            elif event.type == pygame.KEYUP:    # если отпустили клавишу
                fl_left = fl_right = fl_attack = False  # флаг ходьбы и атаки не работают
                fl_nothing = True   # флаг AFK работает
                if event.key == pygame.K_e:
                    if cooldown == 0:
                        cooldown = 90  # задержка чтобы персонаж не атаковал постоянно
                    fl_attack = False
                elif event.key == pygame.K_q:
                    if cooldown == 0:
                        cooldown = 90  # задержка чтобы персонаж не атаковал постоянно
                    fl_attack = False
        if is_jump:   # если флаг прыжка работает
            player_y -= y_velocity  # начинаем перемещать героя
            y_velocity -= gravity   # задействуем гравитацию
            if y_velocity < -jump_count:    # если приземлились
                is_jump = False     # флаг прыжка не работает
                y_velocity = jump_count  # обновляем высоту прыжка
            if side == 1:   # если смотрели вправо
                frame_index = 4  # нужна строчка анимации 4
                frame = get_image(takeshi_animation, player_width, player_height, frame_index,
                                  frame_count_jump, black)  # берём нужный нам кадр
            elif side == 0:     # если смотрели влево
                frame_index = 5  # нужна строчка анимации 5
                frame = get_image(takeshi_animation, player_width, player_height, frame_index,
                                  frame_count_jump, black)  # берём нужный нам кадр
        elif not fl_attack and not fl_left and not fl_right:    # если не атакуем и не идём
            frame_index = 6     # нужна строчка анимации 6
            frame = get_image(takeshi_animation, player_width, player_height,
                              frame_index, frame_count_idle, black)     # берём нужный нам кадр
        if fl_right:    # если флаг идти вправо активен
            if player_x <= 1150:    # если мы не у края окна
                player_x = player_x + player_walking_speed  # идём
            else:
                player_x -= player_walking_speed    # не идём
            frame_index = 3     # нужна строчка анимации 3
            frame = get_image(takeshi_animation, player_width, player_height,
                              frame_index, frame_count // 4, black)  # берём нужный нам кадр
        elif fl_left:   # если флаг идти влево активен
            if player_x > 20:    # если мы не у края окна
                player_x = player_x - player_walking_speed  # идём
            else:
                player_x += player_walking_speed    # не идём
            frame_index = 2     # нужна строчка анимации 2
            frame = get_image(takeshi_animation, player_width, player_height,
                              frame_index, frame_count // 4, black)     # берём нужный нам кадр
        elif fl_nothing and not is_jump:    # если мы AFK и не в воздухе
            frame_index = 6     # нужна строчка анимации 6
            frame = get_image(takeshi_animation, player_width, player_height,
                              frame_index, frame_count_idle, black)     # берём нужный нам кадр
        if frame_count != 20:   # пока счётчик не дойдёт до 20
            frame_count += 1    # увеличиваем
        else:
            frame_count = 0     # обнуляем
        if cooldown != 0:   # пока задержка не дойдёт до 0
            cooldown -= 1   # уменьшаем
        if enemy_walk_anim != 27:   # пока счётчик не дойдёт до 27
            enemy_walk_anim += 1    # увеличиваем
        else:
            enemy_walk_anim = 0     # обнуляем
        player_rect = pygame.Rect((player_x, player_y), (190, 180))  # берём невидимую область вокруг героя 200 на 200
        enemy_rect = pygame.Rect((enemy_x, 428), (190, 180))    # берём невидимую область вокруг врага 200 на 200
        if player_rect.colliderect(enemy_rect):    # смотрим столкновения
            attack_flag = True  # флаг атаки героя активен
            enemy_attack = True  # флаг атаки врага активен
        else:
            attack_flag = enemy_attack = False  # флаг атаки врага и героя неактивен
        if attack_flag and fl_attack:   # если флаг атаки героя и атака активны
            damage(0)
        elif enemy_attack and attack_cooldown == 0:  # флаг атаки врага активен и задержка атаки = 0
            damage(1)
        if attack_cooldown != 0:
            attack_cooldown -= 1
        else:
            attack_cooldown = 0
        screen.blit(frame, (player_x, player_y))    # рисуем героя
        enemy = Enemy(player_x)     # обращаемся к классу врага
        enemy.update_position(enemy_attack)  # обновляем позицию
        enemy.drawing()  # рисуем врага
        pygame.display.flip()   # обновляем экран

def damage(hit):
    global enemy_health, hero_health, attack_cooldown, enemy_attack_anim, fl_attack
    if hit == 0:
        if enemy_health > 5:  # Если здоровье врага не 0
            enemy_health -= 5  # убавляем здоровье врага
            fl_attack = False
            enemy_pain_sound.play()  # проигрываем звук урона
        else:
            end_of_game('win')  # выводим экран победы
    elif hit == 1:
        if hero_health > 5:  # Если здоровье героя больше 5
            hero_health -= 5  # убавляем здоровье героя
            hero_pain_sound.play()  # проигрываем звук урона
            attack_cooldown = 90  # задержка атаки
            enemy_attack_anim = 4  # кадр анимации атаки врага
        else:
            end_of_game('lose')  # выводим экран проигрыша

menu()  # при запуске файла вызываем меню
