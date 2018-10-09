from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.datastructures.digraphs import UndirectedGraph

import sys


def create_labyrinth(rows: int, cols: int, corridors) -> UndirectedGraph:
    vertices = [(r, c) for r in range(rows) for c in range(cols)]
    mfs = MergeFindSet()
    for v in vertices:
        mfs.add(v)

    return UndirectedGraph(E=corridors)


if __name__ == '__main__':
    f = open(sys.argv[1])
    fichero = []
    # Paso 1: Leer el fichero y guardarlo en una matriz
    for linea in f:
        fichero.append(linea.split(','))

    f.close()
    edges = []
    descartados=[]
    for i in range(len(fichero)):
        for j in range(len(fichero[0])):
            if 's' not in fichero[i][j]:
                edges.append(((i, j), (i + 1, j)))
            else:
                descartados.append(((i, j), (i + 1, j)))
            if 'e' not in fichero[i][j]:
                edges.append(((i, j), (i, j + 1)))
            else:
                descartados.append(((i, j), (i, j + 1)))
    rows = len(fichero)
    cols = len(fichero[0])
    print(edges)
    print(descartados)

    graph = create_labyrinth(rows, cols,edges)
    viewer = LabyrinthViewer(graph, canvas_width=800, canvas_height=480, margin=10)
    viewer.run()


