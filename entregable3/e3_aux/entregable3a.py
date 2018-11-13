import sys
from typing import *

from .brikerdef import Move, Block, Level
from Utils.bt_scheme import PartialSolutionWithVisitedControl, Solution, State


def bricker_vc_solve(level: Level):
    class BrikerVC_PS(PartialSolutionWithVisitedControl):
        def __init__(self, block: Block, decisions: Tuple[Move, ...]):
            self.block = block
            self.decisions=decisions
            self.n = len(decisions)

        def is_solution(self) -> bool:
            return self.block.is_standing_at_pos(level.get_targetpos())

        def get_solution(self) -> Solution:
            return self.decisions

        def successors(self) -> Iterable["BrikerVC_PS"]:
            if not self.is_solution():
                for elem in self.block.valid_moves(level.is_valid):
                    yield BrikerVC_PS(self.block.move(elem), self.decisions+(elem,))

        def state(self) -> State:
            return self.block

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
