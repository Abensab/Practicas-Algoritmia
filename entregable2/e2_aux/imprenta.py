import sys
from typing import *

Folleto = Tuple[int, int, int]
PosicionFolleto = Tuple[int, int, int, int]


def optimiza_folletos(m: int, folletos: List[Folleto]) -> List[PosicionFolleto]:
    print(folletos)
    for v in folletos:
        print(v)
    ordenado = sorted(range(len(folletos)), key=lambda x: -(folletos[x][1]*folletos[x][2]))
    print(ordenado)
    sol=[-1]*len(folletos)
    espacio = [0]*len(folletos)
    for i in ordenado:
        for j in range(len(espacio)):
            if folletos[i] + espacio[j] <= m:
                sol[i]=j
                espacio[j] = espacio[j] + folletos[i]
                break
    return sol


def lee_fichero_imprenta(nombreFichero: str) -> Tuple[int, List[Folleto]]:
    f = open(nombreFichero)
    folletos = []
    m = f.readline().replace('\n', '')
    for linea in f:
        var = linea.replace('\n', '').split(' ')
        folletos.append([int(i) for i in var])
    f.close()
    return int(m), folletos


def muestra_solucion(solucion: List[PosicionFolleto]):
    for linea in solucion:
        print('{} {} {} {}'.format(linea[0], linea[1], linea[2], linea[3]))


if __name__ == "__main__":
    print(lee_fichero_imprenta(sys.argv[1]))
    i,v = lee_fichero_imprenta(sys.argv[1])
    muestra_solucion(optimiza_folletos(i,v))
