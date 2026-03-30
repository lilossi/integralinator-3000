from sympy import exp, pprint, Expr
from sympy.abc import x
from evaluation.evaluation import get_solution_score, print_entire_evaluation

def main():
   # ex = exp(-x**2)
   # ex = 1/(x**2 + 4)
   ex = x**3 + 2*x**2 + x + 1
   # print(get_solution_score(ex))
   print_entire_evaluation(ex)
if __name__ == "__main__":
    main()
