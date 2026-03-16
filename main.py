from sympy import *
import random
from evaluation.evaluation import print_entire_evaluation
from evaluation.solvability import is_solvable
from test_suite.test_integrals import *

def main():
    for expr in ALL_EXPRESSIONS:
        print(repr(expr) + " is solvable: " + str(is_solvable(expr)))
            

if __name__ == "__main__":
    main()
