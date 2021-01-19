import sys
import os
import pygame
import pygame_gui
import pytmx
from random import choice, randint


def main(cells, cells_spawn, objects, waterr, map, num_map, x, y):
    '''Основная функция, в которой и происходит весь игровой процесс'''
    global amount_enemies, death_enemies, enemies_coords, kill_enemy, \
        player_death, death_enemies_coords, counter_of_loudness, \
        difficulty_of_game, free_cells, free_cells_spawn, \
        transparent_objects, water, num_of_map, volume, passed_maps
    for sprite in player_group:
        sprite.kill()
    for sprite in enemies_group:
        sprite.kill()
    for sprite in objects_group:
        sprite.kill()
    for sprite in additional_objects:
        sprite.kill()
    for sprite in coin_group:
        sprite.update_balance()
    num_of_map = num_map
    pygame.display.flip()
    death_enemies_coords = []
    free_cells = cells
    free_cells_spawn = cells_spawn
    transparent_objects = objects
    water = waterr
    volume = 100
    kill_enemy = []
    player_death = []
    enemies_coords = []
    amount_enemies = 0
    death_enemies = 0
    Heart()
    pygame.mixer.music.set_volume(volume // 100)
    player, level_x, level_y = generate_level(load_level(map), x, y)
    Border(0, 0, WIDTH, 50)
    Border(0, HEIGHT, WIDTH, HEIGHT + 1)
    Border(0, 0, -1, HEIGHT)
    Border(WIDTH, 0, WIDTH + 1, HEIGHT)
    MYEVENTTYPE = pygame.USEREVENT + 200
    if difficulty_of_game == 'Легкая':
        MYEVENTTYPE = pygame.USEREVENT + 200
    elif difficulty_of_game == 'Средняя':
        MYEVENTTYPE = pygame.USEREVENT + 400
    else:
        MYEVENTTYPE = pygame.USEREVENT + 600
    pygame.time.set_timer(MYEVENTTYPE, 1000)
    for _ in range(randint(2, 4)):
        Enemy(level_x, level_y)
        amount_enemies += 1
    running = True
    while running:
        for event in pygame.event.get():
            if kill_enemy:
                pygame.mixer.music.load('sound/death.mp3')
                pygame.mixer.music.play()
                kill_enemy.pop(0).death()
                death_enemies += 1
            if player_death:
                player_death.pop(0).death()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                player_group.update(pygame.key.get_pressed())
            if event.type == MYEVENTTYPE:
                for sprite in enemies_group:
                    sprite.add_coords()
                for sprite in enemies_group:
                    sprite.update(player.rect.x, player.rect.y)
                enemies_coords.clear()
        if kill_enemy:
            kill_enemy[0].image = load_image('empty_image.png')
        if player_death:
            player_death[0].image = load_image('empty_image.png')
        bullet_group.update()
        tiles_group.draw(screen)
        additional_objects.draw(screen)
        player_group.draw(screen)
        enemies_group.draw(screen)
        bullet_group.draw(screen)
        objects_group.draw(screen)
        heart_group.draw(screen)
        coin_group.draw(screen)
        for sprite in coin_group:
            sprite.update_balance()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
    sys.exit()


def load_level(filename):
    '''Загрузка карты'''
    global level_map, tile_size, height_map, width_map
    level_map = pytmx.load_pygame('maps/{}'.format(filename))
    width_map = level_map.width
    height_map = level_map.height
    tile_size = level_map.tilewidth
    return level_map


def load_image(name):
    '''Загрузка изображения'''
    fullname = os.path.join('data/', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


def generate_level(level, pos_x, pos_y):
    '''Создание уровня игры(отрисовка карты)'''
    for y in range(height_map):
        for x in range(width_map):
            image = level.get_tile_image(x, y, 0)
            Tile(x, y, image)
            if level.get_tile_image(x, y, 1):
                image = level.get_tile_image(x, y, 1)
                Object(x, y, image)
            if level.get_tile_image(x, y, 2):
                image = level.get_tile_image(x, y, 2)
                AdditionalObjects(x, y, image)
    new_player = MainCharacter(pos_x, pos_y)
    return new_player, pos_x, pos_y


def search_place(x, y):
    '''Поиск свободной клетки для расположения вражеского танка'''
    while True:
        pos_x, pos_y = randint(0, width_map - 1), randint(0, height_map - 1)
        if abs(x - pos_x) <= 2 or abs(y - pos_y) <= 2:
            continue
        if level_map.tiledgidmap[level_map.get_tile_gid(pos_x, pos_y, 1)] \
                in free_cells_spawn:
            return pos_x, pos_y


def terminate():
    '''Выохд из приложения'''
    pygame.quit()
    sys.exit()


def maps(key=None):
    '''Открывается окно выбора карты, на которой игрок хочет сыграть,
     но карты проходятся одна за другой'''
    if key:
        if key == 1:
            free_cells = [130, 131, 132, 144, 305, 306, 307]
            free_cells_spawn = [130, 131, 132, 144]
            transparent_objects = [156, 158, 160]
            water = [1, 2, 3, 13, 14, 15, 25, 26, 27, 37, 38, 39, 49, 50, 51]
            main(free_cells, free_cells_spawn, transparent_objects, water,
                 'map_1.tmx', 1, 0, 11)
        if key == 2:
            free_cells = [20, 130, 131, 132, 144, 168, 255, 289, 407, 408,
                          1610612866, 1610612867,
                          1610612868, 2147484056, 2147484055]
            free_cells_spawn = [130, 131, 132, 289, 1610612866, 1610612867,
                                1610612868]
            transparent_objects = [400, 403, 405]
            water = [13, 25, 26, 27, 145]
            main(free_cells, free_cells_spawn, transparent_objects, water,
                 'map_2.tmx', 2, 0, 0)
    screen.blit(maps_fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 32 < event.pos[0] < 300 and 15 < event.pos[1] < 185:
                    free_cells = [130, 131, 132, 144, 305, 306, 307]
                    free_cells_spawn = [130, 131, 132, 144]
                    transparent_objects = [156, 158, 160]
                    water = [1, 2, 3, 13, 14, 15, 25, 26, 27, 37, 38, 39,
                             49, 50, 51]
                    main(free_cells, free_cells_spawn, transparent_objects,
                         water, 'map_1.tmx', 1, 0, 12)
                if 637 < event.pos[0] < 934 and 15 < event.pos[1] < 195 and \
                        passed_maps == 1:
                    free_cells = [20, 130, 131, 132, 144, 168, 255, 289, 407,
                                  408, 1610612866, 1610612867,
                                  1610612868, 2147484056, 2147484055]
                    free_cells_spawn = [130, 131, 132, 289, 1610612866,
                                        1610612867, 1610612868]
                    transparent_objects = [400, 403, 405]
                    water = [13, 25, 26, 27, 145]
                    main(free_cells, free_cells_spawn, transparent_objects,
                         water, 'map_2.tmx', 2, 0, 1)
                if 637 < event.pos[0] < 934 and 15 < event.pos[1] < 195 and \
                        passed_maps != 1:
                    font = pygame.font.Font(None, 50)
                    text = font.render("Чтобы сыграть на этой карте"
                                       " пройдите предыдущую", True, (0, 0, 0))
                    screen.blit(text, (50, 250))
        pygame.display.flip()


def shop():
    '''Создание окна внутриигрового магазина, осуществление покупки нового
     танка в том случае, если у игрока есть необходимая сумма'''
    global main_character_image
    fon = pygame.transform.scale(load_image('fon_shop.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Назад", True, (0, 0, 0))
    img_x_1 = WIDTH - 120
    img_y_1 = HEIGHT - 40
    img_x_2 = text.get_width()
    img_y_2 = text.get_height()
    pygame.draw.rect(screen, (60, 170, 60), (img_x_1, img_y_1,
                                             img_x_2, img_y_2))
    screen.blit(text, (img_x_1, img_y_1))
    img2_x_1 = 100
    img2_y_1 = 100
    screen.blit(load_image(shop_images[0]), (img2_x_1, img2_y_1))
    text2 = font.render('15', True, (0, 0, 0))
    screen.blit(text2, (img2_x_1 + 100, img2_y_1 + 10))
    img3_x_1 = 100
    img3_y_1 = 200
    screen.blit(load_image(shop_images[1]), (img3_x_1, img3_y_1))
    text3 = font.render('15', True, (0, 0, 0))
    screen.blit(text3, (img3_x_1 + 100, img3_y_1 + 10))
    img4_x_1 = 100
    img4_y_1 = 300
    screen.blit(load_image(shop_images[2]), (img4_x_1, img4_y_1))
    text4 = font.render('15', True, (0, 0, 0))
    screen.blit(text4, (img4_x_1 + 100, img4_y_1 + 10))
    for sprite in coin_group:
        coin = sprite
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if img_x_1 < event.pos[0] < img_x_2 + img_x_1 and \
                        img_y_1 < event.pos[1] < img_y_2 + img_y_1:
                    start_screen()
                if coin.value >= 15:
                    if img2_x_1 < event.pos[0] < img2_x_1 + 50 and \
                            img2_y_1 < event.pos[1] < img2_y_1 + 50:
                        main_character_image = load_image(shop_images[0])
                    if img3_x_1 < event.pos[0] < img3_x_1 + 50 and \
                            img3_y_1 < event.pos[1] < img3_y_1 + 50:
                        main_character_image = load_image(shop_images[1])
                    if img4_x_1 < event.pos[0] < img4_x_1 + 50 and \
                            img4_y_1 < event.pos[1] < img4_y_1 + 50:
                        main_character_image = load_image(shop_images[2])
                    warning = font.render("Успешно куплено!", True, (0, 0, 0))
                    screen.blit(warning, (100, 400))
                    coin.value -= 15
                else:
                    warning = font.render("У вас недостаточно монет!",
                                          True, (0, 0, 0))
                    screen.blit(warning, (100, 400))
        coin_group.draw(screen)
        coin.update_balance()
        pygame.display.flip()


def settings():
    '''Создание меню настроек, в котором выставляется уровень сложности
     и меняется громкость звуков'''
    global counter_of_loudness, settings_, menu, back, exit, \
        difficulty, difficulty_print, volume_1, volume_print, volume_print_2, \
        volume, difficulty_of_game
    settings_pos_x = 400
    settings_pos_y = 200
    settings_width = 400
    settings_height = 300
    pygame.draw.rect(screen, (77, 77, 77), (settings_pos_x, settings_pos_y,
                                            settings_width, settings_height))
    if counter_of_loudness == 0:
        settings_ = pygame_gui.elements.UILabel(
            text='Настройки',
            relative_rect=pygame.Rect((settings_pos_x,
                                       settings_pos_y, settings_width, 20)),
            manager=manager
        )
        menu = pygame_gui.elements.ui_button.UIButton(
            relative_rect=pygame.Rect((settings_pos_x,
                                       settings_pos_y + settings_height - 20,
                                       210, 20)),
            text='Вернуться в главное меню',
            manager=manager
        )

        back = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((settings_pos_x + 210,
                                       settings_pos_y + settings_height - 20,
                                       60, 20)),
            text='Назад',
            manager=manager
        )
        exit = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((settings_pos_x + settings_width - 130,
                                       settings_pos_y + settings_height - 20,
                                       130, 20)),
            text='Выйти из игры',
            manager=manager
        )
        difficulty_print = pygame_gui.elements.UILabel(
            text='Уровень сложности',
            relative_rect=pygame.Rect((settings_pos_x + 10,
                                       settings_pos_y + 30, 150, 20)),
            manager=manager,
        )
        difficulty = pygame_gui.elements.UIDropDownMenu(
            options_list=['Легкая', 'Средняя', 'Тяжелая'],
            starting_option='Легкая',
            relative_rect=pygame.Rect((settings_pos_x + 10,
                                       settings_pos_y + 50, 150, 20)),
            manager=manager
        )
        volume_1 = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((settings_pos_x + 10,
                                       settings_pos_y + 100, 150, 20)),
            start_value=100,
            value_range=(0, 100),
            manager=manager
        )
        volume_print_2 = pygame_gui.elements.UILabel(
            text='Громкость',
            relative_rect=pygame.Rect((settings_pos_x + 10,
                                       settings_pos_y + 80, 150, 20)),
            manager=manager,
        )
        volume_print = pygame_gui.elements.UILabel(
            text='',
            relative_rect=pygame.Rect((settings_pos_x + 10,
                                       settings_pos_y + 80, 40, 20)),
            manager=manager,
        )
        counter_of_loudness += 1
    while True:
        time_delta = clock.tick(fps) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    volume = event.value
                    volume_print.set_text(str(volume))
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    pygame.draw.rect(screen, (77, 77, 77),
                                     (settings_pos_x + 5,
                                      settings_pos_y + 71, 155, 65))
                    difficulty_of_game = event.text
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == menu:
                        start_screen()
                    if event.ui_element == back:
                        return True
                    if event.ui_element == exit:
                        terminate()
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()


def graphic_start_screen():
    '''Создание графического интерфейса для главного окна'''
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Играть", True, (179, 68, 108))
    text_x_1 = 400
    text_y_1 = 550
    text_x_2 = text.get_width()
    text_y_2 = text.get_height()
    pygame.draw.rect(screen, (60, 170, 60), (text_x_1 - 10, text_y_1 - 10,
                                             text_x_2 + 20, text_y_2 + 20))
    screen.blit(text, (text_x_1, text_y_1))
    text2 = font.render("Настройки", True, (179, 68, 108))
    text2_x_1 = 650
    text2_y_1 = 550
    text2_x_2 = text2.get_width()
    text2_y_2 = text2.get_height()
    pygame.draw.rect(screen, (60, 170, 60), (text2_x_1 - 10, text2_y_1 - 10,
                                             text2_x_2 + 20, text2_y_2 + 20))
    screen.blit(text2, (text2_x_1, text2_y_1))

    text3 = font.render("Магазин", True, (179, 68, 108))
    text3_x_1 = 510
    text3_y_1 = 620
    text3_x_2 = text3.get_width()
    text3_y_2 = text3.get_height()
    pygame.draw.rect(screen, (60, 170, 60), (text3_x_1 - 10, text3_y_1 - 10,
                                             text3_x_2 + 20, text3_y_2 + 20))
    screen.blit(text3, (text3_x_1, text3_y_1))
    return (text_x_1, text_x_2, text_y_1, text_y_2,
            text2_x_1, text2_x_2, text2_y_1, text2_y_2,
            text3_x_1, text3_x_2, text3_y_1, text3_y_2)


def start_screen():
    '''Главное окно, откуда осуществляется переход в настройки,
     запуск игры, переход во внутриигровой магазин'''
    (text_x_1, text_x_2, text_y_1, text_y_2,
     text2_x_1, text2_x_2, text2_y_1, text2_y_2,
     text3_x_1, text3_x_2, text3_y_1, text3_y_2) = graphic_start_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if text_x_1 < event.pos[0] < text_x_2 + text_x_1 and \
                        text_y_1 < event.pos[1] < text_y_2 + text_y_1:
                    maps()
                elif text2_x_1 < event.pos[0] < text2_x_2 + text2_x_1 and \
                        text2_y_1 < event.pos[1] < text2_y_2 + text2_y_1:
                    if settings():
                        (text_x_1, text_x_2, text_y_1, text_y_2,
                         text2_x_1, text2_x_2, text2_y_1, text2_y_2,
                         text3_x_1, text3_x_2, text3_y_1, text3_y_2) \
                            = graphic_start_screen()
                elif text3_x_1 < event.pos[0] < text3_x_2 + text3_x_1 and \
                        text3_y_1 < event.pos[1] < text3_y_2 + text3_y_1:
                    shop()
        coin_group.draw(screen)
        for sprite in coin_group:
            sprite.update_balance()
        pygame.display.flip()


def victory():
    '''Функция победы, при уничтожении главного персонажа открывается окно
     с информационной надписью и несколькими кнопками'''
    pygame.mixer.music.load('sound/win.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.play()
    global passed_maps
    font = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 25)

    pygame.draw.rect(screen, (255, 160, 137), (425, 350, 400, 300))
    text = font.render("Вы победили!", True, (179, 68, 108))
    screen.blit(text, (500, 375))

    pygame.draw.rect(screen, (77, 77, 77), (425, 630, 225, 20))
    text2 = font2.render("Вернуться в главное меню", True, (0, 0, 0))
    screen.blit(text2, (425, 630))

    pygame.draw.rect(screen, (77, 77, 77), (651, 630, 174, 20))
    text3 = font2.render("Перейти к меню карт", True, (0, 0, 0))
    screen.blit(text3, (650, 630))
    passed_maps = num_of_map
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 425 < event.pos[0] < 650 and 630 < event.pos[1] < 650:
                    start_screen()
                if 651 < event.pos[0] < 825 and 630 < event.pos[1] < 650:
                    maps()
        pygame.display.flip()


def defeat():
    '''Функция проигрыша, при уничтожении главного персонажа открывается окно
     с информационной надписью и несколькими кнопками'''
    pygame.mixer.music.load('sound/losing.mp3')
    pygame.mixer.music.play()
    font = pygame.font.Font(None, 50)
    font2 = pygame.font.Font(None, 25)

    pygame.draw.rect(screen, (255, 160, 137), (425, 350, 400, 300))
    text = font.render("Вы проиграли!", True, (179, 68, 108))
    screen.blit(text, (500, 375))

    pygame.draw.rect(screen, (77, 77, 77), (425, 630, 225, 20))
    text2 = font2.render("Вернуться в главное меню", True, (0, 0, 0))
    screen.blit(text2, (425, 630))

    pygame.draw.rect(screen, (77, 77, 77), (685, 630, 140, 20))
    text3 = font2.render("Сыграть заново", True, (0, 0, 0))
    screen.blit(text3, (685, 630))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 425 < event.pos[0] < 650 and 630 < event.pos[1] < 650:
                    start_screen()
                if 651 < event.pos[0] < 825 and 630 < event.pos[1] < 650:
                    maps(num_of_map)
        pygame.display.flip()


class Tile(pygame.sprite.Sprite):
    '''Класс объектов, объекты над которыми персонажи должны перемещаться'''

    def __init__(self, pos_x, pos_y, image):
        super().__init__(tiles_group)
        self.image = image
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y)


class Object(pygame.sprite.Sprite):
    '''Класс объектов, объекты под которыми персонажи должны перемещаться,
     либо объекты, которые являются преградой'''

    def __init__(self, pos_x, pos_y, image):
        super().__init__(objects_group)
        self.id = level_map.tiledgidmap[level_map.get_tile_gid(pos_x,
                                                               pos_y, 1)]
        self.image = image
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y)


