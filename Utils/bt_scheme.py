"""
Version: 2.0 (22-oct-2018)

@author: David Llorens (dllorens@uji.es)
         (c) Universitat Jaume I 2018
@license: GPL2
"""
from abc import ABC, abstractmethod
from typing import *

infinity = float("infinity")

Solution = TypeVar('Solution')
State = TypeVar('State')


# Esquema para BT básico --------------------------------------------------------------------------


class PartialSolution(ABC):
    @abstractmethod
    def is_solution(self) -> bool:
        pass

    @abstractmethod
    def get_solution(self) -> Solution:
        pass

    @abstractmethod
    def successors(self) -> Iterable["PartialSolution"]:
        pass


class BacktrackingSolver:
    @staticmethod
    def solve(initial_ps: PartialSolution) -> Iterable[Solution]:
        def bt(ps: PartialSolution) -> Iterable[Solution]:
            if ps.is_solution():
                yield ps.get_solution()
            else:
                for new_ps in ps.successors():
                    yield from bt(new_ps)

        return bt(initial_ps)


class BacktrackingSolverOld:
    @staticmethod
    def solve(initial_ps: PartialSolution) -> List[Solution]:
        def bt(ps: PartialSolution) -> List[Solution]:
            if ps.is_solution():
                return [ps.get_solution()]
            else:
                solutions = []
                for new_ps in ps.successors():
                    solutions.extend(bt(new_ps))
                return solutions

        return bt(initial_ps)


#  Esquema para BT con control de visitados --------------------------------------------------------

class PartialSolutionWithVisitedControl(PartialSolution):
    @abstractmethod
    def successors(self) -> Iterable["PartialSolutionWithVisitedControl"]:
        pass

    @abstractmethod
    def state(self) -> State:
        # the returned object must be of an inmutable type  
        pass


class BacktrackingVCSolver:
    @staticmethod
    def solve(initial_ps: PartialSolutionWithVisitedControl) -> Iterable[Solution]:
        def bt(ps: PartialSolutionWithVisitedControl) -> Iterable[Solution]:
            seen.add(ps.state())
            if ps.is_solution():
                yield ps.get_solution()
            else:
                for new_ps in ps.successors():
                    state = new_ps.state()
                    if state not in seen:
                        yield from bt(new_ps)

        seen = set()
        return bt(initial_ps)


# Esquema para BT para optimización ----------------------------------------------------------------

class PartialSolutionWithOptimization(PartialSolutionWithVisitedControl):
    @abstractmethod
    def successors(self) -> Iterable["PartialSolutionWithOptimization"]:
        pass

    @abstractmethod
    def f(self) -> Union[int, float]:
        # result of applying the objective function to the partial solution
        pass


class BacktrackingOptSolver:
    @staticmethod
    def solve(initial_ps: PartialSolutionWithOptimization) -> Iterable[Solution]:
        def bt(ps: PartialSolutionWithOptimization) -> Iterable[Solution]:
            nonlocal best_solution_found_score
            ps_score = ps.f()
            best_seen[ps.state()] = ps_score
            if ps.is_solution() and ps_score < best_solution_found_score:  # sólo muestra una solución si mejora la última mostrada
                best_solution_found_score = ps_score
                yield ps.get_solution()
            else:
                for new_ps in ps.successors():
                    state = new_ps.state()
                    if state not in best_seen or new_ps.f() < best_seen[state]:
                        yield from bt(new_ps)

        best_seen = {}
        best_solution_found_score = infinity
        return bt(initial_ps)
