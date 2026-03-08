from sympy import *
from sympy.abc import x
from TypstConverter import *

def write_latex_to_file(integral: Integral, filename: str) -> None:
    with open(filename, 'w') as f:
        f.write(latex(integral))

def write_latex(integral: Integral) -> None:
    write_latex_to_file(integral, 'output.tex')

def write_typst_to_file(integral: Integral, filename: str) -> None:
    converter = TypstMathConverter()
    with open(filename, 'w') as f:
        f.write('$' + converter.typst(integral) + '$')

def write_typst(integral: Integral) -> None:
    write_typst_to_file(integral, 'output.typ')

def get_integral(expr):
    integral = Integral(expr, x)
    return integral

def print_integral(expr):
    integral = get_integral(expr)
    pprint(integral)