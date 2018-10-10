from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.datastructures.digraphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo

from Utiles.labyrinthviewer import LabyrinthViewer
import sys




def create_labyrinth(rows: int, cols: int, corridors) -> UndirectedGraph:
    vertices = [(r, c) for r in range(rows) for c in range(cols)]
    mfs = MergeFindSet()
    for v in vertices:
        mfs.add(v)

    return UndirectedGraph(E=corridors)


def matriz_saltos(grafo, v_inicial, rows, cols):
    m = []
    for i in range(rows):
        m.append([0] * cols)
    vertices = []
    queue = Fifo()
    seen = set()
    queue.push((v_inicial, v_inicial))
    while len(queue) > 0:
        v = queue.pop()
        vertices.append(v)
        print(grafo.succs(v))
        for suc in grafo.succs(v):
            if suc not in seen:
                seen.add(suc)
                m[suc[0][suc[1]]] = m[v[0]][v[1]] + 1
                queue.push(suc)
    return m, vertices


def encuentra_muro(mat_inicio, mat_final, descartados):
    min = mat_final[0][0]
    muro = set()

    for s, t in range(descartados):
        suma = mat_inicio[s[0]][s[1]] + mat_final[t[0]][t[1]]
        if suma < min:
            min = suma
            muro = s, t

    return muro, min


if __name__ == '__main__':
    f = open(sys.argv[1])
    fichero = []
    # Paso 1: Leer el fichero y guardarlo en una matriz
    for linea in f:
        fichero.append(linea.split(','))

    f.close()

    edges = []
    descartados = []
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

    graph = create_labyrinth(rows, cols, edges)
    source = 0,0
    target = (rows - 1, cols -1)
    print(graph)
    mat_inicio = matriz_saltos(graph, source, rows, cols)
    mat_final = matriz_saltos(graph, target, rows, cols)

    muro = encuentra_muro(mat_inicio, mat_final, descartados)
    edges.append(muro)
    print(edges)
    print(descartados)

    viewer = LabyrinthViewer(graph, canvas_width=800, canvas_height=480, margin=10)
    viewer.run()
