from sympy import *
from evaluation.evaluation import bell_curve_score, print_entire_evaluation
from evaluation.solvability import number_of_operations, solvability_score
from utils.converter_output import *
from utils.tree_solution import generate_tree, print_solution_score, print_solution_tree
from sympy.integrals.manualintegrate import integral_steps

def main():
    x = symbols('x')
    expr: Expr = sin(x) * exp(x)
    expr2: Expr = exp(x) / (1 + exp(2 * x))
    expr3: Expr = x**2 + 3*x + 2
    print_entire_evaluation(expr)
    print_entire_evaluation(expr2)
    print_entire_evaluation(expr3)
if __name__ == "__main__":
    main()
