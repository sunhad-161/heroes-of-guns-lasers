import pygame

class Button():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self. width = width
        self.height = height

        self.text = ''

    def render(self, screen):
        pygame.draw.rect(screen,  (170, 170, 170), (self.x, self.y, self.width, self.height), 0)
        font = pygame.font.Font(None, 50)
        text = font.render(self.text, 1, (140, 90, 90))
        text_x = self.width // 2 - text.get_width() // 2
        text_y = self.height // 2 - text.get_height() // 2
        text_w = text.get_width() + self.x
        text_h = text.get_height() + self.y
        screen.blit(text, (text_w, text_h))

    def set_text(self, new_text):
        self.text = new_text

    def check(self, x, y):
        if (x > self.x and x < self.x + self.width) and (y > self.y and y < self.y + self.height):
            return True
        else:
            return False
