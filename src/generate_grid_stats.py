"""
Generate solutions for a NxN grid.
Export all results to files : images of grid, triangles histogrames, smallest triangle possible and list of points.

Gregoire Layet | 2023 | microProjet Polytech Nantes PEIP
"""

import pygame
from pygame.locals import *

import time
import os
import csv

from get_points_simplfied import *
import rng_grid
import calc_triangles

grid_color = (20, 20, 20)  # rgb
grid_px_size_rel = 0.03
dot_size_rel = 0.16

height = 3000
width = 3000

pygame.init()

screen = pygame.surface.Surface((width, height))


def draw(result):
    grid_size = result.size
    screen.fill((255, 255, 255))

    grid_space = min(height, width)/(grid_size+1)

    padding_height = grid_space
    padding_width = grid_space

    if height > width:
        padding_height = height/2 - grid_space*(grid_size-1)/2
    else:
        padding_width = width/2 - grid_space*(grid_size-1)/2

    dot_size = int(grid_space*dot_size_rel)
    grid_px_size = int(grid_space*grid_px_size_rel)

    screen.fill((255, 255, 255))

    # cols
    for i in range(grid_size):
        pygame.draw.line(screen, grid_color, (i*grid_space + padding_width,
                         padding_height), (i*grid_space + padding_width, height - padding_height), grid_px_size)

    # rows
    for i in range(grid_size):
        pygame.draw.line(screen, grid_color, (padding_width, i*grid_space +
                         padding_height), (width - padding_width, i*grid_space + padding_height), grid_px_size)

    for point in result.points:
        x, y = point
        pygame.draw.circle(screen, (255, 0, 0),
                           (x*grid_space + padding_width + 1, y*grid_space + padding_height + 1), dot_size)


def mkdir_if_not_exist(route: str):
    if not os.path.exists(route):
        os.mkdir(route)


def generate_results(result, route: str):
    mkdir_if_not_exist(route)

    # generate image as png
    draw(result)
    pygame.image.save(screen, route + "/grid.png")

    # generate points csv
    with open(route + '/points.csv', mode='w') as points_file:
        writer = csv.writer(
            points_file, delimiter=',', quotechar='"')

        writer.writerow(['x', 'y'])
        for points in result.points:
            writer.writerow(points)

    triangles_info = calc_triangles.calc_triangle(result.points)

    average_surface = 0
    total_surfaces = 0
    for surface, triangle in triangles_info['surface'].items:
        total_surfaces += triangle
        average_surface += surface*triangle

    average_surface = average_surface/total_surfaces
    average_surface_round = f"{average_surface:.5f}"

    with open(route+"/average_surface.txt", 'w') as time_file:
        time_file.write(f"{average_surface_round}s")

    # generate triangles csv
    with open(route + '/triangles.csv', mode='w') as triangle_file:
        writer = csv.writer(
            triangle_file, delimiter=',', quotechar='"')

        writer.writerow(['x_a', 'y_a', 'x_b', 'y_b', 'x_c', 'y_c'])
        for triangle in triangles_info['triangles']:
            a = [triangle[0][0], triangle[0][1]]
            b = [triangle[1][0], triangle[1][1]]
            c = [triangle[2][0], triangle[2][1]]
            writer.writerow(a+b+c)

    # generate triangles histogram csv
    with open(route + '/histogram.csv', mode='w') as histogram_file:
        writer = csv.writer(
            histogram_file, delimiter=',', quotechar='"')

        writer.writerow(['surface', 'number of triangle'])
        for surface, nb in triangles_info['surfaces'].items():
            writer.writerow([surface, nb])


def generate_grid(grid_size: int, func_to_use):
    start_time = time.time()

    results = func_to_use(grid_size)

    end_time = time.time()

    result_time = end_time-start_time
    result_time_round = f"{result_time:.3f}"

    path_result_folder = f"./results/grid {grid_size}x{grid_size}"

    if len(results) == 1:
        generate_results(results[0], path_result_folder)

    else:
        mkdir_if_not_exist(path_result_folder)
        for i in range(len(results)):
            generate_results(results[i], path_result_folder+f"/solution {i+1}")

    with open(path_result_folder+"/time.txt", 'w') as time_file:
        time_file.write(f"{result_time_round}s")


if __name__ == "__main__":
    start = 3
    end = 3  # included

    # get_points or rng_grid.get_one_perfect_grid
    func_to_use = get_points

    for i in range(start, end+1):
        if i > 5:
            func_to_use = rng_grid.get_one_perfect_grid
        if i > 6:
            func_to_use = rng_grid.get_one_perfect_grid
        generate_grid(i, func_to_use)

    pygame.quit()
