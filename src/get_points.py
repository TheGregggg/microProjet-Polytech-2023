from typing import Any


def y(a: int, b: int):
    def func(x: int):
        return x*a + b
    return func


class Node():
    def __init__(self, points=[], banned_lines: list[y] = [], size=10):
        self.points = points
        self.banned_lines = banned_lines
        self.childrens = []
        self.size = size

    def add_node(self, obj):
        self.childrens.append(obj)


def generate_children(node: Node):
    for i in range(node.size + 1):
        for j in range(node.size + 1):
            if (i, j) in node.points:
                continue
            check_invalide = 0
            for banned_line in node.banned_lines:
                # regarde si point est sur la droite pour chaque droite
                if type(banned_line) == int:
                    if i == banned_line:
                        check_invalide += 1
                elif j == banned_line(i):
                    check_invalide += 1

            # si il n'est sur aucune droite, on l'ajoute au points
            if check_invalide == 0:
                # generations des nouvelles droites interdites
                new__ban_lines = []
                for point in node.points:
                    delta_x = i - point[0]
                    delta_y = j - point[1]

                    if delta_x == 0:
                        new__ban_lines.append(i)
                    else:
                        a = delta_y/delta_x
                        b = j - a*i
                        new__ban_lines.append(y(a, b))

                child = Node([value for value in node.points],
                             [value for value in node.banned_lines], size=node.size)
                child.points.append((i, j))
                child.banned_lines += new__ban_lines

                node.childrens.append(child)
                generate_children(child)


root = Node(size=2)
generate_children(root)

leafs = []


def parcours_largeur(noeud):
    file = []
    file.append(noeud)
    while len(file) != 0:
        noeud_en_cours = file.pop()
        if len(noeud_en_cours.childrens) == 0:
            leafs.append(noeud_en_cours)
        else:
            for child in noeud_en_cours.childrens:
                file.append(child)


parcours_largeur(root)

best_leaf = leafs[0]

for leaf in leafs:
    if len(leaf.points) > len(best_leaf.points):
        best_leaf = leaf
