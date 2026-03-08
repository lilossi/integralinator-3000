from sympy import *
from utils.converter_output import *
def main():
    x = symbols('x')
    expr = sin(x) * exp(x)
    integral = Integral(expr, x)
    write_typst(integral)


if __name__ == "__main__":
    main()
