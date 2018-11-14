#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from entregable3.test.mockLevel import *


class TestPos2D(unittest.TestCase):
    def __init__(self, test_name):
        super(TestPos2D, self).__init__(test_name)

    def setUp(self):
        self.origen = Pos2D(0, 0)
        self.destino = Pos2D(10, 10)

    def tearDown(self):
        self.origen = None
        self.destino = None

    def test_add_row(self):
        self.assertEqual(self.origen.add_row(1), Pos2D(1, 0))
        self.assertEqual(self.destino.add_row(1), Pos2D(11, 10))
        self.assertEqual(self.origen.add_row(-1), Pos2D(-1, 0))
        self.assertEqual(self.destino.add_row(-1), Pos2D(9, 10))

    def test_add_col(self):
        self.assertEqual(self.origen.add_col(1), Pos2D(0, 1))
        self.assertEqual(self.destino.add_col(1), Pos2D(10, 11))
        self.assertEqual(self.origen.add_col(-1), Pos2D(0, -1))
        self.assertEqual(self.destino.add_col(-1), Pos2D(10, 9))


class TestLevel(unittest.TestCase):

    def __init__(self, test_name):
        super(TestLevel, self).__init__(test_name)
        self.level = MockLevel()

    def test_is_standing(self):
        self.assertTrue(self.level.standing_block_inicial.is_standing())
        self.assertFalse(self.level.lying_col_block_inicial.is_standing())
        self.assertFalse(self.level.lying_row_block_inicial.is_standing())

    def test_is_lying_on_a_col(self):
        self.assertFalse(self.level.standing_block_inicial.is_lying_on_a_col())
        self.assertTrue(self.level.lying_col_block_inicial.is_lying_on_a_col())
        self.assertFalse(self.level.lying_row_block_inicial.is_lying_on_a_col())

    def test_is_lying_on_a_row(self):
        self.assertFalse(self.level.standing_block_inicial.is_lying_on_a_row())
        self.assertFalse(self.level.lying_col_block_inicial.is_lying_on_a_row())
        self.assertTrue(self.level.lying_row_block_inicial.is_lying_on_a_row())

    def test_valid_moves_standing(self):
        self.assertEqual(self.level.standing_block_inicial.valid_moves(self.level.level.is_valid), ['D', 'R'])
        self.assertEqual(self.level.standing_block_centro.valid_moves(self.level.level.is_valid), ['U', 'D', 'R', 'L'])
        self.assertEqual(self.level.standing_block_final.valid_moves(self.level.level.is_valid), ['U', 'L'])

    def test_valid_moves_lying_col(self):
        self.assertEqual(self.level.lying_col_block_centro.valid_moves(self.level.level.is_valid), ['U', 'D', 'R', 'L'])
        self.assertEqual(self.level.lying_col_block_final.valid_moves(self.level.level.is_valid), ['U', 'L'])
        self.assertEqual(self.level.lying_col_block_inicial.valid_moves(self.level.level.is_valid), ['D', 'R'])

    def test_valid_moves_lying_row(self):
        self.assertEqual(self.level.lying_row_block_centro.valid_moves(self.level.level.is_valid), ['U', 'D', 'R', 'L'])
        self.assertEqual(self.level.lying_row_block_final.valid_moves(self.level.level.is_valid), ['U', 'L'])
        self.assertEqual(self.level.lying_row_block_inicial.valid_moves(self.level.level.is_valid), ['D', 'R'])


    def test_move_standing(self):
        #Esquina superior izquierda
        self.assertEqual(self.level.standing_block_inicial.move(Move.Down), Block(Pos2D(1, 0), Pos2D(2, 0)))
        self.assertEqual(self.level.standing_block_inicial.move(Move.Right), Block(Pos2D(0, 1), Pos2D(0, 2)))
        #Centro
        self.assertEqual(self.level.standing_block_centro.move(Move.Up), Block(Pos2D(1, 2), Pos2D(0, 2)))
        self.assertEqual(self.level.standing_block_centro.move(Move.Down), Block(Pos2D(3, 2), Pos2D(4, 2)))
        self.assertEqual(self.level.standing_block_centro.move(Move.Right), Block(Pos2D(2, 3), Pos2D(2, 4)))
        self.assertEqual(self.level.standing_block_centro.move(Move.Left), Block(Pos2D(2, 0), Pos2D(2, 1)))
        #Esquina inferior derecha
        self.assertEqual(self.level.standing_block_final.move(Move.Up), Block(Pos2D(3, 5), Pos2D(2, 5)))
        self.assertEqual(self.level.standing_block_final.move(Move.Left), Block(Pos2D(4, 3), Pos2D(4, 4)))

    def test_move_lying_on_a_col(self):
        #Esquina superior izquierda
        self.assertEqual(self.level.lying_col_block_inicial.move(Move.Down), Block(Pos2D(2, 0), Pos2D(2, 0)))
        self.assertEqual(self.level.lying_col_block_inicial.move(Move.Right), Block(Pos2D(0, 1), Pos2D(1, 1)))
        #Centro
        self.assertEqual(self.level.lying_col_block_centro.move(Move.Up), Block(Pos2D(1, 2), Pos2D(1, 2)))
        self.assertEqual(self.level.lying_col_block_centro.move(Move.Down), Block(Pos2D(4, 2), Pos2D(4, 2)))
        self.assertEqual(self.level.lying_col_block_centro.move(Move.Right), Block(Pos2D(2, 3), Pos2D(3, 3)))
        self.assertEqual(self.level.lying_col_block_centro.move(Move.Left), Block(Pos2D(2, 1), Pos2D(3, 1)))
        #Esquina inferior derecha
        self.assertEqual(self.level.lying_col_block_final.move(Move.Up), Block(Pos2D(2, 5), Pos2D(2, 5)))
        self.assertEqual(self.level.lying_col_block_final.move(Move.Left), Block(Pos2D(3, 4), Pos2D(4, 4)))

    def test_move_lying_on_a_row(self):
        #Esquina superior izquierda
        self.assertEqual(self.level.lying_row_block_inicial.move(Move.Down), Block(Pos2D(1, 0), Pos2D(1, 1)))
        self.assertEqual(self.level.lying_row_block_inicial.move(Move.Right), Block(Pos2D(0, 2), Pos2D(0, 2)))
        #Centro
        self.assertEqual(self.level.lying_row_block_centro.move(Move.Up), Block(Pos2D(1, 2), Pos2D(1, 3)))
        self.assertEqual(self.level.lying_row_block_centro.move(Move.Down), Block(Pos2D(3, 2), Pos2D(3, 3)))
        self.assertEqual(self.level.lying_row_block_centro.move(Move.Right), Block(Pos2D(2, 4), Pos2D(2, 4)))
        self.assertEqual(self.level.lying_row_block_centro.move(Move.Left), Block(Pos2D(2, 1), Pos2D(2, 1)))
        #Esquina inferior derecha
        self.assertEqual(self.level.lying_row_block_final.move(Move.Up), Block(Pos2D(3, 4), Pos2D(3, 5)))
        self.assertEqual(self.level.lying_row_block_final.move(Move.Left), Block(Pos2D(4, 3), Pos2D(4, 3)))

