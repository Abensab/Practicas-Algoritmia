from typing import *


# ---------------------------------------------------------------------------------------------------------

class Move:
    Left = "L"
    Right = "R"
    Up = "U"
    Down = "D"


# ---------------------------------------------------------------------------------------------------------

class Pos2D:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def add_row(self, d) -> "Pos2D":
        return Pos2D(self.row + d, self.col)

    def add_col(self, d) -> "Pos2D":
        return Pos2D(self.row, self.col + d)

    def __eq__(self, other):
        if not isinstance(other, Pos2D): return False
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

    def __repr__(self):
        return "Pos2D({}, {})".format(self.row, self.col)


# ---------------------------------------------------------------------------------------------------------

class Level:
    def __init__(self, filename: str):

        self._mat = [line.strip() for line in open(filename).readlines()]
        self.rows = len(self._mat)
        self.cols = len(self._mat[0])
        self._sPos, self._tPos = self._load_level(self._mat)

    def is_valid(self, pos: Pos2D) -> bool:
        if pos.col >= 0 and pos.col < self.cols and pos.row >= 0 and pos.row < self.rows:
            baldosa = self._mat[pos.row][pos.col]
            return baldosa == 'o' or baldosa == 'T'
        return False

    def get_startpos(self) -> Pos2D:
        return self._sPos

    def get_targetpos(self) -> Pos2D:
        return self._tPos

    def _load_level(self, matriz: List[List["char"]]) -> Tuple[Pos2D, ...]:
        posI = Pos2D(0, 0)
        posF = Pos2D(0, 0)

        for i, fila in enumerate(matriz):
            for j, col in enumerate(fila):
                if col == 'S':
                    posI = posI.add_col(j).add_row(i)
                if col == 'T':
                    posF = posF.add_col(j).add_row(i)

        return posI, posF


# ---------------------------------------------------------------------------------------------------------

class Block:
    def __init__(self, b1: Pos2D, b2: Pos2D):
        assert isinstance(b1, Pos2D) and isinstance(b2, Pos2D)
        if b2.row < b1.row or (b2.row == b1.row and b2.col < b1.col):
            self._b1, self._b2 = b2, b1
        else:
            self._b1, self._b2 = b1, b2

    # -----------------------------------------------------------------------------
    # <BEGIN> Funciones para comparar correctamente objetos de tipo Block

    def __eq__(self, other):
        if not isinstance(other, Block): return False
        return self._b1 == other._b1 and self._b2 == other._b2

    # Necesario para poder meter objetos de tipo Block en colecciones
    def __hash__(self):
        return hash((self._b1, self._b2))

    # <END> Funciones para comparar correctamente objetos de tipo Block
    # -----------------------------------------------------------------------------

    def __repr__(self):
        return "Block({}, {})".format(self._b1, self._b2)

    def is_standing(self) -> bool:  # true si el bloque está de pie
        return self._b1.row == self._b2.row and self._b1.col == self._b2.col

    def is_standing_at_pos(self, pos: Pos2D) -> bool:
        # Devuelve true si el bloque está de pie en la posición indicada en el parámetro
        return self.is_standing() and self._b1.row == pos.row and self._b1.col == pos.col

    def is_lying_on_a_row(self) -> bool:  # true si el bloque está tumbado en una fila
        return self._b1.row == self._b2.row and self._b1.col != self._b2.col

    def is_lying_on_a_col(self) -> bool:  # true si el bloque está tumbado en una columna
        return self._b1.row != self._b2.row and self._b1.col == self._b2.col

    def valid_moves(self, is_valid_pos: Callable[[Pos2D], bool]) -> Iterable[Move]:
        valid_moves = []
        standing = [((-2, 0), (-1, 0)), ((2, 0), (1, 0)), ((0, 2), (0, 1)), ((0, -2), (0, -1))]
        lying_row = [((-1, 0), (-1, 0)), ((1, 0), (1, 0)), ((0, 2), (0, 1)), ((0, -1), (0, -2))]
        lying_col = [((-1, 0), (-2, 0)), ((2, 0), (1, 0)), ((0, 1), (0, 1)), ((0, -1), (0, -1))]
        moves = [Move.Up, Move.Down, Move.Right, Move.Left]
        if self.is_standing():
            for i, p in enumerate(standing):
                block1, block2 = self._b1.add_row(p[0][0]), self._b1.add_row(p[1][0])
                block1 = block1.add_col(p[0][1])
                block2 = block2.add_col(p[1][1])
                if is_valid_pos(block1) and is_valid_pos(block2):
                    valid_moves.append(moves[i])

        if self.is_lying_on_a_col():
            for i, p in enumerate(lying_col):
                block1, block2 = self._b1.add_row(p[0][0]), self._b2.add_row(p[1][0])
                block1 = block1.add_col(p[0][1])
                block2 = block2.add_col(p[1][1])

                if is_valid_pos(block1) and is_valid_pos(block2):
                    valid_moves.append(moves[i])

        if self.is_lying_on_a_row():
            for i, p in enumerate(lying_row):
                block1, block2 = self._b1.add_row(p[0][0]), self._b2.add_row(p[1][0])
                block1 = block1.add_col(p[0][1])
                block2 = block2.add_col(p[1][1])

                if is_valid_pos(block1) and is_valid_pos(block2):
                    valid_moves.append(moves[i])

        return valid_moves

    def move(self, m: Move) -> "Block":
        # TODO: IMPLEMENTAR - Debe devolver un nuevo objeto 'Block', sin modificar el original
        movimientos = {
            Move.Up: 0,
            Move.Down: 1,
            Move.Right: 2,
            Move.Left: 3
        }
        movimientos_estado = [(((-1, 0), (-2, 0)), ((-1, 0), (-2, 0)), ((-1, 0), (-1, 0))),
                              (((1, 0), (2, 0)), ((2, 0), (1, 0)), ((1, 0), (1, 0))),
                              (((0, 1), (0, 2)), ((0, 1), (0, 1)), ((0, 2), (0, 1))),
                              (((0, -2), (0, -1)), ((0, -1), (0, -1)), ((0, -1), (0, -2)))]
        if self.is_standing():
            b1 = self._b1.add_row(movimientos_estado[movimientos[m]][0][0][0])
            b1 = b1.add_col(movimientos_estado[movimientos[m]][0][0][1])
            b2 = self._b2.add_row(movimientos_estado[movimientos[m]][0][1][0])
            b2 = b2.add_col(movimientos_estado[movimientos[m]][0][1][1])
            return Block(b1, b2)

        elif self.is_lying_on_a_col():
            b1 = self._b1.add_row(movimientos_estado[movimientos[m]][1][0][0])
            b1 = b1.add_col(movimientos_estado[movimientos[m]][1][0][1])
            b2 = self._b2.add_row(movimientos_estado[movimientos[m]][1][1][0])
            b2 = b2.add_col(movimientos_estado[movimientos[m]][1][1][1])
            return Block(b1, b2)

        elif self.is_lying_on_a_row():
            b1 = self._b1.add_row(movimientos_estado[movimientos[m]][2][0][0])
            b1 = b1.add_col(movimientos_estado[movimientos[m]][2][0][1])
            b2 = self._b2.add_row(movimientos_estado[movimientos[m]][2][1][0])
            b2 = b2.add_col(movimientos_estado[movimientos[m]][2][1][1])
            return Block(b1, b2)

# ---------------------------------------------------------------------------------------------------------