class AdditionalObjects(pygame.sprite.Sprite):
    '''Класс дополнительных объектов, объекты над которыми
     персонажи должны перемещаться'''

    def __init__(self, pos_x, pos_y, image):
        super().__init__(additional_objects)
        self.id = level_map.tiledgidmap[level_map.get_tile_gid(pos_x,
                                                               pos_y, 2)]
        self.image = image
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y)


class Heart(pygame.sprite.Sprite):
    '''Класс отображения количества жизней персонажа'''

    def __init__(self):
        super().__init__(heart_group)
        self.image = load_image(heart_images[0])
        self.rect = self.image.get_rect().move(0, 0)
        self.counter = 0

    def update_image(self):
        '''Изменение картинки жизней персонажа(сердечка)'''
        if self.counter == 0:
            self.image = load_image(heart_images[1])
            self.counter += 1
        else:
            self.image = load_image('empty_image.png')
        heart_group.draw(screen)
        pygame.display.flip()


class Coin(pygame.sprite.Sprite):
    '''Класс баланса персонажа, здесь происходит создание картинки,
     изменение баланса, вывод картинки монеты'''

    def __init__(self):
        super().__init__(coin_group)
        self.image = coin_image
        self.rect = self.image.get_rect().move(100, 0)
        self.font = pygame.font.Font(None, 50)
        self.value = 0
        self.update_balance()

    def update_balance(self):
        '''Вывод на экран баланса персонажа'''
        self.text = self.font.render(str(self.value), True, (0, 0, 0))
        screen.blit(self.text, (165, 10))


