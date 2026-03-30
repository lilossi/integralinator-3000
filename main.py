from sympy import exp, pprint, Expr
from sympy.abc import x
from evaluation.evaluation import get_solution_score

def main():
   # ex = exp(-x**2)
   # ex = 1/(x**2 + 4)
   ex = x**3 + 2*x**2 + x + 1
   print(get_solution_score(ex))

if __name__ == "__main__":
    main()
