# 'Deep Learning for Symbolic Mathematics' Lample & Charton (2019)


from __future__ import annotations

import random
import threading
import _thread
from contextlib import contextmanager
from functools import lru_cache

from sympy import Expr, Integer, Integral, nan, oo, zoo, diff, simplify
from sympy.abc import x
from sympy import sin, cos, tan, exp, log, sqrt, asin, atan, sinh, cosh, tanh

# alphabet for the trees: unary ops, binary ops, and leaves (x and small ints).
UNARY_OPS = [
    sin, cos, tan,
    exp, log, sqrt,
    asin, atan,
    sinh, cosh, tanh,
    lambda u: -u, #unary negation
]

def _add(a, b): return a + b
def _sub(a, b): return a - b
def _mul(a, b): return a * b
def _div(a, b): return a / b
def _pow(a, b): return a ** b

BINARY_OPS = [_add, _sub, _mul, _div, _pow]

INT_LEAVES = [i for i in range(-5, 6) if i != 0]


def _random_leaf(p_var: float = 0.5) -> Expr:
    """Leaf is the variable x with prob p_var, otherwise a small nonzero int."""
    if random.random() < p_var:
        return x
    return Integer(random.choice(INT_LEAVES))


@lru_cache(maxsize=None)
def _build_D(max_n: int) -> tuple[tuple[int, ...], ...]:
    """
    D[e][n] = number of tree skeletons with e open leaf-slots and n
    internal operators remaining to place.

    Recurrence:
        D[e][n] = D[e-1][n]  +  D[e][n-1]  +  D[e+1][n-1]
                  └ leaf ┘    └ unary op ┘    └ binary op ┘

    Boundary: D[e][0] = 1 for all e >= 0; D[0][n] = 0 for n > 0.
    """
    max_e = 2 * max_n + 2
    D = [[0] * (max_n + 1) for _ in range(max_e + 1)]
    for e in range(max_e + 1):
        D[e][0] = 1
    for n in range(1, max_n + 1):
        for e in range(1, max_e):
            D[e][n] = D[e - 1][n] + D[e][n - 1] + D[e + 1][n - 1]
    return tuple(tuple(row) for row in D)


def _sample_shape(n_ops: int) -> list[int]:
    """
    Sample a tree shape uniformly at random among all trees with exactly
    `n_ops` internal nodes. Returns a pre-order list of arities:
        0 = leaf, 1 = unary op, 2 = binary op.
    """
    D = _build_D(n_ops)
    shape: list[int] = []
    e, n = 1, n_ops
    while e > 0:
        if n == 0: # no ops left -> fill with leaves
            shape.extend([0] * e)
            break
        w_leaf   = D[e - 1][n]
        w_unary  = D[e][n - 1]
        w_binary = D[e + 1][n - 1]
        r = random.random() * (w_leaf + w_unary + w_binary)
        if r < w_leaf:
            shape.append(0); e -= 1
        elif r < w_leaf + w_unary:
            shape.append(1); n -= 1 # e unchanged (1 slot -> 1 slot)
        else:
            shape.append(2); n -= 1; e += 1 # 1 slot -> 2 slots
    return shape


def _build_expr(shape: list[int]) -> Expr:
    """Decorate a pre-order arity sequence with random ops and leaves."""
    it = iter(shape)

    def rec() -> Expr:
        a = next(it)
        if a == 0:
            return _random_leaf()
        elif a == 1:
            return random.choice(UNARY_OPS)(rec())
        else:  # a == 2
            left, right = rec(), rec()
            return random.choice(BINARY_OPS)(left, right)

    return rec()


def random_expression(n_ops: int) -> Expr:
    """Random SymPy expression in x with exactly `n_ops` internal nodes."""
    return _build_expr(_sample_shape(n_ops))

class _Timeout(Exception):
    #print("Timeout!")
    pass


@contextmanager
def _time_limit(seconds: float):
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise _Timeout()
    finally:
        timer.cancel()

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


def _safe_simplify(f: Expr, timeout: float) -> Expr:
    try:
        with _time_limit(timeout):
            return simplify(f)
    except Exception:
        return f


def generate_random_function(
    n_ops: int = 7,
    max_attempts: int = 50,
    simplify_flag: bool = True,
    timeout: float = 2.0,
) -> Expr | None:
    for _ in range(max_attempts):
        try:
            with _time_limit(timeout):
                f = random_expression(n_ops)
                if simplify_flag:
                    f = _safe_simplify(f, timeout=timeout / 2)
                if not _is_valid_integrand(f):
                    continue
                return f
        except (_Timeout, ZeroDivisionError, ValueError,
                TypeError, OverflowError, RecursionError):
            continue
    return None


def generate_solvable_function(
    n_ops: int = 7,
    max_attempts: int = 50,
    simplify_flag: bool = True,
    timeout: float = 2.0,
) -> Expr | None:
    for _ in range(max_attempts):
        try:
            with _time_limit(timeout):
                F = random_expression(n_ops)
                if simplify_flag:
                    F = _safe_simplify(F, timeout=timeout / 2)
                if F.free_symbols != {x} or F.is_constant():
                    continue
                f = diff(F, x)
                if simplify_flag:
                    f = _safe_simplify(f, timeout=timeout / 2)
                if not _is_valid_integrand(f):
                    continue
                return f
        except (_Timeout, ZeroDivisionError, ValueError,
                TypeError, OverflowError, RecursionError):
            continue
    return None
