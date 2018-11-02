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

    def __init__(self, id, size):
        self.id = id
        self.h = []
        self.pamphlet = {}
        self.area = size * size
        for i in range(size):
            self.h.append([0] * size)

    def get_fist_available_by_width(self, p_width, p_height):
        # print("get_fist_available_by_width", p_width, p_height)
        for i in range(len(self.h)):
            # print("I: ",i)
            for j in range(len(self.h[0])):
                is_ = self.is_good_place(p_width, p_height, (i, j))
                # print("Position",i, j, "Available:", is_)
                if self.h[i][j] == 0 and is_:
                    return i, j
        return

    def get_fist_available_by_heigth(self, p_width, p_height, ):
        for j in range(len(self.h[0])):
            for i in range(len(self.h)):
                is_ = self.is_good_place(p_width, p_height, (i, j))
                # print("Position",i, j, "Available:", is_)
                if self.h[i][j] == 0 and is_:
                    return i, j
        return

    def get_data_at_position(self, position):
        return self.pamphlet[self.h[position]]

    def is_good_place(self, p_width, p_height, position):
        r = position[0]  # row
        c = position[1]  # col
        # print(position)
        if position[0] + p_width > len(self.h[0]) or position[1] + p_height > len(self.h):
            # print("Se sale por el lado")
            return False
        while r < position[0] + p_width:
            if self.h[r][position[1]] != 0:
                # print("---- Salimos porque no hay sitio de ancho", r, "Supuesto:", position[0]+p_width, "valor:", self.h[r][position[1]])
                return False
            r += 1
        while c < position[1] + p_height:
            if self.h[position[0]][c] != 0:
                # print("---- Salimos porque no hay sitio de alto", c, "Supuesto:", position[1]+p_height, "valor:", self.h[position[0]][c])
                return False
            c += 1
        return True

    def put_pamphlet(self, pamphlet):
        pamphlet_area = pamphlet[1] * pamphlet[2]
        # print("Area: ", self.area, "Pamphlet:", pamphlet_area)
        if pamphlet_area <= self.area:
            position = self.get_fist_available_by_width(pamphlet[1], pamphlet[2])
            # position = self.get_fist_available_by_width(pamphlet[1], pamphlet[2])
            if position is None:
                return False

            for r in range(position[0], position[0] + pamphlet[1]):
                for c in range(position[1], position[1] + pamphlet[2]):
                    self.h[r][c] = pamphlet[0]
            self.pamphlet[position] = pamphlet
            self.area -= pamphlet_area
            return True
        return False


def optimiza_folletos(size, folletos):
    print(folletos)

    for v in folletos:
        print(v)
    # We order by width descending
    ordenado = sorted(range(len(folletos)), key=lambda x: -(folletos[x][1]))
    print("--Ordenado--")
    sol = []
    sol.append(Hoja(1, size))
    print("--Empezamos--")
    cont = 0
    for i in ordenado:
        cont += 1
        print("Folleto", cont, "de", len(folletos),
              "| Hojas hasta el momento:", len(sol))
        added = False
        for hoja in sol:
            res = hoja.put_pamphlet(folletos[i])
            if res:
                added = True
                break
        if not added:
            new_hoja = Hoja(len(sol) + 1, size)
            new_hoja.put_pamphlet(folletos[i])
            sol.append(new_hoja)
        if i>100:
            break
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


def muestra_solucion(lista_hojas):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M')
    path = "entregable2/e2_aux/solution/"
    title = 'Solution-' + str(st)
    new_file = open(path + title + '.txt', 'w')
    for hoja in lista_hojas:
        for k, folleto in hoja.pamphlet.items():
            new_file.write('{} {} {} {}\n'.format(folleto[0], hoja.id, k[0], k[1]))
    new_file.close()

if __name__ == "__main__":
    start = time.time()
    i, v = lee_fichero_imprenta(sys.argv[1])
    res = optimiza_folletos(i, v)
    print("--", len(res), "folletos")
    muestra_solucion(res)
    print("\n---Program completed in:", time.time() - start, "seconds---")
