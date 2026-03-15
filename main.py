from sympy import *
from evaluation.evaluation import print_entire_evaluation
from test_suite.test_integrals import *

def main():
    x = symbols('x')
    print_entire_evaluation(chapter_1_1[4])
    print_entire_evaluation(chapter_1_7[5])
    print_entire_evaluation(chapter_2_1[6])
if __name__ == "__main__":
    main()
