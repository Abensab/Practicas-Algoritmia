#!/usr/bin/env python
# -*- coding: utf-8 -*-
from entregable3.e3_aux.brikerdef import *



class MockLevel:

    def __init__(self):
        self.level = Level("C:\\Users\\Abrahan\\PycharmProjects\\Practicas-Algoritmia\\entregable3\\test\\mock.txt")
        p1, p2, p3 = Pos2D(0, 0), Pos2D(0, 1), Pos2D(1, 0)  #Esquina inicial
        p4, p5, p6 = Pos2D(2, 2), Pos2D(2, 3), Pos2D(3, 2)  #Central
        p7, p8, p9 = Pos2D(4, 5), Pos2D(4, 4), Pos2D(3, 5)  #Esquina final

        self.standing_block_inicial = Block(p1, p1)
        self.standing_block_centro = Block(p4, p4)
        self.standing_block_final = Block(p7, p7)

        self.lying_row_block_inicial = Block(p1, p2)
        self.lying_row_block_centro = Block(p4, p5)
        self.lying_row_block_final = Block(p7, p8)

        self.lying_col_block_inicial = Block(p1, p3)
        self.lying_col_block_centro = Block(p4, p6)
        self.lying_col_block_final = Block(p7, p9)

    def print(self):
        print(self.level._mat)
        print(self.standing_block_centro.valid_moves(self.level.is_valid))


if __name__ == "__main__":
    m = MockLevel()
    m.print()
