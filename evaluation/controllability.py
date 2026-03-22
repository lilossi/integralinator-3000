from sympy import Expr, Symbol, preorder_traversal, pprint
from sympy.abc import x
from sympy.integrals.manualintegrate import manualintegrate
def get_symbol_count(expr: Expr) -> int:
    count = 0
    for node in preorder_traversal(expr): #returns all possible nodes
        #filter by symbol, number or function
        if isinstance(node, Symbol) or node.is_Number or node.args:
            count += 1
    return count

def get_controllability_score(expr: Expr) -> int:
    result = manualintegrate(expr, x)
    #print("Result of integration:")
    #pprint(result)
    return get_symbol_count(result)