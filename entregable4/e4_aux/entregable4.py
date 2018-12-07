import sys

from typing import List, Tuple
from Utils.kdtree import KDTree, KDLeaf, Axis, KDNode


def read_points(filename: str) -> List[Tuple[float, float]]:
    points = []
    for linea in open(filename).readlines():
        i = linea.split(" ")
        points.append((float(i[0]), float(i[1])))
    return points


def build_kd_tree(points: List[Tuple[float, float]]) -> KDTree:
    def build(list_x, list_y):
        x = len(list_x)
        y = len(list_y)
        if x == 1 and y == 1:
            return KDLeaf(points[list_x[0]])

        else:
            if abs(points[list_x[-1]][0] - points[list_x[0]][0]) > abs(
                    points[list_y[-1]][1] - points[list_y[0]][1]):  # Cortamos por el eje Y
                axis = Axis.X
                if x % 2 == 0:
                    split_value = (points[list_x[x // 2 - 1]][0] + points[list_x[x // 2]][0]) / 2
                else:
                    split_value = points[list_x[x // 2]][0]

                right_x, left_x = list_x[:x // 2], list_x[x // 2:]
                right_y, left_y = get_list(right_x, list_y)
            else:  # Cortamos por el eje X
                axis = Axis.Y
                if x % 2 == 0:
                    split_value = (points[list_y[y // 2]][1] + points[list_y[y // 2 - 1]][1]) / 2
                else:
                    split_value = points[list_y[y // 2]][1]

                right_y, left_y = list_y[:y // 2], list_y[y // 2:]
                right_x, left_x = get_list(right_y, list_x)
            return KDNode(axis, split_value, build(right_x, right_y), build(left_x, left_y))

    x_list = sorted(range(len(points)), key=lambda d: points[d][0])
    y_list = sorted(range(len(points)), key=lambda z: points[z][1])
    return build(x_list, y_list)


def get_list(busqueda: List[int], lugar: List[int]) ->Tuple[List[int], List[int]]:
    left = []
    right = []
    for i in lugar:
        if i in busqueda:
            left.append(i)
        else:
            right.append(i)
    return left, right


if __name__ == "__main__":
    points = read_points(sys.argv[1])
    kdtree = build_kd_tree(points)
    print(kdtree.pretty())
