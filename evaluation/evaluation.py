from sympy import Expr, Integral, pprint
from sympy.abc import x
from sympy.integrals.manualintegrate import integral_steps, manualintegrate
from evaluation.controllability import get_controllability_score
from evaluation.controllability import get_symbol_count
from evaluation.expression_depth import get_expression_depth
from evaluation.solvability import is_solvable, solvability_score
from utils.tree_solution import get_solution_vector, print_solution_tree, generate_tree
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
    solvability, depth, controllability = get_evaluation_components(expr)
    #optimal values and deviation defined here
    adjusted_scores = [
        bell_curve_score(solvability, optimum=20, deviation=4),
        bell_curve_score(depth, optimum=5, deviation=2),
        #very dependent on integral, either bestimmt or unbestimmt
        bell_curve_score(controllability, optimum=7, deviation=3)
    ]
    # different maybe
    return hmean(adjusted_scores)


def get_evaluation_components(expr: Expr) -> tuple[int, int, int]:
    # Compute the integration rule tree once and reuse it for solvability + depth.
    tree, solvability = generate_tree(repr(integral_steps(expr, x)))
    depth = tree.depth() + 1
    controllability = get_symbol_count(manualintegrate(expr, x))
    return solvability, depth, controllability

def bell_curve_score(expr_score: int, optimum: float, deviation: float) -> float:
    #needs peak to normalize score
    peak = norm.pdf(optimum, loc=optimum, scale=deviation)
    return norm.pdf(expr_score, loc=optimum, scale=deviation) / peak


def print_vector_evaluation(expr: Expr) -> None:
    print("is solvable:")
    print(is_solvable(expr))
    print("\nSolvability Score Components:")
    print(get_solution_vector(expr))
    print("\nMax Depth:")
    print(get_expression_depth(expr))
    print("Controllability Score:")
    print(get_controllability_score(expr))
    print("\nOverall Evaluation Score:")
    print(get_evaluation_score(expr))