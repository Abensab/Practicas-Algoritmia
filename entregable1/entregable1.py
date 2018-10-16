from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.datastructures.digraphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo

from Utils.labyrinthviewer import LabyrinthViewer
import sys
import time


def create_labyrinth(rows: int, cols: int, corridors) -> UndirectedGraph:
    vertices = [(r, c) for r in range(rows) for c in range(cols)]
    mfs = MergeFindSet()
    for v in vertices:
        mfs.add(v)

    return UndirectedGraph(E=corridors)


def jump_matrix(grafo, num_rows: int, num_cols: int, v_inicial):
    m = []
    for r in range(num_rows):
        m.append([0] * num_cols)
    vertices = []
    queue = Fifo()
    seen = set()
    queue.push(v_inicial)
    seen.add(v_inicial)
    while len(queue) > 0:
        v = queue.pop()
        vertices.append(v)
        for suc in grafo.succs(v):
            if suc not in seen:
                seen.add(suc)
                m[suc[0]][suc[1]] = m[v[0]][v[1]] + 1
                queue.push(suc)
    return m


def path(g: UndirectedGraph, source: "T", target: "T"):
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


def get_remove_edge(matrix_init, matrix_fin, descartados):
    edge_remove = set()
    min = matrix_fin[0][0]

    for s, t in descartados:
        if matrix_init[s[0]][s[1]] + matrix_fin[t[0]][t[1]] < min:
            edge_remove = s, t
            min = matrix_init[s[0]][s[1]] + matrix_fin[t[0]][t[1]]

    return edge_remove, min


def get_edges(fichero):
    edges, descartados = [], []
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

    return edges, descartados


def lee_fichero(fichero):
    f = open(fichero)
    mapa = []
    for linea in f:
        mapa.append(linea.split(','))
    f.close()
    return mapa


if __name__ == '__main__':
    start_time = time.time()

    # Paso 1: Leer el fichero y guardarlo en una matriz
    mapa = lee_fichero(sys.argv[1])

    rows = len(mapa)
    cols = len(mapa[0])

    source = (0, 0)
    target = (rows - 1, cols - 1)

    # Paso 2: Obtener la lista de aristas del laberinto y las aristas descartadas
    edges, descartados = get_edges(mapa)

    # Paso 3: Crear el grafo para recorrer el único camino
    graph = create_labyrinth(rows, cols, edges)

    # Paso 4: Crear las matrices de saltos desde el inico y desde el final del laberinto
    matrix_inicio = jump_matrix(graph, rows, cols, (0, 0))
    matrix_fin = jump_matrix(graph, rows, cols, (rows - 1, cols - 1))

    # Paso 5: Obtener el vértice que hay que añadir al grafo para encontrar el camino más corto y la distancia
    edge, new_distance = get_remove_edge(matrix_inicio, matrix_fin, descartados)

    # Paso 6: Mostrar el resultado por pantalla para pasar los tests
    print(' '.join([str(i[0]) + " " + str(i[1]) for i in edge]))

    # Indistintamente puede usarse una forma o la otra, tener en cuenta las carácterísticas de estas matrices
    print(matrix_fin[0][0])
    # print(matrix_inicio[rows-1][cols-1])

    print(new_distance + 1)

    ''' No es necesario añadir el vertice en el grafo ni volver a calcular el camino,
        porque podemos obtenerlos sin necesidad de calcular nuevos caminos, como
        se hace anteriormente. Los siguientes pasos se han de realizar en el caso
        que se quiera mostrar ambos caminos por cada laberinto, además del 
        tiempo que ha tardado en realizar los cálculos
    '''
    # edges.append(edge)
    # new_graph = create_labyrinth(rows, cols, edges)
    #
    # road = path(graph, source, target)
    # new_road = path(new_graph, source, target)

    # print("\n\n--- %s seconds ---" % (time.time() - start_time))

    # viewer = LabyrinthViewer(graph, canvas_width=800, canvas_height=480, margin=10)
    # viewer.add_path(new_road, color="green", offset=-3)
    # viewer.add_path(road, color="blue")
    # viewer.run()
