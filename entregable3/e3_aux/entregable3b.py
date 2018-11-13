import sys
from typing import *

from .brikerdef import Move, Block, Level
from Utils.bt_scheme import PartialSolutionWithOptimization, BacktrackingOptSolver, Solution, State


def bricker_opt_solve(level):
    class BrikerOpt_PS(PartialSolutionWithOptimization):
        def __init__(self, block: Block, decisions: Tuple[Move, ...]):
            # TODO: Implementar
            raise NotImplementedError

        def is_solution(self)-> bool:
            # TODO: Implementar
            raise NotImplementedError

        def get_solution(self) -> Solution:
            # TODO: Implementar
            raise NotImplementedError

        def successors(self) -> Iterable["BrikerOpt_PS"]:
            # TODO: Implementar
            raise NotImplementedError

        def state(self) -> State:
            # TODO: Implementar
            raise NotImplementedError

        def f(self) -> Union[int, float]:
            # TODO: Implementar
            raise NotImplementedError

    # TODO: crea initial_ps y llama a BacktrackingOptSolver.solve
    raise NotImplementedError


if __name__ == '__main__':
    level_filename = "level1.txt" # TODO: Cámbialo por sys.argv[1]

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
