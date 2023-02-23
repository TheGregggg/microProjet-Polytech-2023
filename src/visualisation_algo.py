from typing import Any
import traceback
import sys
import math

import pygame
from pygame.locals import *

import time

from get_points import *

height = 800
width = 800

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode([width, height], pygame.RESIZABLE)

font = pygame.font.SysFont("Arial", 20)

grid_size = 2
grid_color = (20, 20, 20)  # rgb

start_time = time.time()

result = get_points(grid_size)

end_time = time.time()
result_time = end_time-start_time


def draw(node):
    screen.fill((255, 255, 255))

    grid_space = min(height, width)/(grid_size+2)

    padding_height = grid_space
    padding_width = grid_space

    if height > width:
        padding_height = height/2 - grid_space*grid_size/2
    else:
        padding_width = width/2 - grid_space*grid_size/2

    screen.fill((255, 255, 255))

    # cols
    for i in range(grid_size+1):
        pygame.draw.line(screen, grid_color, (i*grid_space + padding_width,
                         padding_height), (i*grid_space + padding_width, height - padding_height))

    # rows
    for i in range(grid_size+1):
        pygame.draw.line(screen, grid_color, (padding_width, i*grid_space +
                         padding_height), (width - padding_width, i*grid_space + padding_height))

    for droite in node.banned_lines:
        if math.isinf(droite[0]):
            x = droite[1]
            pygame.draw.line(screen, (0, 255, 0), (padding_width + x*grid_space,
                             padding_height), (padding_width + x*grid_space, height - padding_height))

        else:
            y_start = droite[1]
            y_end = droite[0]*grid_size + droite[1]

            pygame.draw.line(screen, (0, 255, 0), (padding_width, padding_height + y_start *
                                                   grid_space), (width - padding_width, padding_height + y_end*grid_space))

    for point in node.points:
        x, y = point
        pygame.draw.circle(screen, (255, 0, 0),
                           (x*grid_space + padding_width + 1, y*grid_space + padding_height + 1), 5)

    txt = f"Temps de calcul : {result_time:.3f}s"
    width_text, height_text = font.size(txt)
    txt_render = font.render(txt, True, grid_color)
    screen.blit(txt_render, (width/2 - width_text/2,
                height - padding_height/2 - height_text/2))

    pygame.display.flip()


""" benchmark on laptop
optimisation cache
grid 2 => 0.010s
grid 3 => 42s


optimisation symetrie check et rotations
grid 2 => 0.002s
grid 3 => 0.1s
grid 4 => 30s

fix optimisation symetrie
grid 2 => 0.002s
grid 3 => 0.01s
grid 4 => 10.5s

"""


def rotating_points(grid_size, points):
    points_to_return = []
    for point in points:
        new_point = (grid_size-point[1], point[0])
        points_to_return.append(new_point)
    return points_to_return


def symetrie_horizontal(grid_size, points):
    points_to_return = []
    for point in points:
        new_point = (grid_size - point[0], point[1])
        points_to_return.append(new_point)
    return points_to_return


def symetrie_vertical(grid_size, points):
    points_to_return = []
    for point in points:
        new_point = (point[0], grid_size - point[1])
        points_to_return.append(new_point)
    return points_to_return


class Node():
    def __init__(self, points=[], banned_lines: list = [], size=10, generation=0):
        self.points = points

        # list of tuple (a,b) or (0,0,x) if its a vertical line
        self.banned_lines = banned_lines
        self.childrens = []
        self.size = size
        self.generation = generation

    def add_node(self, obj):
        self.childrens.append(obj)


already_done_node = []
nb_generation = 0

nb_check_pos_point = 0


def generate_children(node: Node):
    global nb_generation, nb_check_pos_point, clock
    nb_generation += 1
    print(node.points, node.banned_lines, node.generation)
    draw(node)

    pygame.event.clear()
    a = True
    while a:
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                a = False

    for i in range(node.size + 1):

        allowed_y = [*range(node.size + 1)]

        for banned_line in node.banned_lines:
            if math.isinf(banned_line[0]):
                if i == banned_line[1]:
                    allowed_y = []
                    break
            else:
                y_to_remove = banned_line[0]*i + banned_line[1]
                if y_to_remove in allowed_y:
                    allowed_y.remove(y_to_remove)

        for j in allowed_y:
            print(f"GEN {node.generation} | DOING J : {j} with I still : {i}")
            if (i, j) in node.points:
                continue

            # generations des nouvelles droites interdites
            new_ban_lines = []
            for point in node.points:
                delta_x = i - point[0]
                delta_y = j - point[1]

                if delta_x == 0:
                    new_ban_lines.append((math.inf, i))
                else:
                    a = int(delta_y/delta_x)
                    b = int(j - a*i)
                    new_ban_lines.append((a, b))

            child = Node([value for value in node.points],
                         [value for value in node.banned_lines], size=node.size, generation=node.generation+1)
            child.points.append((i, j))
            child.banned_lines += new_ban_lines

            child.points = sorted(
                child.points, key=lambda tup: (tup[0], tup[1]))
            child.banned_lines = sorted(
                child.banned_lines, key=lambda tup: (tup[0], tup[1]))

            node.childrens.append(child)
            if child.points in already_done_node:
                continue

            pass_rotation_tests = True
            rotation = child.points
            for a in range(3):
                rotation = rotating_points(node.size, rotation)
                rotation = sorted(
                    rotation, key=lambda tup: (tup[0], tup[1]))
                if rotation in already_done_node:
                    pass_rotation_tests = False
                    break

            if not pass_rotation_tests:
                continue

            sym_hori = symetrie_horizontal(node.size, child.points)
            sym_hori = sorted(
                sym_hori, key=lambda tup: (tup[0], tup[1]))

            if sym_hori in already_done_node:
                continue

            sym_vert = symetrie_vertical(node.size, child.points)
            sym_vert = sorted(
                sym_vert, key=lambda tup: (tup[0], tup[1]))

            if sym_vert in already_done_node:
                continue

            already_done_node.append(child.points)
            generate_children(child)
        print(f"GEN {node.generation} | Finish J, I go up")
    print(f"GEN {node.generation} | Finish I")


def parcours_largeur(noeud):
    to_return = []
    file = []
    file.append(noeud)
    while len(file) != 0:
        noeud_en_cours = file.pop()
        if len(noeud_en_cours.childrens) == 0:
            to_return.append(noeud_en_cours)
        else:
            for child in noeud_en_cours.childrens:
                file.append(child)

    return to_return


def get_points(grid_size: int) -> list:
    global nb_generation
    nb_generation = 0

    print("generating childs")

    root = Node(size=grid_size)
    generate_children(root)

    print("finish generating childs")
    print("getting leafs")
    leafs = parcours_largeur(root)

    print("getting best leaf")

    best_leaf = leafs[0]
    for leaf in leafs:
        if len(leaf.points) > len(best_leaf.points):
            best_leaf = leaf

    return best_leaf


clock = pygame.time.Clock()
get_points(grid_size)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
