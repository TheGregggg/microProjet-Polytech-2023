from typing import Any
import math


def rotating_points(grid_size, points):
    for point in points:
        point[0] = point[1]
        point[1] = grid_size - point[1]


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


def generate_children(node: Node):
    global nb_generation
    nb_generation += 1
    for i in range(node.size + 1):
        for j in range(node.size + 1):
            if (i, j) in node.points:
                continue

            check_invalide = 0
            for banned_line in node.banned_lines:
                # regarde si point est sur la droite pour chaque droite
                if math.isinf(banned_line[0]):
                    if i == banned_line[1]:
                        check_invalide += 1
                elif j == (banned_line[0]*i + banned_line[1]):
                    check_invalide += 1

            # si il n'est sur aucune droite, on l'ajoute au points
            if check_invalide == 0:
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
                             [value for value in node.banned_lines], size=node.size)
                child.points.append((i, j))
                child.banned_lines += new_ban_lines

                child.points = sorted(
                    child.points, key=lambda tup: (tup[0], tup[1]))
                child.banned_lines = sorted(
                    child.banned_lines, key=lambda tup: (tup[0], tup[1]))

                node.childrens.append(child)
                if (child.points, child.banned_lines) not in already_done_node:
                    already_done_node.append(
                        (child.points, child.banned_lines))
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

    root = Node(size=grid_size)
    generate_children(root)

    leafs = parcours_largeur(root)

    best_leaf = leafs[0]
    for leaf in leafs:
        if len(leaf.points) > len(best_leaf.points):
            best_leaf = leaf

    return best_leaf


# result = get_points(2)
# print(result.points)
# print(f"You generate {nb_generation} childs")

# before caching : gridSize = 2 => 4842 generations
# after caching : gridSize = 2 => 388 generations
