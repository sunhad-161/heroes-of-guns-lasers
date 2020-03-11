import pygame
from random import choice
from windows import load_image, end
import os

for current_dir, dirs, files in os.walk('data/rooms'):
    all_rooms = files

prop_width = prop_height = 64
player = pygame.sprite.Group()
walls = pygame.sprite.Group()
all_props = pygame.sprite.Group()
en_props = pygame.sprite.Group()


def generate_level(level, room, l, t, r, b):
    new_player, x, y = None, None, None
    for x in range(len(level)):
        for y in range(len(level[x])):
            if level[x][y] == 'W':
                room[x][y] = Wall(room.walls, y, x)
            elif level[x][y] == 'P':
                room[x][y] = Ground(room.all_props, y, x)
            elif level[x][y] == 'E':
                room[x][y] = Ground(room.all_props, y, x)
                room[x][y] = Enemy(room.en_props, y, x, 5)
            elif level[x][y] == 'D':
                if x == 0 and t:
                    room[x][y] = Door((room.all_props, room.walls), y, x)
                elif x == len(level) - 1 and b:
                    room[x][y] = Door((room.all_props, room.walls), y, x)
                elif y == 0 and l:
                    room[x][y] = Door((room.all_props, room.walls), y, x)
                elif y == len(level[x]) - 1 and r:
                    room[x][y] = Door((room.all_props, room.walls), y, x)
                else:
                    room[x][y] = Wall(room.walls, y, x)
            elif level[x][y] == 'B':
                room[x][y] = Boss(room.en_props, y, x, bosses[defeated_bosses] + '.png')
                room[x][y] = Ground(room.all_props, y, x)
    return x, y


def load_level(type_of_lvl):
    if type_of_lvl == 'rand':
        filename = choice(all_rooms)
        filename = "data/rooms/" + filename
    else:
        filename = "data/" + type_of_lvl + ".txt"
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    mapFile.close()
    return level_map


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
        self.konami = list()
        self.button = None
        self.flag = True

    def update(self, *args):
        if args:
            event = args[0]
            self.event = event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.y_vector = -self.speed
                elif event.key == pygame.K_LEFT:
                    self.x_vector = -self.speed
                elif event.key == pygame.K_DOWN:
                    self.y_vector = self.speed
                elif event.key == pygame.K_RIGHT:
                    self.x_vector = self.speed
                self.button = event.key
                self.flag = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.y_vector = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.x_vector = 0
                if self.flag:
                    self.konami.append(event.key)
                    self.flag = False
                    print(self.konami)
                if len(self.konami) > 10:
                    self.konami.remove(self.konami[0])
        if pygame.sprite.spritecollideany(self, walls):
            if self.rect.x % prop_width <= self.speed and self.button == 275:
                self.rect.x -= self.speed
            elif self.rect.x % prop_width >= self.speed and self.button == 276:
                self.rect.x += self.speed
            elif self.rect.y % prop_height <= self.speed and self.button == 274:
                self.rect.y -= self.speed
            elif self.rect.y % prop_height >= self.speed and self.button == 273:
                self.rect.y += self.speed
        if self.rect.x + prop_width < 0:
            current_room[1] -= 1
            x, y = current_room
            current_floor[x][y].load()
            self.rect.x = 1130
        elif self.rect.x + prop_width > 1280:
            current_room[1] += 1
            x, y = current_room
            current_floor[x][y].load()
            self.rect.x = 70
        elif self.rect.y + prop_height < 0:
            current_room[0] -= 1
            x, y = current_room
            current_floor[x][y].load()
            self.rect.y = 500
        elif self.rect.y + prop_height > 640:
            current_room[0] += 1
            x, y = current_room
            current_floor[x][y].load()
            self.rect.y = 70


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
    def __init__(self, room, x, y, c_x, c_y):
        image = load_image('bullet.png', -1)
        super().__init__(player, x, y, image)
        vector = count_vectors(x, y, c_x, c_y, 12)
        if vector:
            self.x_vector, self.y_vector = vector
        else:
            self.delete(player)

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, walls):
            self.delete(player)
        for enemy in en_props.spritedict:
            if ((enemy.rect.x <= self.rect.x <= enemy.rect.x + enemy.rect.width) and
                    (enemy.rect.y <= self.rect.y <= enemy.rect.y + enemy.rect.height)):
                enemy.hp -= 1
                self.delete(player)
        self.move()


