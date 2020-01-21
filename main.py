import pygame
import props


pygame.init()
pygame.mixer.init()

size = width, height = 1280, 720

main_menu_music = pygame.mixer.music.load('HateBit-Pixelizer.mp3')
screen = pygame.display.set_mode(size)
pygame.mixer.music.play(-1)

running = True
clock = pygame.time.Clock()
pl = props.Player(width // 2, height // 2, (255, 0, 0))
cur = props.Cursor(0, 0, (0, 255, 0))
bullets = list()
pygame.mouse.set_visible(False)
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
            center = (pl.x + pl.width // 2, pl.y + pl.height // 2)
            bullets.append(props.Bullet(*center, (200, 200, 0)))
            b_vector = props.count_vectors(pl.x + pl.width // 2, pl.y + pl.height // 2,
                                           cur.x + cur.width // 2, cur.y + cur.height // 2,
                                           12, bullets[-1])
            if b_vector:
                bullets[-1].vector(*b_vector)
    screen.fill((0, 0, 0))
    pl.move(screen)
    cur.render(screen)
    for bul in bullets:
        bul.check(screen, bullets)
    clock.tick(80)
    pygame.display.flip()
pygame.quit()
