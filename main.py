import sys
import os
import pygame
import pytmx
from random import choice, randint


def load_level(filename):
    global level_map, tile_size, height_map, width_map
    level_map = pytmx.load_pygame(f"{'maps'}/{filename}")
    width_map = level_map.width
    height_map = level_map.height
    tile_size = level_map.tilewidth
    return level_map


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


def generate_level(level, pos_x, pos_y):
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
    while True:
        pos_x, pos_y = randint(0, width_map - 1), randint(0, height_map - 1)
        if abs(x - pos_x) <= 2 or abs(y - pos_y) <= 2:
            continue
        if level_map.tiledgidmap[level_map.get_tile_gid(pos_x, pos_y, 1)] in free_cells_spawn:
            return pos_x, pos_y


def terminate():
    pygame.quit()
    sys.exit()


def settings():
    global value, counter_of_loudness
    font1 = pygame.font.Font(None, 20)
    font2 = pygame.font.Font(None, 22)
    settings_pos_x = 400
    settings_pos_y = 200
    settings_width = 400
    settings_height = 300
    pygame.draw.rect(screen, (0, 0, 0), (settings_pos_x, settings_pos_y,
                                         settings_width, settings_height))
    pygame.draw.rect(screen, (179, 179, 179), (settings_pos_x, settings_pos_y,
                                               settings_width, settings_height))
    text1 = font1.render("Настройки", True, (0, 0, 0))
    screen.blit(text1, (settings_pos_x, settings_pos_y))
    text2 = font2.render("Нажмите на поле ниже и введите нужную громкость", True, (0, 0, 0))
    text3 = font2.render("в процентах(от 0 до 100)", True, (0, 0, 0))
    screen.blit(text2, (settings_pos_x, settings_pos_y + 22))
    screen.blit(text3, (settings_pos_x, settings_pos_y + 42))
    pygame.draw.rect(screen, (255, 255, 255), (settings_pos_x, settings_pos_y + 60, 25, 25))
    print(counter_of_loudness)
    if counter_of_loudness == 0:
        value = '100'
        counter_of_loudness += 1
    text5 = font2.render(value, True, (0, 0, 0))
    screen.blit(text5, (settings_pos_x, settings_pos_y + 65))
    flag = False
    pygame.draw.rect(screen, (255, 255, 255), (settings_pos_x + settings_width - 80,
                                               settings_pos_y + settings_height - 20, 80, 20))
    text4 = font2.render("Применить", True, (0, 0, 0))
    screen.blit(text4, (settings_pos_x + settings_width - 80, settings_pos_y + settings_height - 15))
    text6 = font2.render("Выйти из игры", True, (0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (settings_pos_x, settings_pos_y + 100, 115, 25))
    screen.blit(text6, (settings_pos_x, settings_pos_y + 105))
    text7 = font2.render("Выйти из игры", True, (0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (settings_pos_x, settings_pos_y + 100, 115, 25))
    screen.blit(text7, (settings_pos_x, settings_pos_y + 105))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if flag:
                    try:
                        value += event.unicode
                    except ValueError:
                        pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if settings_pos_x < event.pos[0] < settings_pos_x + 20 and\
                        settings_pos_y + 60 < event.pos[1] < settings_pos_y + 80:
                    flag = True
                    value = ''
                    pygame.draw.rect(screen, (255, 255, 255), (settings_pos_x, settings_pos_y + 60, 25, 25))
                else:
                    if flag:
                        flag = False
                        text5 = font2.render(value, True, (0, 0, 0))
                        screen.blit(text5, (settings_pos_x, settings_pos_y + 65))
                if settings_pos_x + settings_width - 80 < event.pos[0] < settings_pos_x + settings_width and \
                        settings_pos_y + settings_height - 20 < event.pos[1] < settings_pos_y + settings_height:
                    return True
                if settings_pos_x < event.pos[0] < settings_pos_x + 115 and \
                        settings_pos_y + 100 < event.pos[1] < settings_pos_y + 125:
                    terminate()
        pygame.display.flip()


def graphic_start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
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
    return text_x_1, text_x_2, text_y_1, text_y_2, text2_x_1, text2_x_2, text2_y_1, text2_y_2



def start_screen():
    counter_of_loudness = 0
    text_x_1, text_x_2, text_y_1, text_y_2, text2_x_1, text2_x_2, text2_y_1, text2_y_2 = graphic_start_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if text_x_1 < event.pos[0] < text_x_2 + text_x_1 and text_y_1 < event.pos[1] < text_y_2 + text_y_1:
                    return True
                elif text2_x_1 < event.pos[0] < text2_x_2 + text2_x_1 and\
                        text2_y_1 < event.pos[1] < text2_y_2 + text2_y_1:
                    if settings():
                        text_x_1, text_x_2, text_y_1, text_y_2, text2_x_1, text2_x_2, text2_y_1, text2_y_2 = graphic_start_screen()
        pygame.display.flip()


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(tiles_group)
        self.image = image
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y)


class Object(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(objects_group)
        self.id = level_map.tiledgidmap[level_map.get_tile_gid(pos_x, pos_y, 1)]
        self.image = image
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y)


class AdditionalObjects(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(additional_objects)
        self.id = level_map.tiledgidmap[level_map.get_tile_gid(pos_x, pos_y, 2)]
        self.image = image
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y)


class Bullet(pygame.sprite.Sprite):
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
            self.speed = -5
            self.rect = self.image.get_rect().move(self.pos_x + 22, self.pos_y)
        elif self.side == 'd':
            self.image = pygame.transform.rotate(self.image, -90)
            self.speed = 5
            self.rect = self.image.get_rect().move(self.pos_x + 22, self.pos_y + 50)
        elif self.side == 'r':
            self.speed = 5
            self.rect = self.image.get_rect().move(self.pos_x + 50, self.pos_y + 22)
        elif self.side == 'l':
            self.image = pygame.transform.flip(self.image, True, False)
            self.speed = -5
            self.rect = self.image.get_rect().move(self.pos_x, self.pos_y + 22)

    def update(self):
        if self.side in ['u', 'd']:
            self.rect.y += self.speed
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.kill()
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id not in transparent_objects and \
                        pygame.sprite.spritecollideany(self, objects_group).id not in free_cells:
                    self.kill()
            if self.from_ == 'player':
                if pygame.sprite.spritecollideany(self, enemies_group) and\
                        pygame.sprite.spritecollideany(self, enemies_group).state == 1:
                    if pygame.sprite.spritecollideany(self, enemies_group) not in kill_enemy:
                        kill_enemy.append(pygame.sprite.spritecollideany(self, enemies_group))
                        self.kill()
            else:
                if pygame.sprite.spritecollideany(self, player_group):
                    pygame.sprite.spritecollideany(self, player_group).death()
                    self.kill()
        else:
            self.rect.x += self.speed
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.kill()
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id not in transparent_objects and \
                        pygame.sprite.spritecollideany(self, objects_group).id not in free_cells:
                    self.kill()
            if self.from_ == 'player':
                if pygame.sprite.spritecollideany(self, enemies_group) and \
                        pygame.sprite.spritecollideany(self, enemies_group).state == 1:
                    if pygame.sprite.spritecollideany(self, enemies_group) not in kill_enemy:
                        kill_enemy.append(pygame.sprite.spritecollideany(self, enemies_group))
                        self.kill()
            else:
                if pygame.sprite.spritecollideany(self, player_group):
                    pygame.sprite.spritecollideany(self, player_group).death()
                    self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, main_character_x, main_character_y):
        super().__init__(enemies_group)
        self.pos_x, self.pos_y = search_place(main_character_x, main_character_y)
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
        self.channel = pygame.mixer.Channel(0)
        self.channel.play(movement_sound, loops=-1)

    def death(self):
        self.movement = 0
        if self.state != 0:
            self.state = 0
            self.image = self.image_2
            x, y = self.rect.x, self.rect.y
            for i in range(7):
                enemies_group.draw(screen)
                pygame.display.flip()
                self.update_death()

    def cut_sheet(self):
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
        if amount_enemies - death_enemies == 0:
            self.channel.stop()
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
                    if 0 <= next_x < width_map and 0 <= next_y < height_map and \
                            (level_map.tiledgidmap[level_map.get_tile_gid(next_x, next_y, 1)] in
                             free_cells_spawn or level_map.tiledgidmap[level_map.get_tile_gid(next_x, next_y, 1)] in
                             transparent_objects) and distance[next_y][next_x] == INF:
                        distance[next_y][next_x] = distance[y][x] + 1
                        prev[next_y][next_x] = (x, y)
                        queue.append((next_x, next_y))
            x, y = fin_x // tile_size, fin_y // tile_size
            if distance[y][x] == INF or (self.rect.x, self.rect.y) == (fin_x, fin_y):
                pass
            else:
                while prev[y][x] != (self.rect.x // tile_size, self.rect.y // tile_size):
                    x, y = prev[y][x]
                side = self.side
                if x * tile_size > self.rect.x:
                    if self.side != 'r' and self.side != 'l':
                        if side == 'u':
                            self.image = pygame.transform.rotate(self.image, self.angle - 90)
                        else:
                            self.image = pygame.transform.rotate(self.image, self.angle + 90)
                    elif self.side == 'l':
                        self.image = pygame.transform.flip(self.image, True, False)
                    self.side = 'r'
                elif x * tile_size < self.rect.x:
                    if self.side != 'l' and self.side != 'r':
                        if side == 'u':
                            self.image = pygame.transform.rotate(self.image, self.angle + 90)
                        else:
                            self.image = pygame.transform.rotate(self.image, self.angle - 90)
                    elif self.side == 'r':
                        self.image = pygame.transform.flip(self.image, True, False)
                    self.side = 'l'
                elif y * tile_size > self.rect.y:
                    if self.side != 'd' and self.side != 'u':
                        if side == 'r':
                            self.image = pygame.transform.rotate(self.image, self.angle - 90)
                        else:
                            self.image = pygame.transform.rotate(self.image, self.angle + 90)
                    elif self.side == 'u':
                        self.image = pygame.transform.flip(self.image, False, True)
                    self.side = 'd'
                elif y * tile_size < self.rect.y:
                    if self.side != 'u' and self.side != 'd':
                        if side == 'r':
                            self.image = pygame.transform.rotate(self.image, self.angle + 90)
                        else:
                            self.image = pygame.transform.rotate(self.image, self.angle - 90)
                    elif self.side == 'd':
                        self.image = pygame.transform.flip(self.image, False, True)
                    self.side = 'u'
                if x * tile_size == fin_x and y * tile_size == fin_y and self.collision != 1:
                    self.collision = 1
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
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.life = 2
        self.characteristics_character()

    def characteristics_character(self):
        self.image = main_character_image
        self.rect = self.image.get_rect().move(
            tile_size * self.pos_x, tile_size * self.pos_y)
        self.side = 'r'
        self.angle = 0

    def update(self, args):
        side = self.side
        if args[pygame.K_ESCAPE]:
            pygame.mixer.Channel(0).pause()
            if settings():
                pygame.mixer.music.set_volume(int(int(value) // 100))
                pygame.mixer.Channel(0).unpause()

        if args[pygame.K_UP]:
            if self.side != 'u' and self.side != 'd':
                if side == 'r':
                    self.image = pygame.transform.rotate(self.image, self.angle + 90)
                else:
                    self.image = pygame.transform.rotate(self.image, self.angle - 90)
            elif self.side == 'd':
                self.image = pygame.transform.flip(self.image, False, True)
            self.rect.y -= tile_size
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.rect.y += tile_size
            elif pygame.sprite.spritecollideany(self, enemies_group):
                pygame.mixer.Sound.play(collision_sound)
                self.rect.y += tile_size
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id in transparent_objects:
                    pass
                elif pygame.sprite.spritecollideany(self, objects_group).id not in free_cells:
                    self.rect.y += tile_size
            self.side = 'u'

        elif args[pygame.K_DOWN]:
            if self.side != 'd' and self.side != 'u':
                if side == 'r':
                    self.image = pygame.transform.rotate(self.image, self.angle - 90)
                else:
                    self.image = pygame.transform.rotate(self.image, self.angle + 90)
            elif self.side == 'u':
                self.image = pygame.transform.flip(self.image, False, True)
            self.rect.y += tile_size
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.rect.y -= tile_size
            elif pygame.sprite.spritecollideany(self, enemies_group):
                pygame.mixer.Sound.play(collision_sound)
                self.rect.y -= tile_size
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id in transparent_objects:
                    pass
                elif pygame.sprite.spritecollideany(self, objects_group).id not in free_cells:
                    self.rect.y -= tile_size
            self.side = 'd'

        elif args[pygame.K_RIGHT]:
            if self.side != 'r' and self.side != 'l':
                if side == 'u':
                    self.image = pygame.transform.rotate(self.image, self.angle - 90)
                else:
                    self.image = pygame.transform.rotate(self.image, self.angle + 90)
            elif self.side == 'l':
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect.x += tile_size
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.rect.x -= tile_size
            elif pygame.sprite.spritecollideany(self, enemies_group):
                pygame.mixer.Sound.play(collision_sound)
                self.rect.x -= tile_size
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id in transparent_objects:
                    pass
                elif pygame.sprite.spritecollideany(self, objects_group).id not in free_cells:
                    self.rect.x -= tile_size
            self.side = 'r'

        elif args[pygame.K_LEFT]:
            if self.side != 'l' and self.side != 'r':
                if side == 'u':
                    self.image = pygame.transform.rotate(self.image, self.angle + 90)
                else:
                    self.image = pygame.transform.rotate(self.image, self.angle - 90)
            elif self.side == 'r':
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect.x -= tile_size
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.rect.x += tile_size
            elif pygame.sprite.spritecollideany(self, enemies_group):
                pygame.mixer.Sound.play(collision_sound)
                self.rect.x += tile_size
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id in transparent_objects:
                    pass
                elif pygame.sprite.spritecollideany(self, objects_group).id not in free_cells:
                    self.rect.x += tile_size
            self.side = 'l'

        if level_map.tiledgidmap[level_map.get_tile_gid(self.rect.x // tile_size, self.rect.y // tile_size, 0)] in\
                water and level_map.get_tile_gid(self.rect.x // tile_size, self.rect.y // tile_size, 2) == 0:
            pygame.mixer.Sound.play(water_sound)
            self.death()
        if args[pygame.K_SPACE]:
            pygame.mixer.Sound.play(shot_sound)
            Bullet(self.rect.x, self.rect.y, self.side, 'player')

    def death(self):
        self.life -= 1
        if self.life > 0:
            self.characteristics_character()
        else:
            pass


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if y2 - y1 == height:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, height])
            self.rect = pygame.Rect(x1, y1, x2, y2)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([width, 1])
            self.rect = pygame.Rect(x1, y1, x2, y2)


pygame.init()
pygame.mixer.init()
size = width, height = 1250, 1000
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Танчики')
fps = 60
clock = pygame.time.Clock()
main_character_image = load_image('main_character.png')
image_death = load_image('animation_death_2.png')
bullet_group = pygame.sprite.Group()
bullet_image = load_image('bullet.png')
enemies_images = ['enemy_1.png', 'enemy_2.png', 'enemy_3.png']
kill_enemy = []
amount_enemies = 0
death_enemies = 0
death_sound = pygame.mixer.Sound('sound/death.mp3')
collision_sound = pygame.mixer.Sound('sound/collision.mp3')
water_sound = pygame.mixer.Sound('sound/water.mp3')
shot_sound = pygame.mixer.Sound('sound/shot.mp3')
movement_sound = pygame.mixer.Sound('sound/movement.mp3')
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
counter_of_loudness = 0
free_cells = [130, 131, 132, 144, 305, 306, 307]
free_cells_spawn = [130, 131, 132, 144]
transparent_objects = [156, 158, 160]
water = [1, 2, 3, 13, 14, 15, 25, 26, 27, 37, 38, 39, 49, 50, 51]
additional_objects = pygame.sprite.Group()
player_group = pygame.sprite.Group()
if start_screen():
    try:
        pygame.mixer.music.set_volume(0.5)
    except NameError:
        pygame.mixer.music.set_volume(1)
    player, level_x, level_y = generate_level(load_level('map_1.tmx'), 0, 11)
    Border(0, 0, width, -1)
    Border(0, height, width, height + 1)
    Border(0, 0, -1, height)
    Border(width, 0, width + 1, height)
    MYEVENTTYPE = pygame.USEREVENT + 200
    pygame.time.set_timer(MYEVENTTYPE, 1000)
    for _ in range(randint(2, 4)):
        Enemy(level_x, level_y)
        amount_enemies += 1
    running = True
    while running:
        for event in pygame.event.get():
            if kill_enemy:
                pygame.mixer.init()
                pygame.mixer.music.load('sound/death.mp3')
                pygame.mixer.music.play()
                kill_enemy.pop(0).death()
                death_enemies += 1
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                player_group.update(pygame.key.get_pressed())
            if event.type == MYEVENTTYPE:
                for sprite in enemies_group:
                    sprite.update(player.rect.x, player.rect.y)
        if kill_enemy:
            kill_enemy[0].image = load_image('empty_image.png')
        bullet_group.update()
        tiles_group.draw(screen)
        additional_objects.draw(screen)
        player_group.draw(screen)
        enemies_group.draw(screen)
        bullet_group.draw(screen)
        objects_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()