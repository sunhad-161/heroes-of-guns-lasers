import pygame
import props
import windows
import music
from random import choice


pygame.init()
pygame.mixer.init()

size = width, height = 1280, 704
music.main_menu()

screen = pygame.display.set_mode(size)
pygame.mixer.music.play(-1)

running = True
clock = pygame.time.Clock()
pl = props.Player(width // 2, height // 2, (45, 200, 200))
cur = props.Cursor(0, 0, (0, 255, 0))
bullets = list()
walls = list()
start_b = windows.Button(320, 250, 280, 110)
start_b.set_text('Start')
window = 'main'

count = 5
enemy = list()
for i in range(count):
    x, y = choice(range(width)), choice(range(height))
    enemy.append(props.Enemy(x, y, (255, 0, 0), 5))
for i in range(width // 32):
    for j in range(height // 32):
        if (i > 0 and j > 0) and (i < width / 32 - 1 and j < height / 32 - 1):
            continue
        else:
            walls.append(props.Wall(i * 32, j * 32, (102, 51, 51)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pl.vector(0, -9)
            if event.key == pygame.K_LEFT:
                pl.vector(-9, 0)
            if event.key == pygame.K_DOWN:
                pl.vector(0, 9)
            if event.key == pygame.K_RIGHT:
                pl.vector(9, 0)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                pl.vector(0, 9)
            if event.key == pygame.K_LEFT:
                pl.vector(9, 0)
            if event.key == pygame.K_DOWN:
                pl.vector(0, -9)
            if event.key == pygame.K_RIGHT:
                pl.vector(-9, 0)
        if event.type == pygame.MOUSEMOTION:
            cur.move(*event.pos, screen)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if window == 'game':
                center = (pl.x + pl.width // 2, pl.y + pl.height // 2)
                bullets.append(props.Bullet(*center, (230, 200, 0)))
                b_vector = props.count_vectors(pl.x + pl.width // 2, pl.y + pl.height // 2,
                                               cur.x + cur.width // 2, cur.y + cur.height // 2,
                                               12, bullets[-1])
                if b_vector:
                    bullets[-1].vector(*b_vector)
            elif window == 'main':
                if start_b.check(*event.pos):
                    window = 'game'
                    music.game()
                    pygame.mixer.music.play(-1)
    screen.fill((25, 25, 25))
    if window == 'game':
        pygame.mouse.set_visible(False)
        pl.move(screen)
        for bul in bullets:
            bul.check(screen, bullets, enemy)
        for en in enemy:
            if en.check(enemy):
                en.render(screen)
        cur.render(screen)
        for w in walls:
            w.render(screen)
    elif window == 'main':
        pygame.mouse.set_visible(True)
        start_b.render(screen)
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
