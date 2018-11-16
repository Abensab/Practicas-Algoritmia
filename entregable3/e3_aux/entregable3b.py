import sys
from typing import *

from entregable3.e3_aux.brikerdef import Move, Block, Level
from Utils.bt_scheme import PartialSolutionWithOptimization, BacktrackingOptSolver, Solution, State


def bricker_opt_solve(level):
    class BrikerOpt_PS(PartialSolutionWithOptimization):
        def __init__(self, block: Block, decisions: Tuple[Move, ...]):
            # TODO: Implementar
            self.block = block
            self.decisions = decisions
            self.n = len(decisions)

        def is_solution(self)-> bool:
            # TODO: Implementar
            return self.block.is_standing_at_pos(level.get_targetpos())

        def get_solution(self) -> Solution:
            return self.decisions

        def successors(self) -> Iterable["BrikerOpt_PS"]:
            for elem in self.block.valid_moves(level.is_valid):
                yield BrikerOpt_PS(self.block.move(elem), self.decisions + (elem,))

        def state(self) -> State:
            return self.block

        def f(self) -> Union[int, float]:
            return self.n

    # TODO: crea initial_ps y llama a BacktrackingOptSolver.solve
    bloque = Block(level.get_startpos(), level.get_startpos())
    return BacktrackingOptSolver.solve(BrikerOpt_PS(bloque, ()))


if __name__ == '__main__':
    level_filename = sys.argv[1]                        # TODO: Cámbialo por sys.argv[1]

    print("<BEGIN BACKTRACKING>\n")

    # la última solución que devuelva será la más corta
    solutions = list(bricker_opt_solve(Level(level_filename)))

    if len(solutions)==0:
        print("El puzle no tiene solución.")
    else:
        best_solution = solutions[-1]
        string_solution = "".join(best_solution) #convierte la solución de lista  a  string
        print("La solución más corta es: {0} (longitud: {1})".format(string_solution, len(string_solution)))

    print("\n<END BACKTRACKING>")
