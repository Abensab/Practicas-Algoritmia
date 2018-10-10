from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.datastructures.digraphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo
import sys

from Utils.labyrinthviewer import LabyrinthViewer

def create_labyrinth(rows: int, cols: int, corridors) -> UndirectedGraph:
    vertices = [(r, c) for r in range(rows) for c in range(cols)]
    mfs = MergeFindSet()
    for v in vertices:
        mfs.add(v)

    return UndirectedGraph(E=corridors)

def path(g, source: "T", target: "T"):
    la = traveler_edges_width(g, source)
    bp = {}
    for (u, v) in la:
        bp[v] = u
    road = []
    v = target
    road.append(v)
    while bp[v] != v:
        v = bp[v]
        road.append(v)

    return road

def traveler_edges_width(graph, v_initial):
    edges = []
    queue = Fifo()
    seen = set()
    queue.push((v_initial, v_initial))
    seen.add(v_initial)
    while len(queue) > 0:
        u, v = queue.pop()
        edges.append((u, v))
        for suc in graph.succs(v):
            if suc not in seen:
                seen.add(suc)
                queue.push((v, suc))
    return edges

def matriz_saltos(grafo, v_inicial, rows, cols):
    m = []
    for i in range(rows):
        m.append([0] * cols)
    vertices = []
    queue = Fifo()
    seen = set()
    queue.push((v_inicial, v_inicial))
    while len(queue) > 0:
        u, v = queue.pop()
        vertices.append((u, v))
        print("v",v,"u:",u)
        for suc in grafo.succs(v):
            if suc not in seen:
                seen.add(suc)
                m[suc[0]][suc[1]] = m[v[0]][v[1]] + 1
                queue.push((v, suc))
    return m, vertices


def encuentra_muro(mat_inicio, mat_final, descartados):
    min = mat_final[0][0]
    muro = set()

    for s, t in descartados:
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
                if i + 1 < len(fichero):
                    descartados.append(((i, j), (i + 1, j)))
            if 'e' not in fichero[i][j]:
                edges.append(((i, j), (i, j + 1)))
            else:
                if j + 1 < len(fichero[0]):
                    descartados.append(((i, j), (i, j + 1)))

    rows = len(fichero)
    cols = len(fichero[0])

    graph = create_labyrinth(rows, cols, edges)
    source = 0, 0
    target = rows - 1, cols -1

    print(graph)
    mat_inicio, la = matriz_saltos(graph, source, rows, cols)
    mat_final, miau= matriz_saltos(graph, target, rows, cols)

    muro = encuentra_muro(mat_inicio, mat_final, descartados)
    edges.append(muro)
    new_graph = create_labyrinth(rows, cols, edges)


    road = path(graph, source, target)
    new_road = path(new_graph, source, target)

    print(len(road))
    print(len(new_road))

    viewer = LabyrinthViewer(graph, canvas_width=800, canvas_height=480, margin=10)
    viewer.add_path(new_road, color="green", offset=-3)
    viewer.add_path(road, color="blue")
    viewer.run()
