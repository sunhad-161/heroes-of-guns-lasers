import pygame
import props
import windows
import music


def draw():
    props.walls.draw(screen)
    props.all_props.draw(screen)
    props.en_props.draw(screen)
    props.player.draw(screen)
    props.player.update(event)
    props.all_props.update(event)
    props.en_props.update(event)


pygame.init()
pygame.mixer.init()

size = width, height = 1280, 704
music.main_menu()

screen = pygame.display.set_mode(size)
pygame.mixer.music.play(-1)

running = True
clock = pygame.time.Clock()
pl = props.Player(width // 2, height // 2)
start_b = windows.Button(320, 250, 280, 110)
start_b.set_text('Start')
window = 'main'
pygame.mouse.set_visible(True)

# основной цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and window == 'main':
            if start_b.check(*event.pos):
                window = 'game'
                music.game()
                pygame.mouse.set_visible(False)
                pygame.mixer.music.play(-1)
                props.now_room = props.load_level()
                props.generate_level(props.now_room)
                cur = props.Cursor(*event.pos)
                print(props.en_props)
        elif window == 'game':
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                pl.update(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pl.rect.x + pl.rect.width // 2, pl.rect.y + pl.rect.height // 2
                props.Bullet(x, y, *event.pos)
    screen.fill((25, 25, 25))
    if window == 'game':
        draw()
        pl.move()
    elif window == 'main':
        start_b.render(screen)
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
