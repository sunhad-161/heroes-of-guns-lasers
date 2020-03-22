import pygame
import os


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


class Button:
    def __init__(self, x, y, width, height, text=''):
        self.x = x
        self.y = y
        self. width = width
        self.height = height

        self.text = text

    def render(self, screen):
        pygame.draw.rect(screen,  (170, 170, 170), (self.x, self.y, self.width, self.height), 0)
        font = pygame.font.Font(None, 50)
        text = font.render(self.text, 1, (140, 90, 90))
        text_w = text.get_width() + self.x
        text_h = text.get_height() + self.y
        screen.blit(text, (text_w, text_h))

    def set_text(self, new_text):
        self.text = new_text

    def check(self, x, y):
        if (x > self.x and y > self.y) and (x < self.x + self.width and y < self.y + self.height):
            return True
        else:
            return False


class HealthBar:
    def __init__(self, subject):
        self.width = subject.rect.width
        self.height = 4
        self.subject = subject

    def render(self, screen):
        x, y = self.subject.rect.x, self.subject.rect.y - self.height
        hp = self.subject.current_health / self.subject.max_health
        pygame.draw.rect(screen, (0, 255, 0), (x, y, self.width * hp, self.height), 0)
        pygame.draw.rect(screen, (255, 0, 0), (x + self.width * hp, y,
                                               self.width * (1 - hp), self.height), 0)


class Ammunition:
    def __init__(self):
        self.ammo = 6
        self.full = load_image('full_bullet.png', -1)
        self.empty = load_image('empty_bullet.png', -1)

    def reload(self):
        self.ammo = 6

    def lose(self):
        self.ammo -= 1

    def render(self, screen):
        for i in range(1, 7):
            if i <= self.ammo:
                screen.blit(self.full, (37 * i, 576))
            else:
                screen.blit(self.empty, (37 * i, 576))


def end(screen, win):
    if win:
        text = 'You win!'
    else:
        text = 'You lose('
    font = pygame.font.Font(None, 50)
    text = font.render(text, 1, (140, 90, 90))
    text_w = text.get_width() + 300
    text_h = text.get_height() + 430
    screen.blit(text, (text_w, text_h))
