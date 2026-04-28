# 'Deep Learning for Symbolic Mathematics' Lample & Charton (2019)

from __future__ import annotations

import random
from functools import lru_cache

from sympy import Expr, Integer
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
def _build_tree_counts_table(max_internal_ops: int) -> tuple[tuple[int, ...], ...]:
    """
    tree_counts[open_leaf_slots][remaining_internal_ops] = number of tree skeletons
    with open_leaf_slots open leaf-slots and remaining_internal_ops
    internal operators remaining to place.

    Recurrence:
        tree_counts[open_leaf_slots][remaining_internal_ops] = 
        tree_counts[open_leaf_slots-1][remaining_internal_ops]  (leaf)
        +  tree_counts[open_leaf_slots][remaining_internal_ops-1]  (unary op)
        +  tree_counts[open_leaf_slots+1][remaining_internal_ops-1]  (binary op)


    Boundary: tree_counts[open_leaf_slots][0] = 1 for all open_leaf_slots >= 0; 
        tree_counts[0][remaining_internal_ops] = 0 for remaining_internal_ops > 0.
    """
    max_open_slots = 2 * max_internal_ops + 2
    tree_counts = [[0] * (max_internal_ops + 1) for _ in range(max_open_slots + 1)]
    for open_leaf_slots in range(max_open_slots + 1):
        tree_counts[open_leaf_slots][0] = 1
    for remaining_internal_ops in range(1, max_internal_ops + 1):
        for open_leaf_slots in range(1, max_open_slots):
            tree_counts[open_leaf_slots][remaining_internal_ops] = tree_counts[open_leaf_slots - 1][remaining_internal_ops] + tree_counts[open_leaf_slots][remaining_internal_ops - 1] + tree_counts[open_leaf_slots + 1][remaining_internal_ops - 1]
    return tuple(tuple(row) for row in tree_counts)


def _sample_tree_arity_sequence(num_internal_ops: int) -> list[int]:
    """
    Sample a tree shape uniformly at random among all trees with exactly
    `num_internal_ops` internal nodes. Returns a pre-order list of arities:
        0 = leaf, 1 = unary op, 2 = binary op.
    """
    tree_counts = _build_tree_counts_table(num_internal_ops)
    arity_sequence: list[int] = []
    open_leaf_slots, remaining_internal_ops = 1, num_internal_ops
    while open_leaf_slots > 0:
        if remaining_internal_ops == 0: # no ops left -> fill with leaves
            arity_sequence.extend([0] * open_leaf_slots)
            break
        weight_leaf   = tree_counts[open_leaf_slots - 1][remaining_internal_ops]
        weight_unary  = tree_counts[open_leaf_slots][remaining_internal_ops - 1]
        weight_binary = tree_counts[open_leaf_slots + 1][remaining_internal_ops - 1]
        rand_val = random.random() * (weight_leaf + weight_unary + weight_binary)
        if rand_val < weight_leaf:
            arity_sequence.append(0); open_leaf_slots -= 1
        elif rand_val < weight_leaf + weight_unary:
            arity_sequence.append(1); remaining_internal_ops -= 1 # e unchanged (1 slot -> 1 slot)
        else:
            arity_sequence.append(2); remaining_internal_ops -= 1; open_leaf_slots += 1 # 1 slot -> 2 slots
    return arity_sequence


def _build_expr(arity_sequence: list[int]) -> Expr:
    """Decorate a pre-order arity sequence with random ops and leaves."""
    iterator = iter(arity_sequence)

    def build_subtree() -> Expr:
        arity = next(iterator)
        if arity == 0:
            return _random_leaf()
        elif arity == 1:
            return random.choice(UNARY_OPS)(build_subtree())
        else:
            left_child, right_child = build_subtree(), build_subtree()
            return random.choice(BINARY_OPS)(left_child, right_child)

    return build_subtree()


def random_expression(num_internal_ops: int) -> Expr:
    """Random SymPy expression in x with exactly `num_internal_ops` internal nodes."""
    return _build_expr(_sample_tree_arity_sequence(num_internal_ops))