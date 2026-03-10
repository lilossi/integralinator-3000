from sympy import Expr
from sympy.abc import x
from sympy.integrals.manualintegrate import integral_steps
from utils.tree_solution import generate_tree

def get_expression_depth(expr: Expr) -> int:
    #optimization possible, not every time new generation
    tree, _ = generate_tree(repr(integral_steps(expr, x)))
    return tree.depth() + 1
