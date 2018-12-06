import sys
from abc import ABC, abstractmethod

from typing import List, Tuple


class Axis:
    X = 0
    Y = 1


class KDTree(ABC):
    @abstractmethod
    def pretty(self, level: int = 0) -> str: pass


class KDNode(KDTree):
    def __init__(self, axis: Axis, split_value: float, child1: KDTree, child2: KDTree):
        self.axis = axis  # Eje utilizado para separar sus hijos (Axis.X o Axis.Y)
        self.split_value = split_value  # Coordenada x o y (depende de axis)
        self.child1 = child1  # Hijo izquierdo o superior (Coordenada x o y (depende de axis) < split_value)
        self.child2 = child2  # Hijo dererecho o inferior (Coordenada x o y (depende de axis) >= split_value)

    def pretty(self, level: int = 0) -> str:
        return "       " * level + f"KDNode({self.axis}, {self.split_value},\n" + \
               self.child1.pretty(level + 1) + ",\n" + self.child2.pretty(level + 1) + "\n" + \
               "       " * level + ")"


class KDLeaf(KDTree):
    def __init__(self, point: Tuple[float, float]):
        self.point = point

    def pretty(self, level: int = 0) -> str:
        return "       " * level + "KDLeaf({0})".format(self.point)


def read_points(filename: str) -> List[Tuple[float, float]]:
    points = []
    for linea in open(filename).readlines():
        i = linea.split(" ")
        points.append((float(i[0]), float(i[1])))

    return points


def build_kd_tree(points: List[Tuple[float, float]]) -> KDTree:
    def build(lx, ly):
        x = len(lx)
        y = len(ly)
        if x == 1 and y == 1:
            return KDLeaf(points[lx[0]])
        else:
            #print("-Lx:", lx, " -Ly:", ly)
            if abs(points[lx[-1]][0] - points[lx[0]][0]) > abs(
                    points[ly[-1]][1] - points[ly[0]][1]):  # Cortamos por el eje Y
                #print("Elegimos X")
                axis = Axis.X
                if x % 2 == 0:
                    split_value = (points[lx[x // 2 - 1]][0] + points[lx[x // 2]][0]) / 2
                else:
                    split_value = points[lx[x // 2]][0]
                dx, ix = lx[:x // 2], lx[x // 2:]
                dy, iy = get_lista(dx, ly)
            else:  # Cortamos por el eje X
                #print("Elegimos Y")
                axis = Axis.Y
                if x % 2 == 0:
                    split_value = (points[ly[y // 2]][1] + points[ly[y // 2 - 1]][1]) / 2
                else:
                    split_value = points[ly[y // 2 ]][1]
                dy, iy = ly[:y // 2], ly[y // 2:]
                dx, ix = get_lista(dy, lx)
            #print("split", axis, split_value)
            return KDNode(axis, split_value, build(dx, dy), build(ix, iy))

    #print(points)
    x_list = sorted(range(len(points)), key=lambda d: points[d][0])
    y_list = sorted(range(len(points)), key=lambda z: points[z][1])
    # indices_folletos = sorted(range(len(folletos)), key=lambda x: (-folletos[x][2], -folletos[x][1]))
    return build(x_list, y_list)


def get_lista(busqueda, lugar):
    l = []
    r = []
    for i in lugar:
        if i in busqueda:
            l.append(i)
        else:
            r.append(i)
    print(l, r)
    return l, r


if __name__ == "__main__":
    points = read_points(sys.argv[1])
    kdtree = build_kd_tree(points)
    print(kdtree.pretty())
    # Utilizando las dos funciones anteriores, implementa el programa entregable4.py que reciba como
    # parámetro el nombre de un fichero de puntos, obtenga el kd-tree siguiendo el criterio de partición
    # “estándar” presentado anteriormente y, por último, que lo imprima por pantalla. Dado que las clases
    # KDNode y KDLeaf de partida tienen implementado el método pretty() que devuelve la
    # información del objeto como una cadena, puedes hacerlo fácilmente con
    # print(kdtree.pretty()).
    pass
