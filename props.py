import pygame


class Prop():
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
