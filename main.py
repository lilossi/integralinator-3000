from evaluation.evaluation import print_vector_evaluation
from test_suite.integral_data import create_integral_dataframe
from test_suite.test_integrals import bad_integrals

def main():
   df = create_integral_dataframe()
   print(df.head(-5))
   df.head()

if __name__ == "__main__":
    main()
