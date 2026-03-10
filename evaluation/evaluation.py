from sympy import Expr, Integral, pprint
from sympy.abc import x
from evaluation.controllability import get_controllability_score
from evaluation.expression_depth import get_expression_depth
from evaluation.solvability import solvability_score
from utils.tree_solution import print_solution_tree


def print_entire_evaluation(expr: Expr) -> None:
    print("Expression:")
    pprint(Integral(expr, x))
    print("\nSolution Tree:")
    print_solution_tree(expr)
    print("\nSolvability Score:")
    print(solvability_score(expr))
    print("\nMax Depth:")
    print(get_expression_depth(expr))
    print("Controllability Score:")
    print(get_controllability_score(expr))

    