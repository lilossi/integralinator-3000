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
    return calculate_score(solvability, depth, controllability)


def get_evaluation_components(expr: Expr) -> tuple[int, int, int]:
    #more efficient -> only one tree generation
    tree, solvability = generate_tree(repr(integral_steps(expr, x)))
    depth = tree.depth() + 1
    controllability = get_symbol_count(manualintegrate(expr, x))
    return solvability, depth, controllability

def calculate_score(solvability: int, depth: int, controllability: int) -> float:
    #these params can be tuned to adjust the importance of each component
    solv_weight = 0.03
    depth_weight = 0.13
    ctrl_weight = 4.44
    
    norm_solv = bell_curve_score(solvability, optimum=400.74, deviation=80.04)
    norm_depth = bell_curve_score(depth, optimum=2.91, deviation=1.21)
    norm_ctrl = bell_curve_score(controllability, optimum=14.14, deviation=19.59)
    
    norm_scores = [norm_solv, norm_depth, norm_ctrl]
    weights = [solv_weight, depth_weight, ctrl_weight]
    
    return hmean(norm_scores, weights=weights)

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