import pygame
import pytmx
import os


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
                    screen.blit(pygame.sprite.spritecollideany(self, objects_group).image, (self.rect.x, self.rect.y))
                elif pygame.sprite.spritecollideany(self, objects_group).id not in obstacles:
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
                    screen.blit(pygame.sprite.spritecollideany(self, objects_group).image, (self.rect.x, self.rect.y))
                elif pygame.sprite.spritecollideany(self, objects_group).id not in obstacles:
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
                    screen.blit(pygame.sprite.spritecollideany(self, objects_group).image, (self.rect.x, self.rect.y))
                elif pygame.sprite.spritecollideany(self, objects_group).id not in obstacles:
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
                    screen.blit(pygame.sprite.spritecollideany(self, objects_group).image, (self.rect.x, self.rect.y))
                elif pygame.sprite.spritecollideany(self, objects_group).id not in obstacles:
                    self.rect.x += tile_size
            self.side = 'l'


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
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
obstacles = [130, 131, 132, 144, 305]
transparent_objects = [156, 158, 160]
additional_objects = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player, level_x, level_y = generate_level(load_level('map_1.tmx'), 0, 11)
Border(0, 0, width, -1)
Border(0, height, width, height + 1)
Border(0, 0, -1, height)
Border(width, 0, width + 1, height)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player_group.update(pygame.key.get_pressed())
    tiles_group.draw(screen)
    additional_objects.draw(screen)
    player_group.draw(screen)
    objects_group.draw(screen)
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()