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
            print(2)
            continue
        cell = level_map.get_tile_gid(pos_x, pos_y, 1)
        if cell == 0:
            continue
        if level_map.tiledgidmap[cell] in free_cells:
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
                return self.kill()
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id not in transparent_objects and\
                        pygame.sprite.spritecollideany(self, objects_group).id not in free_cells:
                    return self.kill()
        else:
            self.rect.x += self.speed
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                return self.kill()
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id not in transparent_objects and\
                        pygame.sprite.spritecollideany(self, objects_group).id not in free_cells:
                    return self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, main_character_x, main_character_y):
        super().__init__(enemies_group)
        self.pos_x, self.pos_y = search_place(main_character_x, main_character_y)
        self.image = load_image(choice(enemies_images))
        self.rect = self.image.get_rect().move(
            tile_size * self.pos_x, tile_size * self.pos_y)


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = main_character_image
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y)
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
            elif pygame.sprite.spritecollideany(self, objects_group):
                if pygame.sprite.spritecollideany(self, objects_group).id in transparent_objects:
                    pass
                elif pygame.sprite.spritecollideany(self, objects_group).id not in free_cells:
                    self.rect.x += tile_size
            self.side = 'l'
        elif args[pygame.K_SPACE]:
            Bullet(self.rect.x, self.rect.y, self.side)


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
bullet_group = pygame.sprite.Group()
bullet_image = load_image('bullet.png')
enemies_images = ['enemy_1.png', 'enemy_2.png', 'enemy_3.png']
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
free_cells = [130, 131, 132, 144]
transparent_objects = [156, 158, 160]
additional_objects = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player, level_x, level_y = generate_level(load_level('map_1.tmx'), 0, 11)
Border(0, 0, width, -1)
Border(0, height, width, height + 1)
Border(0, 0, -1, height)
Border(width, 0, width + 1, height)
for _ in range(randint(2, 4)):
    Enemy(level_x, level_y)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player_group.update(pygame.key.get_pressed())
    bullet_group.update()
    tiles_group.draw(screen)
    additional_objects.draw(screen)
    player_group.draw(screen)
    enemies_group.draw(screen)
    bullet_group.draw(screen)
    objects_group.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()