import pygame
def draw():
    pygame.draw.line(screen, pygame.Color("white"), (0, 0), (width, height), 3)
    pygame.draw.line(screen, pygame.Color("white"), (width, 0), (0, height), 3)

pygame.init()
pygame.mixer.init()

size = width, height = 600, 300

main_menu_music = pygame.mixer.music.load('HateBit-Pixelizer.mp3')
screen = pygame.display.set_mode(size)
draw()
pygame.mixer.music.play(-1)
while pygame.event.wait().type != pygame.QUIT:
    pygame.display.flip()
pygame.quit()
