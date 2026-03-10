from sympy import *
from evaluation.evaluation import print_entire_evaluation

def main():
    x = symbols('x')
    expr: Expr = sin(x) * exp(x)
    expr2: Expr = exp(x) / (1 + exp(2 * x))
    expr3: Expr = x**2 + 3*x + 2
    print_entire_evaluation(expr)
    print_entire_evaluation(expr2)
    print_entire_evaluation(expr3)
if __name__ == "__main__":
    main()
