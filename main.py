from ast import expr

from sympy import pprint, Expr
from sympy.abc import x
from evaluation.evaluation import print_entire_evaluation, print_vector_evaluation
from test_suite.integral_data import create_integral_dataframe
from test_suite.test_integrals import BAD_INTEGRALS, SOLVABLE_EXPRESSIONS, SOLVABLE_EXPRESSIONS_CHAPTER_1, SOLVABLE_EXPRESSIONS_CHAPTER_2_ONWARD, bad_integrals
from utils.tree_solution import get_solution_vector

def main():
   df = create_integral_dataframe()
   print(df.head())
   print(df.head(-5))

if __name__ == "__main__":
    main()
