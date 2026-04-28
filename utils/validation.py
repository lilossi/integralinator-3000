from sympy import Expr, nan, zoo, oo, simplify
from sympy.abc import x

def _is_valid_integrand(f: Expr) -> bool:
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
    try:
        return simplify(f)
    except Exception:
        return f