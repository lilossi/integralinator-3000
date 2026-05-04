from sympy import Expr, nan, zoo, oo, simplify
from sympy.abc import x
from func_timeout import func_timeout, FunctionTimedOut

def _is_valid_integrand(f: Expr) -> bool:
    """Checks if an expression is a valid integrand: must be a function of x, not constant, and free of singularities."""
    if f is None:
        return False
    if any(f.has(b) for b in (nan, zoo, oo, -oo)):
        return False
    if f.free_symbols != {x}:
        return False
    try:
        if f.is_constant():
            return False
    except Exception:
        return False
    return True


def _safe_simplify(f: Expr) -> Expr:
    """Attempts to simplify an expression, returning the original if it fails or takes too long (3 seconds)."""
    try:
        return func_timeout(3, simplify, args=(f,))
    except (Exception, FunctionTimedOut):
        return f

def clean_and_validate(expr: Expr, fallback: Expr, limit_ops:int) -> Expr:
    """Simplifies and validates an expression, returning fallback if invalid."""
    if expr.count_ops() > limit_ops:
        # might be a mistake here
        return fallback
        
    expr = _safe_simplify(expr)
    if _is_valid_integrand(expr):
        return expr
    return fallback