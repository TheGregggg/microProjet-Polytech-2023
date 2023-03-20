import random
import sys
import calc_triangles


def possible_coord(grid):
    points = []
    for i in range(len(grid)):
        for value in grid[i]:
            points.append((i, value))

    return points


def round_nb(nb):
    rounded = round(nb)
    if abs(rounded - nb) < 0.000001:
        return rounded
    return nb


class Node():
    def __init__(self, points=[], grid: list = [], size=10, generation=0):
        if len(points) == 0:
            self.points = []
        else:
            self.points = points

        if len(grid) == 0:
            self.grid = []
        else:
            self.grid = grid
        self.childrens = []
        self.size = size
        self.generation = generation

    def add_child(self, obj):
        self.childrens.append(obj)


should_continue = True


def generate_random_grid(size):
    global should_continue

    base_grid = []
    for i in range(size):
        line = []
        for y in range(size):
            line.append(y)
        base_grid.append(line)

    node = Node(size=size, grid=base_grid)

    possible_choices = possible_coord(node.grid)

    while should_continue and len(possible_choices) != 0:

        new_point = random.choice(possible_choices)

        i, j = new_point

        if len(node.points)+1 == (node.size)*2:
            node.points.append(new_point)
            should_continue = False
            break

        for point in node.points:
            delta_x = i - point[0]
            delta_y = j - point[1]

            if delta_x == 0:
                node.grid[i] = []  # remove vertical line
            else:
                for x in range(node.size):
                    a = round_nb(delta_y/delta_x)
                    b = round_nb(j - delta_y/delta_x*i)
                    y_to_remove = round_nb(a*x + b)
                    if y_to_remove == int(y_to_remove) and y_to_remove in node.grid[x]:
                        node.grid[x].remove(y_to_remove)

        if j in node.grid[i]:
            node.grid[i].remove(j)

        node.points.append(new_point)

        possible_choices = possible_coord(node.grid)

    return node


def get_best_of_n_grid(grid_size: int, n_grids: int = 10):
    global should_continue
    grids = []
    for i in range(n_grids):
        should_continue = True
        grids.append(generate_random_grid(grid_size))

    return grids


def get_one_perfect_grid(grid_size):
    global should_continue
    should_continue = True
    last_grid = None
    while should_continue:
        last_grid = generate_random_grid(grid_size)

    return [last_grid]


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "help":
        print(
            "-- Random Grid by Greg --\nCommandes : \n - perfect [grid size] | get a perfect solution")

    elif cmd == "perfect":
        size = int(sys.argv[2])
        result = get_one_perfect_grid(size)
        print(result[0].points)
    else:
        print("Unknown command, try help")
