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
    pl.move()
    props.all_props.update(event)
    props.en_props.update(event)
    for en in props.en_props.spritedict:
        en.hunt(pl.rect.x, pl.rect.y)


pygame.init()
pygame.mixer.init()


size = width, height = 1280, 640
music.main_menu()

screen = pygame.display.set_mode(size)
props.init()
pygame.mixer.music.play(-1)

running = True
clock = pygame.time.Clock()
pl = props.Player(width // 2, height // 2)
start_b = windows.Button(250, 250, 280, 110)
start_b.set_text('Start')
exit_b = windows.Button(250, 400, 280, 110)
exit_b.set_text('Exit')
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
                x, y = props.current_room
                props.current_floor[x][y].load()
                cur = props.Cursor(*event.pos)
            elif exit_b.check(*event.pos):
                running = False
        elif window == 'game':
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                pl.update(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pl.rect.x + pl.rect.width // 2, pl.rect.y + pl.rect.height // 2
                props.Bullet(props.current_floor[props.current_room[0]][props.current_room[1]], x, y, *event.pos)
    screen.fill((25, 25, 25))
    if window == 'game':
        draw()
        if pl.konami == [273, 273, 274, 274, 276, 275, 276, 275, 98, 97]:
            windows.konami()
    elif window == 'main':
        start_b.render(screen)
        exit_b.render(screen)
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
