from sympy import *
from evaluation.solvability import solvability_score
from utils.converter_output import *
def main():
    x = symbols('x')
    expr = sin(x) * exp(x)
    expr2 = exp(x) / (1 + exp(2 * x))
    pprint(Integral(expr, x))
    print("Solvability Score:", solvability_score(Integral(expr, x)))


if __name__ == "__main__":
    main()
