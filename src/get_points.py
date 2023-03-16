########################################
#
#     Place points on grid of NxN
#  Algorithm coded by Gregoire Layet
#  microProjet Polytech 2022 | PEIP 1
#        all right reserved
#
########################################

################################
#     Typing definition
################################

Point = tuple[int, int]
Points = list[Point]


################################
#     Symmetry functions
################################

def rotating_points(grid_size: int, points: Points) -> Points:
    """Rotate all the point by 90 degree to the right. Meant to rotate a complete grid

    Args:
        grid_size (int): the size of the grid where the points are
        points (Points): list of the points, list of (x,y) coords

    Returns:
        Points: list of the new points, rotated by 90 degree
    """

    points_to_return = []
    for point in points:
        new_point = (grid_size-1 - point[1], point[0])
        points_to_return.append(new_point)
    return points_to_return


def horizontal_symmetry(grid_size: int, points: Points) -> Points:
    """Apply a horizontal symmetry to the points. Meant to be applied on a complete grid

    Args:
        grid_size (int): the size of the grid where the points are
        points (Points): list of the points, list of (x,y) coords

    Returns:
        Points: list of the new points, by symmetry
    """

    points_to_return = []
    for point in points:
        new_point = (grid_size - 1 - point[0], point[1])
        points_to_return.append(new_point)
    return points_to_return


def vertical_symmetry(grid_size: int, points: Points) -> Points:
    """Apply a vertical symmetry to the points. Meant to be applied on a complete grid

    Args:
        grid_size (int): the size of the grid where the points are
        points (Points): list of the points, list of (x,y) coords

    Returns:
        Points: list of the new points, by symmetry
    """

    points_to_return = []
    for point in points:
        new_point = (point[0], grid_size-1 - point[1])
        points_to_return.append(new_point)
    return points_to_return


################################
#   Node class and functions
################################


class Node():
    def __init__(self, points: Points = [], grid: list = [], size: int = 10, generation: int = 0):
        self.points = points
        self.grid = grid
        self.childrens = []
        self.size = size
        self.generation = generation

    def add_child(self, child: 'Node'):
        self.childrens.append(child)


def breadth_first_search(root: Node) -> list[Node]:
    """Know as 'Parcours en largeur d'abord' in French, a BFS implementation to retrieve the leafs of the tree

    Args:
        root (Node): the root of the tree

    Returns:
        list[Node]: list of the leafs of the tree
    """

    leafs_to_return = []
    queue = []
    queue.append(root)
    while len(queue) != 0:
        current_node = queue.pop()

        if len(current_node.childrens) == 0:
            leafs_to_return.append(current_node)
        else:
            for child in current_node.childrens:
                queue.append(child)

    return leafs_to_return


################################
#  Main algorithm function
################################

already_done_node = {}


def generate_children(node: Node):
    global already_done_node

    for i in range(node.size):

        allowed_y = node.grid[i]

        for j in allowed_y:

            new_grid = [list(line) for line in node.grid]

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

            child = Node([value for value in node.points],
                         new_grid, size=node.size, generation=node.generation)
            child.points.append((i, j))

            child.points = sorted(
                child.points, key=lambda tup: (tup[0], tup[1]))

            if node.generation in already_done_node:
                pass_rotation_tests = True
                rotation = child.points
                for a in range(4):
                    if rotation in already_done_node[node.generation]:
                        pass_rotation_tests = False
                        break

                    sym_hori = horizontal_symmetry(node.size, rotation)
                    sym_hori = sorted(
                        sym_hori, key=lambda tup: (tup[0], tup[1]))

                    if sym_hori != rotation and sym_hori in already_done_node[node.generation]:
                        pass_rotation_tests = False
                        break

                    sym_vert = vertical_symmetry(node.size, rotation)
                    sym_vert = sorted(
                        sym_vert, key=lambda tup: (tup[0], tup[1]))

                    if sym_vert != rotation and sym_vert in already_done_node[node.generation]:
                        pass_rotation_tests = False
                        break

                    rotation = rotating_points(node.size, rotation)
                    rotation = sorted(
                        rotation, key=lambda tup: (tup[0], tup[1]))

                if not pass_rotation_tests:
                    continue

                already_done_node[node.generation].append(child.points)
            else:
                already_done_node[node.generation] = [child.points]

            node.add_child(child)
            generate_children(child)


def get_points(grid_size: int) -> list[list[Points]]:

    # To improve perfs, we generate the grid from 1x1 to NxN beacause when a grid is generated, its added to the already_done_grids variable.
    # What improve perfs is that the best solution of a NxN grid can't be a solution of a N-1XN-1 grid,
    # base on that we calculate all the grid before to remove a lot a useless grid in the NxN one.

    # generating childs from grid 1 to grid_size
    for grid_size_to_use in range(1, grid_size+1):
        base_grid = []
        for i in range(grid_size_to_use):
            line = []
            for y in range(grid_size_to_use):
                line.append(y)
            base_grid.append(line)

        root = Node(size=grid_size_to_use, grid=base_grid)
        generate_children(root)

    leafs = breadth_first_search(root)

    # retrieve the best leafs, the ones with the most among of points

    best_leafs = [leafs[0]]
    for leaf in leafs:
        if len(leaf.points) > len(best_leafs[0].points):
            best_leafs = [leaf]
        elif(len(leaf.points) == len(best_leafs[0].points)):
            best_leafs.append(leaf)

    return best_leafs


if __name__ == "__main__":
    result = get_points(5)
    print(result[0].points)
