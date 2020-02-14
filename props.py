import pygame
from random import choice
import os

for currentdir, dirs, files in os.walk('data/rooms'):
    all_rooms = files
all_props = pygame.sprite.Group()
en_props = pygame.sprite.Group()
player = pygame.sprite.Group()
walls = pygame.sprite.Group()
prop_width = prop_height = 64
now_room = None


def load_level():
    filename = choice(all_rooms)
    filename = "data/rooms/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'W':
                Wall(x, y)
            elif level[y][x] == 'P':
                Floor(x, y)
            elif level[y][x] == 'E':
                Floor(x, y)
                Enemy(x, y, 5)
    # вернем размер поля в клетках
    return x, y


# для снарядов
def count_vectors(x_1, y_1, x_2, y_2, v):
    v_x = x_2 - x_1
    v_y = y_2 - y_1
    distance = (v_x**2 + v_y**2)**0.5
    if distance != 0:
        k = v / distance
        return k * v_x, k * v_y
    else:
        return False


def load_image(name, color_key=None):
    fullname = os.path.join('data', 'sprite', name)
    image = pygame.image.load(fullname).convert()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


# основной класс
class Prop(pygame.sprite.Sprite):
    def __init__(self, group, x, y, image):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x_vector = 0
        self.y_vector = 0

    def vector(self, x, y):
        self.x_vector += x
        self.y_vector += y
        print(self.x_vector, self.y_vector)

    def move(self):
        self.rect.x += self.x_vector
        self.rect.y += self.y_vector

    def delete(self, group):
        group.remove(self)


class Player(Prop):
    def __init__(self, x, y):
        image = load_image('knight.png', -1)
        super().__init__(player, x, y, image)
        self.event = 0
        self.speed = 6

    def update(self, *args):
        if args:
            event = args[0]
            self.event = event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.y_vector = -self.speed
                if event.key == pygame.K_LEFT:
                    self.x_vector = -self.speed
                if event.key == pygame.K_DOWN:
                    self.y_vector = self.speed
                if event.key == pygame.K_RIGHT:
                    self.x_vector = self.speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.y_vector = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.x_vector = 0
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.x -= self.x_vector * 1.5
            self.rect.y -= self.y_vector * 1.5


class Cursor(Prop):
    def __init__(self, x, y):
        image = load_image('aim.png', -1)
        super().__init__(player, x, y, image)

    def update(self, *args):
        event = args[0]
        if args and event.type == pygame.MOUSEMOTION:
            self.rect.x, self.rect.y = event.pos
            self.rect.x -= self.rect.width // 2
            self.rect.y -= self.rect.height // 2


class Bullet(Prop):
    def __init__(self, x, y, c_x, c_y):
        image = load_image('bullet.png', -1)
        super().__init__(all_props, x, y, image)
        vector = count_vectors(x, y, c_x, c_y, 12)
        if vector:
            self.x_vector, self.y_vector = vector
        else:
            self.delete(all_props)

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, walls):
            self.delete(all_props)
        for enemy in en_props.spritedict:
            if ((enemy.rect.x <= self.rect.x <= enemy.rect.x + prop_width) and
                    (enemy.rect.y <= self.rect.y <= enemy.rect.y + prop_height)):
                enemy.hp -= 1
                self.delete(all_props)
        self.move()


class Enemy(Prop):
    def __init__(self, x, y, health):
        image = load_image('enemy.png', -1)
        super().__init__(en_props, x * prop_width, y * prop_height, image)
        self.health = health
        self.hp = health

    def update(self, *args):
        if self.hp <= 0:
            self.delete(en_props)
            return False
        else:
            return True


class Wall(Prop):
    def __init__(self, x, y):
        image = load_image('wall.png')
        super().__init__(walls, x * prop_width, y * prop_height, image)


class Floor(Prop):
    def __init__(self, x, y):
        image = load_image('floor.png')
        super().__init__(all_props, x * prop_width, y * prop_height, image)
