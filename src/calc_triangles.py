from get_points_simplfied import *
import csv


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

                a = point1
                b = point2
                c = point3

                # use determinant forumula : https://fr.wikipedia.org/wiki/Aire_d%27un_triangle
                det = (b[0]-a[0])*(c[1]-a[1]) - (c[0]-a[0])*(b[1]-a[1])
                triangle_surface = abs(det)/2

                # help trouble shot problemes
                # if triangle_surface == 0:
                #     print(a, b, c)

                if triangle_surface in surfaces:
                    surfaces[triangle_surface] += 1
                else:
                    surfaces[triangle_surface] = 1

    surfaces_lists = list(surfaces.keys())
    surfaces_lists.sort()
    surfaces = {i: surfaces[i] for i in surfaces_lists}

    return {'surfaces': surfaces, 'triangles': already_done}


def calc_triangle_from_csv_triangles(name):
    with open(name, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            a = (int(row['x_a']), int(row['y_a']))
            b = (int(row['x_b']), int(row['y_b']))
            c = (int(row['x_c']), int(row['y_c']))

            det = (b[0]-a[0])*(c[1]-a[1]) - (c[0]-a[0])*(b[1]-a[1])
            triangle_surface = abs(det)/2

            if triangle_surface == 0:
                print(a, b, c)


if __name__ == "__main__":
    calc_triangle_from_csv_triangles("./results/grid 9x9/triangles.csv")
