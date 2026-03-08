from sympy import *
from sympy.integrals.manualintegrate import manualintegrate
from sympy.integrals.manualintegrate import integral_steps
from sympy.abc import x
from utils.solution_tree import *

def number_of_operations(integral) -> float:
    print(repr(integral_steps(integral, x)))
    return manualintegrate(integral, x).count_ops()

def solvability_score(expr) -> float:
    print(solution_tree(expr))
    return len(solution_tree(expr).split('\n'))