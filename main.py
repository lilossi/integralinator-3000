from sympy import exp, pprint, Expr
from sympy.abc import x
from evaluation.evaluation import print_entire_evaluation, print_vector_evaluation
from test_suite.integral_data import create_integral_dataframe
from test_suite.test_integrals import BAD_INTEGRALS, SOLVABLE_EXPRESSIONS, SOLVABLE_EXPRESSIONS_CHAPTER_1, SOLVABLE_EXPRESSIONS_CHAPTER_2_ONWARD, bad_integrals
from utils.tree_solution import get_solution_vector

def main():
   # ex = exp(-x**2)
   ex = 1/(x**2 + 4)
   print_entire_evaluation(ex)

if __name__ == "__main__":
    main()
