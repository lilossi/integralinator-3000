from sympy import *
from evaluation.controllability import get_controllability_score
from evaluation.evaluation import print_entire_evaluation
from test_suite.test_integrals import *
from sympy.integrals.manualintegrate import manualintegrate
from sympy.integrals.manualintegrate import integral_steps
def main():
    for integral in SOLVABLE_EXPRESSIONS:
        print(get_controllability_score(integral))

if __name__ == "__main__":
    main()
