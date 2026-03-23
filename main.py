from evaluation.evaluation import print_vector_evaluation
from test_suite.test_integrals import bad_integrals

def main():
   for integral in bad_integrals:
        print_vector_evaluation(integral)

if __name__ == "__main__":
    main()
