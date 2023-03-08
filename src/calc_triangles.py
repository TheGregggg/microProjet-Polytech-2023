from get_points_simplfied import *


def calc_triangle(list_points):
    already_done = []
    surfaces = {}

    for point1 in list_points:
        for point2 in list_points:
            if point2 == point1:
                continue
            for point3 in list_points:
                if point2 == point3 or point1 == point3:
                    continue

                points = [point1, point2, point3]
                points = sorted(
                    points, key=lambda tup: (tup[0], tup[1]))

                if points in already_done:
                    continue
                else:
                    already_done.append(points)

                right_point = points[-1]
                left_point = points[0]

                points = sorted(
                    points, key=lambda tup: (tup[1], tup[0]))

                top_point = points[-1]
                bottom_point = points[0]

                rectangle_length = right_point[0] - left_point[0]
                rectangle_height = top_point[1] - bottom_point[1]

                # calc triangle surface

                rectangle_surface = rectangle_height*rectangle_length
                # tp x - lp x -> longueur rect, tp y - lp y -> largeur rect
                top_left_triangle_surface = (top_point[0] - left_point[0]) * \
                    (top_point[1] - left_point[1])/2

                top_right_triangle_surface = (right_point[0] - top_point[0]) * \
                    (top_point[1] - right_point[1])/2

                bottom_left_triangle_surface = (bottom_point[0] - left_point[0]) * \
                    (left_point[1] - bottom_point[1])/2

                bottom_right_triangle_surface = (right_point[0] - bottom_point[0]) * \
                    (right_point[1] - bottom_point[1])/2

                triangle_surface = rectangle_surface - top_left_triangle_surface - \
                    top_right_triangle_surface - bottom_left_triangle_surface - \
                    bottom_right_triangle_surface

                print(sorted(points, key=lambda tup: (
                    tup[0], tup[1])), bottom_point, left_point, right_point[1] - bottom_point[1], triangle_surface)

                if triangle_surface in surfaces:
                    surfaces[triangle_surface] += 1
                else:
                    surfaces[triangle_surface] = 1

    surfaces_lists = list(surfaces.keys())
    surfaces_lists.sort()
    surfaces = {i: surfaces[i] for i in surfaces_lists}

    return surfaces


if __name__ == "__main__":
    result = get_points(3)
    surfaces = calc_triangle(result[0].points)
    print(surfaces)
