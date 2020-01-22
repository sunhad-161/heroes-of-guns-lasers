import pygame


class Prop:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

        self.x_vector = 0
        self.y_vector = 0

    def render(self, screen):
        pygame.draw.rect(screen, self.image, (self.x, self.y, self.width, self.height), 0)

    def vector(self, x, y):
        self.x_vector += x
        self.y_vector += y

    def move(self, screen):
        self.x += self.x_vector
        self.y += self.y_vector
        self.render(screen)

    def delete(self, arrey):
        arrey.remove(self)

class Player(Prop):
    def __init__(self, x, y,image):
        super().__init__(x, y, 32, 32, image)


class Cursor(Prop):
    def __init__(self, x, y, image):
        super().__init__(x, y, 4, 4, image)

    def move(self, x, y, screen):
        self.x = x
        self.y = y
        super().render(screen)


class Bullet(Prop):
    def __init__(self, x, y, image):
        super().__init__(x, y, 4, 4, image)

    def check(self, screen, arrey_1, arrey_2):
        if (self.x < 0 or self.x >= 1280) or (self.y < 0 or self.y >= 720):
            self.delete(arrey_1)
        else:
            for en in arrey_2:
                if ((self.x + self.width > en.x and self.x < en.x + en.width) and
                    (self.y + self.height > en.y and self.y < en.x + en.height)):
                    en.hp -= 1
                    self.delete(arrey_1)
        self.move(screen)

class Enemy(Prop):
    def __init__(self, x, y, image, health):
        super().__init__(x, y, 32, 32, image)
        self.health = health
        self.hp = health

    def check(self, arrey):
        if self.hp <= 0:
            self.delete(arrey)
            return False
        else:
            return True


def count_vectors(x_1, y_1, x_2, y_2, v, object):
    v_x = x_2 - x_1
    v_y = y_2 - y_1
    l = (v_x**2 + v_y**2)**0.5
    if v != 0:
        k = v / l
        return k * v_x, k * v_y
    else:
        object.delete()
        return False