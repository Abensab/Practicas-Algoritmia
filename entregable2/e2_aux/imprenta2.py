'''
Created on 27 de oct. de 2015

@author: CARJOVIC
'''

import sys
from asyncio.log import logger

def lee_fichero_imprenta(nombreFichero: "String") -> "(int, List<Folleto>)":
        
    fichero = open(nombreFichero, encoding='utf-8').readlines()
    m = int(fichero[0])
    folletos = []
    
    for linea in fichero[1:]:
        linea = linea.rstrip("\n").split(" ")
        folletos.append((int(linea[0]),int(linea[1]),int(linea[2])))

    return (m,folletos)


def optimiza_folletos(m: "int", folletos: "List<Folleto>") -> "List<PosicionFolleto>":
    '''
    El algoritmo asume que los folletos están ordenados de mayor a menor altura.
    Ordenamos los indices para que cumpla con ese orden y para no modificar folletos.
    '''
    indiceFolletos = sorted(range(len(folletos)), key=lambda i:-folletos[i][2])
    distrFolletos = [0]*len(folletos)
    
    anchoLocal = m
    altoLocal = folletos[indiceFolletos[0]][2]
    pivote = 0 #Delimita las filas para que no solapen los folletos
    
    hojas = [(m,altoLocal,0)] #lista de hojas con una hoja inicial
    
    for elem in indiceFolletos:
        isIn = False
        for i,pag in enumerate(hojas):
            
            #almacenamos los datos de estado de la hoja actual
            anchoLocal = pag[0]
            altoLocal = pag[1]
            pivote = pag[2]
            
            if(anchoLocal-folletos[elem][1] >= 0):
                #cabe a lo ancho
                isIn = True
            elif((altoLocal+folletos[elem][2]) <= m):
                #fila llena, pero cabe a lo alto e la siguiente fila
                anchoLocal = m
                pivote = altoLocal
                altoLocal += folletos[elem][2]
                isIn = True
                
            if(isIn == False):
                if(i == len(hojas)-1):
                    '''
                    el folleto no se ha podido meter en ninguna hoja
                    existente creamos una nueva guardando el estado de la
                    anterior como siempre
                    '''
                    hojas[i] = (anchoLocal,altoLocal,pivote) #guardamos estado
                    pivote = 0
                    altoLocal = folletos[elem][2]
                    distrFolletos[elem] = (elem+1,len(hojas)+1,0,0)
                    anchoLocal = m-folletos[elem][1]          
                    hojas.append((anchoLocal,altoLocal,0))
                    break
            else:
                distrFolletos[elem] = (elem+1,i+1,m-anchoLocal,pivote)
                anchoLocal -= folletos[elem][1]
                hojas[i] = (anchoLocal,altoLocal,pivote) #guardamos estado
                break
    
    return distrFolletos


def muestra_solucion(solucion: "List<PosicionFolleto>"):
    path = "C:\\Users\\Abrahan\\PycharmProjects\\Practicas-Algoritmia\\entregable2\\e2_aux\\solution\\"  # windows
    # path = "solution/" #linux
    title = 'Solution.txt'
    new_file = open(path + title, 'w')
    for elem in solucion:
        new_file.write("{0} {1} {2} {3}\n".format(elem[0],elem[1],elem[2],elem[3]))
    new_file.close()

if(len(sys.argv) < 2):
    logger.error("Te has dejado el argumento del fichero.")
    exit(1)

m,folletos = lee_fichero_imprenta(sys.argv[1])
solucion = optimiza_folletos(m, folletos)    
muestra_solucion(solucion)

