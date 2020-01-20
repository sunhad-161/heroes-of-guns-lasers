import pygame
from props import Prop


class Player(Prop):
    def __init__(self, x, y, size, image):
        super().__init__(x, y, size, size, image)


class Cursor(Prop):
    def __init__(self, x, y, size, image):
        super().__init__(x, y, size, size, image)

    def move(self, x, y):
        self.x = x
        self.y = y
        super().render(screen)


class Bullet(Prop):
    def __init__(self, x, y, size, image):
        super().__init__(x, y, size, size, image)

    def check(self, screen):
        if (self.x < 0 or self.x >= 1280) or (self.y < 0 or self.y >= 720):
            bullets.insert(bullets.index(self))
        self.move(screen)


pygame.init()
pygame.mixer.init()

size = width, height = 1280, 720

main_menu_music = pygame.mixer.music.load('HateBit-Pixelizer.mp3')
screen = pygame.display.set_mode(size)
pygame.mixer.music.play(-1)

running = True
clock = pygame.time.Clock()
player = Player(width // 2, height // 2, 32, (255, 0, 0))
cur = Cursor(0, 0, 4, (0, 255, 0))
bullets = list()
pygame.mouse.set_visible(False)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.vector(0, -9)
            if event.key == pygame.K_LEFT:
                player.vector(-9, 0)
            if event.key == pygame.K_DOWN:
                player.vector(0, 9)
            if event.key == pygame.K_RIGHT:
                player.vector(9, 0)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.vector(0, 9)
            if event.key == pygame.K_LEFT:
                player.vector(9, 0)
            if event.key == pygame.K_DOWN:
                player.vector(0, -9)
            if event.key == pygame.K_RIGHT:
                player.vector(-9, 0)
        if event.type == pygame.MOUSEMOTION:
            cur.move(*event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            center = (player.x + player.width // 2, player.y + player.height // 2)
            bullets.append(Bullet(*center, 4, (200, 200, 0)))
            bullets[-1].vector(16, 16)
    screen.fill((0, 0, 0))
    player.move(screen)
    cur.render(screen)
    for bul in bullets:
        bul.check(screen)
    clock.tick(80)
    pygame.display.flip()
pygame.quit()
