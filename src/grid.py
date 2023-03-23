"""
Generate a cool pygame window so see NxN grid.
Can rotate with space and switch solutions with left arrow.

Gregoire Layet | 2023 | microProjet Polytech Nantes PEIP
"""

import pygame
from pygame.locals import *

import time

from rng_grid import get_one_perfect_grid as get_points

grid_size = 9
grid_color = (20, 20, 20)  # rgb

start_time = time.time()

results = get_points(grid_size)
result_indice = 0

end_time = time.time()
result_time = end_time-start_time

height = 600
width = 800

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode([width, height], pygame.RESIZABLE)

font = pygame.font.SysFont("Arial", 20)


def draw():
    screen.fill((255, 255, 255))

    grid_space = min(height, width)/(grid_size+1)

    padding_height = grid_space
    padding_width = grid_space

    if height > width:
        padding_height = height/2 - grid_space*(grid_size-1)/2
    else:
        padding_width = width/2 - grid_space*(grid_size-1)/2

    screen.fill((255, 255, 255))

    # cols
    for i in range(grid_size):
        pygame.draw.line(screen, grid_color, (i*grid_space + padding_width,
                         padding_height), (i*grid_space + padding_width, height - padding_height))

    # rows
    for i in range(grid_size):
        pygame.draw.line(screen, grid_color, (padding_width, i*grid_space +
                         padding_height), (width - padding_width, i*grid_space + padding_height))

    for point in results[result_indice].points:
        x, y = point
        pygame.draw.circle(screen, (255, 0, 0),
                           (x*grid_space + padding_width + 1, y*grid_space + padding_height + 1), 5)

    txt = f"Temps de calcul : {result_time:.3f}s"
    width_text, height_text = font.size(txt)
    txt_render = font.render(txt, True, grid_color)
    screen.blit(txt_render, (width/2 - width_text/2,
                height - padding_height/2 - height_text/2))

    txt_render = font.render(str(result_indice), True, grid_color)
    screen.blit(txt_render, (10,
                10))

    pygame.display.flip()


draw()

input_repeat_time = 0

clock = pygame.time.Clock()
running = True
while running:
    delta_time = clock.tick(60)
    for event in pygame.event.get():
        if event.type == VIDEORESIZE:
            height = event.h
            width = event.w
            screen = pygame.display.set_mode(
                (event.w, event.h), pygame.RESIZABLE)
            draw()
        if event.type == pygame.QUIT:
            running = False

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE] and input_repeat_time < 0:
        input_repeat_time = 0.2*1000
        results[result_indice].points = rotating_points(
            grid_size, results[result_indice].points)
        draw()

    if pressed[pygame.K_RIGHT] and input_repeat_time < 0:
        input_repeat_time = 0.2*1000
        result_indice += 1
        if result_indice == len(results):
            result_indice = 0

        draw()

    if pressed[pygame.K_LEFT] and input_repeat_time < 0:
        input_repeat_time = 0.2*1000
        result_indice -= 1
        if result_indice == -1:
            result_indice = len(results)-1

        draw()

    input_repeat_time -= delta_time

pygame.quit()
