from typing import Any
import math


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
    def __init__(self, points=[], banned_lines: list = [], size=10):
        self.points = points

        # list of tuple (a,b) or (0,0,x) if its a vertical line
        self.banned_lines = banned_lines
        self.childrens = []
        self.size = size

    def add_node(self, obj):
        self.childrens.append(obj)


already_done_node = []
nb_generation = 0

nb_check_pos_point = 0


def generate_children(node: Node):
    global nb_generation, nb_check_pos_point
    nb_generation += 1

    for i in range(node.size + 1):

        allowed_y = [*range(node.size + 1)]

        # parcours par sense inverse
        for i_banned_line in range(len(node.banned_lines)):
            banned_line = node.banned_lines[-i_banned_line]
            if math.isinf(banned_line[0]):
                if i == banned_line[1]:
                    allowed_y = []
                    break
            else:
                y_to_remove = int(banned_line[0]*i + banned_line[1])
                if y_to_remove in allowed_y:
                    allowed_y.remove(y_to_remove)
            nb_check_pos_point += 1

        for j in allowed_y:
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
                nb_check_pos_point += 1

            child = Node([value for value in node.points],
                         [value for value in node.banned_lines], size=node.size)
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


if __name__ == "__main__":
    result = get_points(2)
    print(result.points)
    print(f"You generate {nb_generation} childs")
    print(nb_check_pos_point)

# before caching : grid 2 => 4842 generations
# after caching : grid 2 => 388 generations
# after symetrie and rotation checking : grid = 2 => 96 generations
# after fixing precedent implementation : grid 2 => 54 generations | grid 3 => 668 generations | grid 4 => 12115 generations
