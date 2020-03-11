import pygame
import props
import windows
import music


def draw(up):
    props.walls.draw(screen)
    props.all_props.draw(screen)
    props.en_props.draw(screen)
    props.player.draw(screen)
    if up:
        props.player.update(event)
        props.all_props.update(event)
        props.en_props.update(event)
        pl.move()
    for en in props.en_props.spritedict:
        en.hunt(pl.rect.x, pl.rect.y)


def konami():
    global window, buttons
    buttons = list()
    buttons.append(windows.Button(460, 100, 280, 110))
    buttons.append(windows.Button(460, 240, 280, 110))
    buttons.append(windows.Button(460, 380, 280, 110))
    window = 'konami'
    pygame.mouse.set_visible(True)


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
buttons = list()
buttons.append(windows.Button(250, 250, 280, 110, 'Start'))
buttons.append(windows.Button(250, 400, 280, 110, 'Exit'))
window = 'main'
pygame.mouse.set_visible(True)

# основной цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and window == 'main':
            if buttons[0].check(*event.pos):
                window = 'game'
                music.game()
                pygame.mouse.set_visible(False)
                pygame.mixer.music.play(-1)
                x, y = props.current_room
                props.current_floor[x][y].load()
                cur = props.Cursor(*event.pos)
            elif buttons[1].check(*event.pos):
                running = False
        elif window == 'game':
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                pl.update(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pl.rect.x + pl.rect.width // 2, pl.rect.y + pl.rect.height // 2
                props.Bullet(props.current_floor[props.current_room[0]][props.current_room[1]], x, y, *event.pos)
    screen.fill((25, 25, 25))
    if window == 'game':
        if props.defeated_bosses != 3:
            draw(True)
        else:
            draw(False)
            windows.end(screen)
        if pl.konami == [273, 273, 274, 274, 276, 275, 276, 275, 98, 97]:
            print('pass')
            konami()
    elif window == 'main' or window == 'konami':
        for i in buttons:
            i.render(screen)
    clock.tick(60)
    pygame.display.flip()
pygame.quit()