class Bullet(pygame.sprite.Sprite):
    '''Класс снаряда, в нем происходит передвижение и основная логика
     передвижения снаряда'''

    def __init__(self, pos_x, pos_y, side, from_):
        super().__init__(bullet_group)
        self.image = bullet_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.side = side
        self.speed = 0
        self.from_ = from_
        if self.side == 'u':
            self.image = pygame.transform.rotate(self.image, 90)
            self.speed = -15
            self.rect = self.image.get_rect().move(self.pos_x + 22,
                                                   self.pos_y)
        elif self.side == 'd':
            self.image = pygame.transform.rotate(self.image, -90)
            self.speed = 15
            self.rect = self.image.get_rect().move(self.pos_x + 22,
                                                   self.pos_y + 50)
        elif self.side == 'r':
            self.speed = 15
            self.rect = self.image.get_rect().move(self.pos_x + 50,
                                                   self.pos_y + 22)
        elif self.side == 'l':
            self.image = pygame.transform.flip(self.image, True, False)
            self.speed = -15
            self.rect = self.image.get_rect().move(self.pos_x,
                                                   self.pos_y + 22)

    def update(self):
        '''Перемещение снаряда и проверка на столкновение
         с каким-либо спрайтом'''
        if self.side in ['u', 'd']:
            self.rect.y += self.speed
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.kill()
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id not \
                        in transparent_objects and \
                        pygame.sprite.spritecollideany(self,
                                                       objects_group).id \
                        not in free_cells:
                    self.kill()
            if self.from_ == 'player':
                if pygame.sprite.spritecollideany(self, enemies_group) and \
                        pygame.sprite.spritecollideany(self,
                                                       enemies_group
                                                       ).state == 1:
                    if pygame.sprite.spritecollideany(self,
                                                      enemies_group) \
                            not in kill_enemy:
                        kill_enemy. \
                            append(pygame.sprite.
                                   spritecollideany(self, enemies_group))
                        self.kill()
            else:
                if pygame.sprite.spritecollideany(self, player_group):
                    pygame.mixer.music.load('sound/death.mp3')
                    pygame.mixer.music.play()
                    player_death.append(
                        pygame.sprite.spritecollideany(self,
                                                       player_group))
                    for sprite in heart_group:
                        sprite.update_image()
                    self.kill()
        else:
            self.rect.x += self.speed
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.kill()
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id \
                        not in transparent_objects and \
                        pygame.sprite.spritecollideany(self,
                                                       objects_group).id \
                        not in free_cells:
                    self.kill()
            if self.from_ == 'player':
                if pygame.sprite.spritecollideany(self, enemies_group) and \
                        pygame.sprite.spritecollideany(self, enemies_group) \
                                .state == 1:
                    if pygame.sprite.spritecollideany(self, enemies_group) \
                            not in kill_enemy:
                        kill_enemy.append(
                            pygame.sprite.spritecollideany(self,
                                                           enemies_group))
                        self.kill()
            else:
                if pygame.sprite.spritecollideany(self, player_group):
                    pygame.mixer.music.load('sound/death.mp3')
                    pygame.mixer.music.play()
                    player_death.append(
                        pygame.sprite.spritecollideany(self,
                                                       player_group))
                    for sprite in heart_group:
                        sprite.update_image()
                    self.kill()


