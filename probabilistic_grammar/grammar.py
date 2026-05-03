from pcfg import PCFG
from sympy import SympifyError, sympify
from sympy.abc import x
from sympy import sympify

from utils.validation import _is_valid_integrand, _safe_simplify
#rules just like in baseline
grammar_string = """
S -> E [1.0]

E -> "x" [0.0357]
E -> "-5" [0.0357] | "-4" [0.0357] | "-3" [0.0357] | "-2" [0.0357] | "-1" [0.0357]
E -> "1" [0.0357]  | "2" [0.0357]  | "3" [0.0357]  | "4" [0.0357]  | "5" [0.0357]
E -> "sin("E")" [0.0357] | "cos("E")" [0.0357] | "tan("E")" [0.0357]
E -> "exp("E")" [0.0357] | "log("E")" [0.0357] | "sqrt("E")" [0.0357]
E -> "asin("E")" [0.0357] | "atan("E")" [0.0357]
E -> "sinh("E")" [0.0357] | "cosh("E")" [0.0357] | "tanh("E")" [0.0357]
E -> "-("E")" [0.0357]
E -> "("E"+"E")" [0.0357] | "("E"-"E")" [0.0357] | "("E"*"E")" [0.0357]
E -> "("E"/"E")" [0.0357] | "("E"**"E")" [0.0361]
"""

grammar = PCFG.fromstring(grammar_string)

def main():
    for sentence in grammar.generate(100):
        # PCFG automatically joins tokens with spaces, so we strip them
        #print(sentence.replace(" ", ""))
        try:
        # Convert the string provided by the LLM into a valid SymPy expression
            expr = sympify(sentence)
        except SympifyError as e:
            continue
        except Exception as e:
            continue

        expr = _safe_simplify(expr)
        if expr.free_symbols != {x} or expr.is_constant():
            continue
        if not _is_valid_integrand(expr):
            continue
        print(expr)

if __name__ == "__main__":
    main()