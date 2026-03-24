from sympy import pprint

from evaluation.evaluation import print_vector_evaluation
from test_suite.integral_data import create_integral_dataframe
from test_suite.test_integrals import SOLVABLE_EXPRESSIONS_CHAPTER_1, SOLVABLE_EXPRESSIONS_CHAPTER_2_ONWARD, bad_integrals

def main():
   pprint(SOLVABLE_EXPRESSIONS_CHAPTER_2_ONWARD[0])

if __name__ == "__main__":
    main()
