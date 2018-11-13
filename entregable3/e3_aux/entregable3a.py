import sys
from typing import *

from .brikerdef import Move, Block, Level
from Utils.bt_scheme import PartialSolutionWithVisitedControl, Solution, State


def bricker_vc_solve(level: Level):
    class BrikerVC_PS(PartialSolutionWithVisitedControl):
        def __init__(self, block: Block, decisions: Tuple[Move, ...]):
            # TODO: Implementar
            raise NotImplementedError

        def is_solution(self) -> bool:
            # TODO: Implementar
            raise NotImplementedError

        def get_solution(self) -> Solution:
            # TODO: Implementar
            raise NotImplementedError

        def successors(self) -> Iterable["BrikerVC_PS"]:
            # TODO: Implementar
            raise NotImplementedError

        def state(self) -> State:
            # TODO: Implementar
            raise NotImplementedError

    # TODO: crea initial_ps y llama a BacktrackingVCSolver.solve
    raise NotImplementedError


if __name__ == '__main__':
    level_filename = "level1.txt"  # TODO: Cámbialo por sys.argv[1]

    print("<BEGIN BACKTRACKING>\n")

    for solution in bricker_vc_solve(Level(level_filename)):
        string_solution = "".join(solution)  # convierte la solución de lista a string
        print("La primera solución encontrada es: {0} (longitud: {1})".format(string_solution, len(string_solution)))
        break

    print("\n<END BACKTRACKING>")
