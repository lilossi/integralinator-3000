from sympy import *
import random
from evaluation.evaluation import print_entire_evaluation
from evaluation.solvability import is_solvable
from test_suite.test_integrals import *

def main():
    print_entire_evaluation(SOLVABLE_EXPRESSIONS[-1])
            

if __name__ == "__main__":
    main()
