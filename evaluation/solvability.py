from sympy import *
from sympy.integrals.manualintegrate import manualintegrate
from sympy.integrals.manualintegrate import integral_steps
from sympy.abc import x
from utils.tree_solution import get_solution_score

def number_of_operations(integral) -> int:
    print(repr(integral_steps(integral, x)))
    return manualintegrate(integral, x).count_ops()

def solvability_score(expr) -> int:
    return get_solution_score(expr)