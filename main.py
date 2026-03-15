from sympy import *
import random
from evaluation.evaluation import print_entire_evaluation
from test_suite.test_integrals import *

def main():
    sample = random.sample(ALL_EXPRESSIONS, 30)

    for expr in sample:
        print_entire_evaluation(expr)
    
if __name__ == "__main__":
    main()