class Enemy(Prop):
    def __init__(self, group, x, y, health, image_name='ghost.png'):
        image = load_image(image_name, -1)
        super().__init__(group, x * prop_width, y * prop_height, image)
        self.health = health
        self.hp = health
        self.group = group

    def update(self, *args):
        if self.hp <= 0:
            self.delete(self.group)

    def hunt(self, x, y):
        vector = count_vectors(self.rect.x, self.rect.y, x, y, 2)
        if vector:
            self.x_vector, self.y_vector = vector
        self.move()


class Boss(Enemy):
    def __init__(self, group, x, y, image):
        super().__init__(group, x, y, 20, image)

    def update(self, *args):
        if self.hp <= 0:
            global current_room, current_floor, defeated_bosses
            self.delete(self.group)
            defeated_bosses += 1
            current_floor = list()
            init()
            current_room = [5, 1]
            current_floor[5][1].load()


class Wall(Prop):
    def __init__(self, group, x, y):
        image = load_image('wall.png')
        super().__init__(group, x * prop_width, y * prop_height, image)


class Ground(Prop):
    def __init__(self, group, x, y):
        image = load_image('floor.png')
        super().__init__(group, x * prop_width, y * prop_height, image)


class Door(Prop):
    def __init__(self, group, x, y, locked=True):
        image = load_image('wall.png')
        super().__init__(group, x * prop_width, y * prop_height, image)
        self.locked = locked

    def update(self, *args):
        if not bool(en_props) and self.locked:
            self.locked = False
            self.image = load_image('floor.png')
            self.delete(walls)


class Room(list):
    def __init__(self, lvl='rand', l=True, t=True, r=True, b=True):
        super().__init__()

        for a in range(10):
            self.append(list())
            for _ in range(20):
                self[a].append(None)

        self.all_props = pygame.sprite.Group()
        self.en_props = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.lvl = lvl

        generate_level(load_level(lvl), self, l, t, r, b)

    def load(self):
        global walls, all_props, en_props
        walls = self.walls
        all_props = self.all_props
        en_props = self.en_props

    def __str__(self):
        return self.lvl


def init():
    for i in range(6):
        current_floor.append(list())
        for j in range(4):
            if i != 0 and i != 5:
                if (i, j) == (1, 0):
                    current_floor[i].append(Room(l=False, t=False))
                elif (i, j) == (1, 3):
                    current_floor[i].append(Room(t=False, r=False))
                elif (i, j) == (4, 0):
                    current_floor[i].append(Room(l=False, b=False))
                elif (i, j) == (4, 3):
                    current_floor[i].append(Room(r=False, b=False))
                elif (i, j) == (1, 1):
                    current_floor[i].append(Room(t=False))
                elif (i, j) == (4, 2):
                    current_floor[i].append(Room(b=False))
                elif j == 0:
                    current_floor[i].append(Room(l=False))
                elif j == 3:
                    current_floor[i].append(Room(r=False))
                else:
                    current_floor[i].append(Room())
            elif (i, j) == (0, 2):
                current_floor[i].append(Room(lvl='finish'))
            elif (i, j) == (5, 1):
                current_floor[i].append(Room(lvl='start'))
            else:
                current_floor[i].append(None)


current_floor = list()
current_room = [5, 1]
defeated_bosses = 0
bosses = ['ghost_boss', 'red_wizard', 'robot', None]