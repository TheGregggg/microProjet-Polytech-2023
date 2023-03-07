
def rotating_points(grid_size, points):
    points_to_return = []
    for point in points:
        new_point = (grid_size-1-point[1], point[0])
        points_to_return.append(new_point)
    return points_to_return


def symetrie_horizontal(grid_size, points):
    points_to_return = []
    for point in points:
        new_point = (grid_size-1 - point[0], point[1])
        points_to_return.append(new_point)
    return points_to_return


def symetrie_vertical(grid_size, points):
    points_to_return = []
    for point in points:
        new_point = (point[0], grid_size-1 - point[1])
        points_to_return.append(new_point)
    return points_to_return


class Node():
    def __init__(self, points=[], grid: list = [], size=10, generation=0):
        self.points = points

        # list of tuple (a,b) or (0,0,x) if its a vertical line
        self.grid = grid
        self.childrens = []
        self.size = size
        self.generation = generation

    def add_child(self, obj):
        self.childrens.append(obj)


already_done_node = {}

should_continue = True


def generate_children(node: Node):
    global should_continue

    i = 0
    while should_continue and i < node.size:

        allowed_y = node.grid[i]

        j_index = 0
        while j_index < len(allowed_y):
            j = allowed_y[j_index]

            j_index += 1

            new_grid = [list(line) for line in node.grid]

            child = Node([value for value in node.points],
                         [], size=node.size, generation=node.generation+1)
            child.points.append((i, j))

            if len(child.points) == (node.size)*2:
                should_continue = False
                node.add_child(child)

            # generations des nouvelles droites interdites
            for point in node.points:
                delta_x = i - point[0]
                delta_y = j - point[1]

                if delta_x == 0:
                    new_grid[i] = []  # remove vertical line
                else:
                    a = delta_y/delta_x
                    b = j - a*i
                    for x in range(node.size):
                        y_to_remove = a*x + b
                        if y_to_remove == int(y_to_remove) and y_to_remove in new_grid[x]:
                            new_grid[x].remove(y_to_remove)

            if j in new_grid[i]:
                new_grid[i].remove(j)

            child.grid = new_grid

            child.points = sorted(
                child.points, key=lambda tup: (tup[0], tup[1]))

            if node.generation in already_done_node:
                if child.points in already_done_node[node.generation]:
                    continue

                pass_rotation_tests = True
                rotation = child.points
                for a in range(3):
                    rotation = rotating_points(node.size, rotation)
                    rotation = sorted(
                        rotation, key=lambda tup: (tup[0], tup[1]))
                    if rotation in already_done_node[node.generation]:
                        pass_rotation_tests = False
                        break

                if not pass_rotation_tests:
                    continue

                sym_hori = symetrie_horizontal(node.size, child.points)
                sym_hori = sorted(
                    sym_hori, key=lambda tup: (tup[0], tup[1]))

                if sym_hori in already_done_node[node.generation]:
                    continue

                sym_vert = symetrie_vertical(node.size, child.points)
                sym_vert = sorted(
                    sym_vert, key=lambda tup: (tup[0], tup[1]))

                if sym_vert in already_done_node[node.generation]:
                    continue

                already_done_node[node.generation].append(child.points)
            else:
                already_done_node[node.generation] = [child.points]

            node.add_child(child)
            generate_children(child)

        i += 1


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
    global should_continue

    print("generating childs")

    base_grid = []
    for grid_size_to_use in range(1, grid_size+1):
        base_grid = []
        for i in range(grid_size_to_use):
            line = []
            for y in range(grid_size_to_use):
                line.append(y)
            base_grid.append(line)

        should_continue = True

        root = Node(size=grid_size_to_use, grid=base_grid)
        generate_children(root)

    print("finish generating childs")
    print("getting leafs")

    leafs = parcours_largeur(root)

    print("getting best leaf")

    best_leafs = [leafs[0]]
    for leaf in leafs:
        if len(leaf.points) > len(best_leafs[0].points):
            best_leafs = [leaf]
        elif(len(leaf.points) == len(best_leafs[0].points)):
            best_leafs.append(leaf)

    return best_leafs


if __name__ == "__main__":
    result = get_points(4)
    print(result)

# before caching : grid 2 => 4842 generations
# after caching : grid 2 => 388 generations
# after symetrie and rotation checking : grid = 2 => 96 generations
# after fixing precedent implementation : grid 2 => 54 generations | grid 3 => 668 generations | grid 4 => 12115 generations
