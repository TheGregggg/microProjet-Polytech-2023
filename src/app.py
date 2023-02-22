import pygame
from pygame.locals import *

height = 1000
width = 800

pygame.init()
screen = pygame.display.set_mode([width, height], pygame.RESIZABLE)

grid_size = 1
grid_color = (20,20,20) #rgb

def get_points(grid_size):
    """
        main algorithme calculatings all the possibles point in the grid without more than 2 align
    """


def draw():
    screen.fill((255,255,255))

    grid_space = min(height,width)/(grid_size+2)

    padding_height = grid_space
    padding_width = grid_space

    if height > width:
        padding_height = height/2 - grid_space*grid_size/2
    else:
        padding_width = width/2 - grid_space*grid_size/2
        

    screen.fill((255, 255, 255))

    # cols
    for i in range(grid_size+1):
        pygame.draw.line(screen, grid_color, (i*grid_space + padding_width, padding_height), (i*grid_space + padding_width, height - padding_height))
    # rows
    for i in range(grid_size+1):
        pygame.draw.line(screen, grid_color, (padding_width, i*grid_space + padding_height), (width - padding_width, i*grid_space + padding_height))

    pygame.display.flip()


draw()

running = True
while running:
    for event in pygame.event.get():
        if event.type == VIDEORESIZE:
            height = event.h
            width = event.w
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            draw()
        if event.type == pygame.QUIT:
            running = False


pygame.quit()
