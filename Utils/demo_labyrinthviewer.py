'''
2015-10-05: Versión 1.1
2012-10-03: Version 1

@author: David Llorens dllorens@uji.es

Representamos un laberinto mediante un grafo no dirigido con las siguientes características:
      - Los vértices son tuplas de enteros (fila, columna) que se corresponden con las celdas 
        del laberinto. El vértice (0,0) se corresponde en el dibujo con la celda superior 
        izquierda del laberinto.
      - Sólo puede haber una arista entre dos vértices si se corresponden a celdas vecinas en 
        el laberinto: La existencia de una arista significa que entre dichas celdas del laberinto 
        NO hay muro.

'''
from algoritmia.datastructures.digraphs import UndirectedGraph
from labyrinthviewer import LabyrinthViewer

if __name__ == '__main__':
    e = [((4, 7), (4, 6)), ((4, 7), (4, 8)), ((1, 3), (0, 3)), ((1, 3), (1, 4)), ((4, 8), (4, 9)), ((3, 0), (2, 0)), 
         ((3, 0), (4, 0)), ((2, 8), (2, 7)), ((2, 8), (1, 8)), ((2, 1), (2, 0)), ((2, 1), (2, 2)), ((0, 0), (1, 0)), 
         ((1, 6), (1, 5)), ((1, 6), (2, 6)), ((3, 7), (3, 8)), ((3, 7), (3, 6)), ((2, 5), (1, 5)), ((2, 5), (2, 4)), 
         ((0, 3), (0, 2)), ((4, 0), (4, 1)), ((1, 2), (0, 2)), ((1, 2), (1, 1)), ((4, 9), (3, 9)), ((3, 3), (2, 3)), 
         ((3, 3), (4, 3)), ((2, 9), (3, 9)), ((2, 9), (1, 9)), ((4, 4), (3, 4)), ((4, 4), (4, 3)), ((3, 6), (3, 5)), 
         ((2, 2), (3, 2)), ((4, 1), (4, 2)), ((1, 1), (1, 0)), ((0, 1), (0, 2)), ((3, 2), (3, 1)), ((2, 6), (2, 7)), 
         ((4, 5), (4, 6)), ((0, 4), (0, 5)), ((0, 4), (1, 4)), ((3, 9), (3, 8)), ((0, 5), (0, 6)), ((0, 7), (0, 6)), 
         ((0, 7), (1, 7)), ((4, 2), (4, 3)), ((0, 8), (0, 9)), ((3, 5), (3, 4)), ((1, 8), (1, 7)), ((0, 9), (1, 9)), 
         ((2, 3), (2, 4))]
    
    # Laberinto en forma de grafo no dirigido
    graph = UndirectedGraph(E=e)
    
    #Obligatorio: Crea un LabyrinthViewer pasándole el grafo del laberinto
    lv = LabyrinthViewer(graph, canvas_width=600, canvas_height=400, margin=10)

    #Opcional: Muestra el símbolo 'I' en la celda de entrada al laberinto
    lv.set_input_point((0,0))
    
    #Opcional: Visualiza el símbolo 'O' en la celda de salida del laberinto
    lv.set_output_point((4,9))
    
    #Opcional: marca una celda
    lv.add_marked_cell((3,4), 'red')
    
    #Opcional: Visualiza un camino en azul
    path = [(0, 0), (1, 0), (1, 1), (1, 2), (0, 2), (0, 3), (1, 3), (1, 4), (0, 4), (0, 5), (0, 6), (0, 7), (1, 7), (1, 8), (2, 8), (2, 7), (2, 6), (1, 6), (1, 5), (2, 5), (2, 4), (2, 3), (3, 3), (4, 3), (4, 4), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 9)]
    lv.add_path(path,'blue')
    
    #Obligatorio: Muestra el laberinto
    lv.run()
