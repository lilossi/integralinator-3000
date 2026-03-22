from sympy import *
from evaluation.controllability import get_controllability_score
from evaluation.evaluation import print_entire_evaluation
from evaluation.expression_depth import get_expression_depth
from test_suite.test_integrals import *
from sympy.integrals.manualintegrate import manualintegrate
from sympy.integrals.manualintegrate import integral_steps

from utils.tree_solution import get_solution_vector
def main():
    for integral in SOLVABLE_EXPRESSIONS:
        print(get_expression_depth(integral))

if __name__ == "__main__":
    main()
