import pygame
import pytmx
import os
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
    def __init__(self, pos_x, pos_y, side):
        super().__init__(bullet_group)
        self.image = bullet_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.side = side
        self.speed = 0
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
            elif pygame.sprite.spritecollideany(self, enemies_group) and\
                    pygame.sprite.spritecollideany(self, enemies_group).state == 1:
                self.kill()
                pygame.display.flip()
                pygame.sprite.spritecollideany(self, enemies_group).death()
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id not in transparent_objects and\
                        pygame.sprite.spritecollideany(self, objects_group).id not in free_cells:
                    self.kill()
        else:
            self.rect.x += self.speed
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.kill()
            elif pygame.sprite.spritecollideany(self, enemies_group) and\
                    pygame.sprite.spritecollideany(self, enemies_group).state == 1:
                self.kill()
                pygame.sprite.spritecollideany(self, enemies_group).death()
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id not in transparent_objects and\
                        pygame.sprite.spritecollideany(self, objects_group).id not in free_cells:
                    self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, main_character_x, main_character_y):
        super().__init__(enemies_group)
        self.pos_x, self.pos_y = search_place(main_character_x, main_character_y)
        self.image = load_image(choice(enemies_images))
        self.rect = self.image.get_rect().move(
            tile_size * self.pos_x, tile_size * self.pos_y)
        self.state = 1

    def death(self):
        self.state = 0
        self.frames = []
        self.cut_sheet(image_death, 8, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(self.pos_x * tile_size, self.pos_y * tile_size)
        for _ in range(7):
            enemies_group.draw(screen)
            pygame.display.flip()
            clock.tick(30)
            self.update_death()

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update_death(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def update(self, fin_x, fin_y):
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
            self.rect.x, self.rect.y = x * tile_size, y * tile_size


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
                self.rect.x += tile_size
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id in transparent_objects:
                    pass
                elif pygame.sprite.spritecollideany(self, objects_group).id not in free_cells:
                    self.rect.x += tile_size
            self.side = 'l'
        if level_map.tiledgidmap[level_map.get_tile_gid(self.rect.x // tile_size, self.rect.y // tile_size, 0)] in\
                water and level_map.get_tile_gid(self.rect.x // tile_size, self.rect.y // tile_size, 2) == 0:
            self.death()
        if args[pygame.K_SPACE]:
            Bullet(self.rect.x, self.rect.y, self.side)
        print(self.rect.x, self.rect.y)

    def death(self):
        self.life -= 1
        if self.life != 0:
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
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
free_cells = [130, 131, 132, 144, 305]
free_cells_spawn = [130, 131, 132, 144]
transparent_objects = [156, 158, 160]
water = [1, 2, 3, 13, 14, 15, 25, 26, 27, 37, 38, 39, 49, 50, 51]
additional_objects = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player, level_x, level_y = generate_level(load_level('map_1.tmx'), 0, 11)
Border(0, 0, width, -1)
Border(0, height, width, height + 1)
Border(0, 0, -1, height)
Border(width, 0, width + 1, height)
MYEVENTTYPE = pygame.USEREVENT + 15
pygame.time.set_timer(MYEVENTTYPE, 300)
for _ in range(randint(2, 4)):
    Enemy(level_x, level_y)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player_group.update(pygame.key.get_pressed())
        if event.type == MYEVENTTYPE:
            for sprite in enemies_group:
                sprite.update(player.rect.x, player.rect.y)
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