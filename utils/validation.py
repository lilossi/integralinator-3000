import time
from sympy import I, Expr, nan, zoo, oo, simplify, sympify, SympifyError
from sympy.abc import x
from func_timeout import func_timeout, func_set_timeout, FunctionTimedOut

def _is_valid_integrand(f: Expr) -> bool:
    """Checks if an expression is a valid integrand: must be a function of x, not constant, and free of singularities."""
    if f is None:
        return False
    if any(f.has(b) for b in (nan, zoo, oo, -oo, I, -I)):
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
    t0 = time.time()
    print(f"    [SIMPLIFY] start: {f}")
    try:
        result = func_timeout(3, simplify, args=(f,))
        print(f"    [SIMPLIFY] done ({time.time()-t0:.2f}s) -> {result}")
        return result
    except FunctionTimedOut:
        print(f"    [SIMPLIFY] timed out ({time.time()-t0:.2f}s)")
        return f
    except Exception as e:
        print(f"    [SIMPLIFY] exception {type(e).__name__} ({time.time()-t0:.2f}s): {e}")
        return f

@func_set_timeout(18.0)
def clean_and_validate(expr: Expr, fallback: Expr, limit_ops: int, use_safe_simplify: bool = False) -> Expr:
    """Simplifies and validates an expression, returning fallback if invalid."""
    if expr.count_ops() > limit_ops:
        return fallback

    if use_safe_simplify:
        expr = _safe_simplify(expr)
    if _is_valid_integrand(expr):
        return expr
    return fallback

def process_string_to_expression(sentence: str) -> Expr:
    """Converts a generated string into a validated SymPy expression.
    Currently only used in the probabilistic grammar module, but could be reused elsewhere."""
    if len(sentence) > 100:
        #print(f"Skipping overly long sentence: {sentence}")
        return None
    try:
        expr = func_timeout(2.0, sympify, args=(sentence,))
        valid_expr = clean_and_validate(expr, None, 50, use_safe_simplify=False)
    except (SympifyError, FunctionTimedOut, Exception) as e:
        #print(f"SympifyError for '{sentence}': {e}")
        return None
    except Exception as e:
        #print(f"Unexpected error for '{sentence}': {e}")
        return None
    
    if valid_expr is None:
        #print(f"Invalid expression (failed validation): {expr}")
        return None
    
    return valid_expr