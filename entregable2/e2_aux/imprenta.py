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


class Hoja:
    def __init__(self, id, alto_actual, ancho_actual, siguiente_altura):
        self.id = id
        self.alto_actual = alto_actual
        self.ancho_actual = ancho_actual
        self.siguiente_altura = siguiente_altura


def optimiza_folletos(size, folletos):
    indices_folletos = sorted(range(len(folletos)), key=lambda x: (-folletos[x][2], -folletos[x][1]))
    sol = []
    # altura_actual, anchura_actual, altura_local, siguiente_altura = 0, 0, 0, 0
    # hoja_actual = 1
    hojas = [Hoja(1, 0, 0, folletos[indices_folletos[0]][2])]
    for i in indices_folletos:
        insertada = False
        for hoja in hojas:
            if(hoja.id==1 and folletos[i][1]==4):
                print("..",hoja.id, folletos[i])
            if hoja.ancho_actual + folletos[i][1] <= size:  #Cabe de ancho
                if hoja.id==1:
                    print(hoja.ancho_actual, folletos[i])
                sol.append((folletos[i][0], hoja.id, hoja.ancho_actual, hoja.alto_actual))
                hoja.ancho_actual += folletos[i][1]
                insertada = True
                break
            elif hoja.siguiente_altura + folletos[i][2]<=size: #Cabe en la siguiente fila
                sol.append((folletos[i][0], hoja.id, 0, hoja.siguiente_altura))
                hoja.ancho_actual = folletos[i][1]
                hoja.alto_actual = hoja.siguiente_altura
                hoja.siguiente_altura = hoja.siguiente_altura + folletos[i][2]
                insertada = True
                break

        if not insertada:# Crea una nueva hoja e insertamos el folleto en ella
            h = Hoja(len(hojas)+1, 0, 0, folletos[i][2])
            sol.append((folletos[i][0], h.id, 0, 0))
            h.ancho_actual = folletos[i][1]
            hojas.append(h)

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
    st = datetime.datetime.fromtimestamp(ts).strftime('%M')
    path = "C:\\Users\\Abrahan\\PycharmProjects\\Practicas-Algoritmia\\entregable2\\e2_aux\\solution\\"  # windows
    # path = "solution/" #linux
    title = 'Solution-' + str(st) + '.txt'
    new_file = open(path + title, 'w')
    for folleto in lista_folletos:
        new_file.write('{} {} {} {}\n'.format(folleto[0], folleto[1], folleto[2], folleto[3]))
    new_file.close()


if __name__ == "__main__":
    start = time.time()
    i, v = lee_fichero_imprenta(sys.argv[1])
    res = optimiza_folletos(i, v)
    print("--", len(res), "folletos")
    muestra_solucion(res)
    print("\n---Program completed in:", time.time() - start, "seconds---")
