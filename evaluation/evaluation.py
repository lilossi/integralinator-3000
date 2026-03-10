from sympy import Expr, Integral, pprint
from sympy.abc import x
from evaluation.controllability import get_controllability_score
from evaluation.expression_depth import get_expression_depth
from evaluation.solvability import solvability_score
from utils.tree_solution import print_solution_tree
from scipy.stats import norm, hmean

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
    print("\nOverall Evaluation Score:")
    print(get_evaluation_score(expr))

    
def get_evaluation_score(expr: Expr) -> float:
    solvability = solvability_score(expr)
    depth = get_expression_depth(expr)
    controllability = get_controllability_score(expr)
    #optimal values and deviation defined here
    adjusted_scores = [
        bell_curve_score(solvability, optimum=20, deviation=4),
        bell_curve_score(depth, optimum=5, deviation=2),
        #very dependent on integral, either bestimmt or unbestimmt
        bell_curve_score(controllability, optimum=7, deviation=3)
    ]
    # different maybe
    return hmean(adjusted_scores)

def bell_curve_score(expr_score: int, optimum: float, deviation: float) -> float:
    #needs peak to normalize score
    peak = norm.pdf(optimum, loc=optimum, scale=deviation)
    return norm.pdf(expr_score, loc=optimum, scale=deviation) / peak