class Enemy(pygame.sprite.Sprite):
    '''Класс противника, в нем происходит передвижение, анимация уничтожения,
     звуковое сопровождение при передвижении'''

    def __init__(self, main_character_x, main_character_y):
        super().__init__(enemies_group)
        self.pos_x, self.pos_y = search_place(main_character_x,
                                              main_character_y)
        self.image = load_image(choice(enemies_images))
        self.rect = self.image.get_rect().move(
            tile_size * self.pos_x, tile_size * self.pos_y)
        self.state = 1
        self.side = 'r'
        self.angle = 0
        self.cut_sheet()
        self.collision = 0
        self.movement = 1
        self.sound()

    def sound(self):
        '''Включение звука передвижения противников'''
        self.channel = pygame.mixer.Channel(0)
        self.channel.play(movement_sound, loops=-1)

    def add_coords(self):
        '''Добавление текущих координат противников в список,
         это нужно для передвижения противника'''
        enemies_coords.append([self.rect.x // tile_size,
                               self.rect.y // tile_size])

    def death(self):
        '''В функции происходит анимация уничтожения противника'''
        self.movement = 0
        if self.state != 0:
            self.state = 0
            death_enemies_coords.append([self.rect.x // tile_size,
                                         self.rect.y // tile_size])
            self.image = self.image_2
            for i in range(7):
                enemies_group.draw(screen)
                pygame.display.flip()
                self.update_death()
        for sprite in coin_group:
            sprite.value += randint(1, 5)
            sprite.update_balance()

    def cut_sheet(self):
        '''Разрезание картинки с анимацией на отдельные картинки'''
        self.frames = []
        self.cur_frame = 0
        sheet, columns, rows = image_death, 8, 1
        self.rect_3 = pygame.Rect(0, 0, sheet.get_width() // columns,
                                  sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect_3.w * i, self.rect_3.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect_3.size)))
        self.image_2 = self.frames[self.cur_frame]

    def update_death(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def update(self, fin_x, fin_y):
        '''Передвижение противника'''
        if amount_enemies - death_enemies == 0:
            self.channel.stop()
            victory()
        if self.state != 0:
            INF = 1000
            x, y = self.rect.x // tile_size, self.rect.y // tile_size
            distance = [[INF] * width_map for _ in range(height_map)]
            distance[y][x] = 0
            prev = [[None] * width_map for _ in range(height_map)]
            queue = [(x, y)]
            while queue:
                x, y = queue.pop(0)
                for dx, dy in (1, 0), (0, -1), (-1, 0), (0, 1):
                    next_x, next_y = x + dx, y + dy
                    if 0 <= next_x < width_map and 0 <= next_y < height_map \
                            and (level_map.tiledgidmap
                                 [level_map.get_tile_gid(next_x, next_y, 1)]
                                 in free_cells_spawn or
                                 level_map.tiledgidmap
                                 [level_map.get_tile_gid(next_x, next_y, 1)]
                                 in transparent_objects) and \
                            distance[next_y][next_x] == INF and \
                            [next_x, next_y] not in enemies_coords and \
                            [next_x, next_y] not in death_enemies_coords:
                        distance[next_y][next_x] = distance[y][x] + 1
                        prev[next_y][next_x] = (x, y)
                        queue.append((next_x, next_y))
            x, y = fin_x // tile_size, fin_y // tile_size
            if distance[y][x] == INF or (self.rect.x, self.rect.y) == \
                    (fin_x, fin_y):
                pass
            else:
                while prev[y][x] != (self.rect.x // tile_size,
                                     self.rect.y // tile_size):
                    x, y = prev[y][x]
                side = self.side
                if x * tile_size > self.rect.x:
                    if self.side != 'r' and self.side != 'l':
                        if side == 'u':
                            self.image = pygame.transform.rotate(
                                self.image, self.angle - 90)
                        else:
                            self.image = pygame.transform.rotate(
                                self.image, self.angle + 90)
                    elif self.side == 'l':
                        self.image = pygame.transform.flip(
                            self.image, True, False)
                    self.side = 'r'
                elif x * tile_size < self.rect.x:
                    if self.side != 'l' and self.side != 'r':
                        if side == 'u':
                            self.image = pygame.transform.rotate(
                                self.image, self.angle + 90)
                        else:
                            self.image = pygame.transform.rotate(
                                self.image, self.angle - 90)
                    elif self.side == 'r':
                        self.image = pygame.transform.flip(
                            self.image, True, False)
                    self.side = 'l'
                elif y * tile_size > self.rect.y:
                    if self.side != 'd' and self.side != 'u':
                        if side == 'r':
                            self.image = pygame.transform.rotate(
                                self.image, self.angle - 90)
                        else:
                            self.image = pygame.transform.rotate(
                                self.image, self.angle + 90)
                    elif self.side == 'u':
                        self.image = pygame.transform.flip(
                            self.image, False, True)
                    self.side = 'd'
                elif y * tile_size < self.rect.y:
                    if self.side != 'u' and self.side != 'd':
                        if side == 'r':
                            self.image = pygame.transform.rotate(
                                self.image, self.angle + 90)
                        else:
                            self.image = pygame.transform.rotate(
                                self.image, self.angle - 90)
                    elif self.side == 'd':
                        self.image = pygame.transform.flip(
                            self.image, False, True)
                    self.side = 'u'
                if x * tile_size == fin_x and y * tile_size == fin_y and \
                        self.collision == 0:
                    pygame.mixer.Sound.play(collision_sound)
                    self.collision = 1
                elif x * tile_size == fin_x and y * tile_size == fin_y and \
                        self.collision != 0:
                    pass
                else:
                    self.collision = 0
                    self.rect.x, self.rect.y = x * tile_size, y * tile_size
                if self.rect.x == fin_x:
                    if self.rect.y > fin_y:
                        if self.side == 'u':
                            Bullet(self.rect.x, self.rect.y, 'u', 'enemy')
                    else:
                        if self.side == 'd':
                            Bullet(self.rect.x, self.rect.y, 'd', 'enemy')
                elif self.rect.y == fin_y:
                    if self.rect.x > fin_x:
                        if self.side == 'l':
                            Bullet(self.rect.x, self.rect.y, 'l', 'enemy')
                    else:
                        if self.side == 'r':
                            Bullet(self.rect.x, self.rect.y, 'r', 'enemy')


class MainCharacter(pygame.sprite.Sprite):
    '''Класс главного персонажа, в нем происходит передвижение персонажа,
     создание, а также открытие иеню настроек, то есть установка паузы во
      время игры'''

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.life = 2
        self.characteristics_character()

    def characteristics_character(self):
        '''Функция, в которой создаются основные атрибуты экземпляра класса'''
        self.image = main_character_image
        self.rect = self.image.get_rect().move(
            tile_size * self.pos_x, tile_size * self.pos_y)
        self.side = 'r'
        self.angle = 0

    def update(self, args):
        '''Передвижение персонажа, в этой функции вся логика передвижения
         персонажа'''
        side = self.side
        if args[pygame.K_ESCAPE]:
            pygame.mixer.Channel(0).pause()
            if settings():
                if difficulty_of_game == 'Легкая':
                    MYEVENTTYPE = pygame.USEREVENT + 200
                    pygame.time.set_timer(MYEVENTTYPE, 1000)
                elif difficulty_of_game == 'Средняя':
                    MYEVENTTYPE = pygame.USEREVENT + 400
                    pygame.time.set_timer(MYEVENTTYPE, 1000)
                else:
                    MYEVENTTYPE = pygame.USEREVENT + 2000
                    pygame.time.set_timer(MYEVENTTYPE, 1000)
                try:
                    pygame.mixer.Channel(0).set_volume(int(int(volume) // 10))
                except TypeError:
                    pygame.mixer.Channel(0).set_volume(100)
                pygame.mixer.Channel(0).unpause()

        if args[pygame.K_UP]:
            if self.side != 'u' and self.side != 'd':
                if side == 'r':
                    self.image = pygame.transform.rotate(
                        self.image, self.angle + 90)
                else:
                    self.image = pygame.transform.rotate(
                        self.image, self.angle - 90)
            elif self.side == 'd':
                self.image = pygame.transform.flip(self.image, False, True)
            self.rect.y -= tile_size
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.rect.y += tile_size
            elif pygame.sprite.spritecollideany(self, enemies_group):
                pygame.mixer.Sound.play(collision_sound)
                self.rect.y += tile_size
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id \
                        in transparent_objects:
                    pass
                elif pygame.sprite.spritecollideany(self, objects_group).id \
                        not in free_cells:
                    self.rect.y += tile_size
            self.side = 'u'

        elif args[pygame.K_DOWN]:
            if self.side != 'd' and self.side != 'u':
                if side == 'r':
                    self.image = pygame.transform.rotate(
                        self.image, self.angle - 90)
                else:
                    self.image = pygame.transform.rotate(
                        self.image, self.angle + 90)
            elif self.side == 'u':
                self.image = pygame.transform.flip(self.image, False, True)
            self.rect.y += tile_size
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.rect.y -= tile_size
            elif pygame.sprite.spritecollideany(self, enemies_group):
                pygame.mixer.Sound.play(collision_sound)
                self.rect.y -= tile_size
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id \
                        in transparent_objects:
                    pass
                elif pygame.sprite.spritecollideany(self, objects_group).id \
                        not in free_cells:
                    self.rect.y -= tile_size
            self.side = 'd'

        elif args[pygame.K_RIGHT]:
            if self.side != 'r' and self.side != 'l':
                if side == 'u':
                    self.image = pygame.transform.rotate(
                        self.image, self.angle - 90)
                else:
                    self.image = pygame.transform.rotate(
                        self.image, self.angle + 90)
            elif self.side == 'l':
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect.x += tile_size
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.rect.x -= tile_size
            elif pygame.sprite.spritecollideany(self, enemies_group):
                pygame.mixer.Sound.play(collision_sound)
                self.rect.x -= tile_size
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id \
                        in transparent_objects:
                    pass
                elif pygame.sprite.spritecollideany(self, objects_group).id \
                        not in free_cells:
                    self.rect.x -= tile_size
            self.side = 'r'

        elif args[pygame.K_LEFT]:
            if self.side != 'l' and self.side != 'r':
                if side == 'u':
                    self.image = pygame.transform.rotate(
                        self.image, self.angle + 90)
                else:
                    self.image = pygame.transform.rotate(
                        self.image, self.angle - 90)
            elif self.side == 'r':
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect.x -= tile_size
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.rect.x += tile_size
            elif pygame.sprite.spritecollideany(self, enemies_group):
                pygame.mixer.Sound.play(collision_sound)
                self.rect.x += tile_size
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id \
                        in transparent_objects:
                    pass
                elif pygame.sprite.spritecollideany(self, objects_group).id \
                        not in free_cells:
                    self.rect.x += tile_size
            self.side = 'l'

        if level_map.tiledgidmap[level_map.get_tile_gid(
                self.rect.x // tile_size,
                self.rect.y // tile_size, 0)] in water and\
                level_map.get_tile_gid(self.rect.x // tile_size,
                                       self.rect.y // tile_size, 2) == 0:
            pygame.mixer.Sound.play(water_sound)
            player_death.append(self)
            for sprite in heart_group:
                sprite.update_image()
        if args[pygame.K_SPACE]:
            pygame.mixer.Sound.play(shot_sound)
            Bullet(self.rect.x, self.rect.y, self.side, 'player')

    def death(self):
        '''Функция, в которой происходит проверка количества жизней персонажа
         и вызов функции поражения при отсутствии оставшихся жизней'''
        self.life -= 1
        if self.life > 0:
            self.characteristics_character()
        elif self.life == 0:
            pygame.mixer.Channel(0).stop()
            defeat()


class Border(pygame.sprite.Sprite):
    '''Класс границ, здесь происходит создание границ,
     за которые не может выехать ни один персонаж'''

    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if y2 - y1 == HEIGHT:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, HEIGHT])
            self.rect = pygame.Rect(x1, y1, x2, y2)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([WIDTH, 1])
            self.rect = pygame.Rect(x1, y1, x2, y2)


'''Начало игры, создание окна, основных нужных переменных,
 констант (добавление картинок, звуков), создание групп спрайтов'''
pygame.init()
pygame.mixer.init()
size = WIDTH, HEIGHT = 1250, 1050
screen = pygame.display.set_mode(size)
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
pygame.display.set_caption('Танчики')
pygame.display.set_icon(load_image('main_character.png'))
main_character_image = load_image('main_character.png')
image_death = load_image('animation_death_2.png')
bullet_image = load_image('bullet.png')
maps_fon = load_image('maps_fon_2.jpg')
enemies_images = ['enemy_1.png', 'enemy_2.png', 'enemy_3.png']
shop_images = ['main_character_2.png', 'main_character_3.png',
               'main_character_4.png']
heart_images = ['heart.png', 'heart_2.png']
coin_image = load_image('coin.png')
death_sound = pygame.mixer.Sound('sound/death.mp3')
collision_sound = pygame.mixer.Sound('sound/collision.mp3')
water_sound = pygame.mixer.Sound('sound/water.mp3')
shot_sound = pygame.mixer.Sound('sound/shot.mp3')
movement_sound = pygame.mixer.Sound('sound/movement.mp3')
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
additional_objects = pygame.sprite.Group()
player_group = pygame.sprite.Group()
heart_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
clock = pygame.time.Clock()
fps = 60
difficulty_of_game = 'Легкая'
counter_of_loudness = 0
passed_maps = 0
Coin()
start_screen()
