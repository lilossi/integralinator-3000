from sympy import pprint, Expr
from sympy.abc import x
from evaluation.evaluation import print_entire_evaluation, print_vector_evaluation
from test_suite.integral_data import create_integral_dataframe
from test_suite.test_integrals import BAD_INTEGRALS, SOLVABLE_EXPRESSIONS, SOLVABLE_EXPRESSIONS_CHAPTER_1, SOLVABLE_EXPRESSIONS_CHAPTER_2_ONWARD, bad_integrals

def main():
   print_entire_evaluation(BAD_INTEGRALS[0])

if __name__ == "__main__":
    main()
