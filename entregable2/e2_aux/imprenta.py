#!/usr/bin/env python
# -*- coding: utf-8 -*
import sys
from typing import *

Folleto = Tuple[int, int, int]
PosicionFolleto = Tuple[int, int, int, int]


class Hoja:
    def __init__(self, id, alto_actual, ancho_actual, siguiente_altura):
        self.id = id
        self.alto_actual = alto_actual
        self.ancho_actual = ancho_actual
        self.siguiente_altura = siguiente_altura


def optimiza_folletos(tamaño, folletos):
    indices_folletos = sorted(range(len(folletos)), key=lambda x: (-folletos[x][2], -folletos[x][1]))
    sol = []
    hojas = [Hoja(1, 0, 0, folletos[indices_folletos[0]][2])]
    for i in indices_folletos:
        insertada = False
        for hoja in hojas:

            if hoja.ancho_actual + folletos[i][1] <= tamaño:  # Cabe de ancho
                sol.append((folletos[i][0], hoja.id, hoja.ancho_actual, hoja.alto_actual))
                hoja.ancho_actual += folletos[i][1]
                insertada = True
                break
            elif hoja.siguiente_altura + folletos[i][2] <= tamaño:  # Cabe en la siguiente fila
                sol.append((folletos[i][0], hoja.id, 0, hoja.siguiente_altura))
                hoja.ancho_actual = folletos[i][1]
                hoja.alto_actual = hoja.siguiente_altura
                hoja.siguiente_altura = hoja.siguiente_altura + folletos[i][2]
                insertada = True
                break

        if not insertada:  # Crea una nueva hoja e insertamos el folleto en ella
            h = Hoja(len(hojas) + 1, 0, 0, folletos[i][2])
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
    for folleto in lista_folletos:
        print('{} {} {} {}'.format(folleto[0], folleto[1], folleto[2], folleto[3]))


if __name__ == "__main__":
    i, v = lee_fichero_imprenta(sys.argv[1])
    muestra_solucion(optimiza_folletos(i, v))
