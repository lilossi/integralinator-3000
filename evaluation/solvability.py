from sympy import *
from sympy.integrals.manualintegrate import manualintegrate
from sympy.integrals.manualintegrate import integral_steps
from sympy.abc import x
from utils.tree_solution import get_solution_score
from func_timeout import FunctionTimedOut

def number_of_operations(integral) -> int:
    print(repr(integral_steps(integral, x)))
    return manualintegrate(integral, x).count_ops()


def is_solvable(expr) -> bool:
    solution = repr(integral_steps(expr, x))
    if "DontKnowRule" in solution:
        return False
    return True