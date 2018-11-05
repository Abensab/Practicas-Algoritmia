#!/usr/bin/env python
# -*- coding: utf-8 -*
import sys
from typing import *
import time
import datetime


Folleto = Tuple[int, int, int]
PosicionFolleto = Tuple[int, int, int, int]

"""
                       FORMAT OF FILE:
        |N Folleto |  Tam. Horizontal	|  Tam. Vertical |
        |------------------------------------------------|
        |    1	    |         0	        |       0        |
        |    2	    |         20        |       0        |
        |    3	    |         0	        |       10       |
        |    4	    |         0	        |       0        |

______________________________________________________________

                      FORMAT OF SOLUTION:
    |Nº Folleto | Nº Hoja |	Pos. Horizontal	| Pos. Vertical |
    |-------------------------------------------------------|
    |    1	    |    1	  |        0	    |       0       |
    |    2	    |    1	  |        20       |       0       |
    |    3	    |    1	  |        0	    |       10      |
    |    4	    |    2	  |        0	    |       0       |
"""


def optimiza_folletos(size, folletos):
    print(folletos)
    ordenado = sorted(range(len(folletos)), key=lambda x: (-folletos[x][2], -folletos[x][1]))
    sol = []
    altura_actual, anchura_actual,altura_local = 0, 0, 0
    hoja_actual = 1
    siguiente_altura = 0
    hojas =[]


    for i in ordenado:

        if anchura_actual + folletos[i][1] <= size and altura_actual + folletos[i][2] <= size:  # comparamos anchura y altura
            sol.append((folletos[i][0], hoja_actual, anchura_actual, altura_actual))
            anchura_actual += folletos[i][1]
            if siguiente_altura < folletos[i][2] + siguiente_altura:
                siguiente_altura = folletos[i][2] + altura_local
        else:
            altura_actual = siguiente_altura
            if anchura_actual + folletos[i][1] <= size:
                sol.append((folletos[i][0], hoja_actual, 0, altura_actual))
                anchura_actual = folletos[i][1]
            else:  # Crea una nueva hoja
                hoja_actual += 1
                altura_actual = 0
                sol.append((folletos[i][0], hoja_actual, 0, 0))
                anchura_actual = folletos[i][1]
                altura_local = folletos[i][2]

    return sol


def lee_fichero_imprenta(nombreFichero):
    f = open(nombreFichero)
    folletos = []
    m = f.readline().replace('\n', '')
    for linea in f:
        var = linea.replace('\n', '').split(' ')
        folletos.append([int(i) for i in var])
    f.close()
    return int(m), folletos


def muestra_solucion(lista_folletos):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M')
    path = "C:\\Users\\Abrahan\\PycharmProjects\\Practicas-Algoritmia\\entregable2\\e2_aux\\solution\\"  # windows
    # path = "solution/" #linux
    title = 'Solution-' + str(st) + '.txt'
    new_file = open(path + title, 'w')
    for folleto in lista_folletos:
        new_file.write('{} {} {} {}\n'.format(folleto[0], folleto[1], folleto[2], folleto[3]))
    new_file.close()


if __name__ == "__main__":
    start = time.time()
    print(sys.path)
    i, v = lee_fichero_imprenta(sys.argv[1])
    res = optimiza_folletos(i, v)
    print("--", len(res), "folletos")
    muestra_solucion(res)
    print("\n---Program completed in:", time.time() - start, "seconds---")
