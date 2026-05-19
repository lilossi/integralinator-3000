from __future__ import annotations

from func_timeout import func_set_timeout, FunctionTimedOut
from sympy import Expr, diff
from sympy.abc import x

from baseline_integrals.utils import random_expression
from utils.validation import _safe_simplify, _is_valid_integrand

@func_set_timeout(2.0)
def try_generate_solvable_function(
    num_internal_ops: int = 7,
    simplify_flag: bool = True,
) -> Expr | None:
    antiderivative = random_expression(num_internal_ops)
    if simplify_flag:
        antiderivative = _safe_simplify(antiderivative)
    if antiderivative.free_symbols != {x} or antiderivative.is_constant():
        return None
    integrand = diff(antiderivative, x)
    if simplify_flag:
        integrand = _safe_simplify(integrand)
    if not _is_valid_integrand(integrand):
        return None
    return integrand

def generate_solvable_function(
    num_internal_ops: int = 7,
    max_attempts: int = 50,
    simplify_flag: bool = True,
) -> Expr | None:
    for _ in range(max_attempts):
        try:
            integrand = try_generate_solvable_function(num_internal_ops, simplify_flag)
            if integrand is not None:
                return integrand
        except (FunctionTimedOut, ZeroDivisionError, ValueError, TypeError, OverflowError, RecursionError, AttributeError):
            continue
    return None