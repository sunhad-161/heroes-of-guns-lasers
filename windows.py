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


class WeaponBar:
    def __init__(self, weapon):
        self.info = weapon

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (0, 576, 64, 64), width=1)


class LevelBar:
    def __init__(self):
        self.xp = 0


class HealthBar:
    def __init__(self, x, y, size, subject=0):
        self.width = size


def end(screen):
    font = pygame.font.Font(None, 50)
    text = font.render('The end', 1, (140, 90, 90))
    text_w = text.get_width() + 300
    text_h = text.get_height() + 430
    screen.blit(text, (text_w, text_h))
