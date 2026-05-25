import random
import time
import numpy as np
from sympy import preorder_traversal, Expr
from baseline_integrals.solvable_integrals import generate_solvable_function
from utils.validation import clean_and_validate
from func_timeout import FunctionTimedOut
from sympy.abc import x

POPULATION_EXPRS: list[Expr] = []
HIGH_FITNESS_INTEGRALS: set[Expr] = set()
LIMIT_OPS = 50

def register_expr(expr: Expr) -> int:
    """Adds an expression to the registry and returns its index."""
    POPULATION_EXPRS.append(expr)
    print(f"Registered new expression: {expr} (Total: {len(POPULATION_EXPRS)})")
    return len(POPULATION_EXPRS) - 1

def get_random_subtree_from_parent(expr: Expr) -> Expr:
    """Extracts a random node (subtree) from the syntax tree using traversal."""
    nodes = list(preorder_traversal(expr))
    return random.choice(nodes) if nodes else expr

def crossover_func(parents, offspring_size, ga_instance):
    """
    Subtree crossover: Pick two parents, swap one's subtree with the other's.
    """
    gen = ga_instance.generations_completed
    print(f"[CROSSOVER] gen={gen}, making {offspring_size[0]} offspring, registry size={len(POPULATION_EXPRS)}")
    offspring = np.empty(offspring_size, dtype=int)
    for k in range(offspring_size[0]):
        parent1_idx = int(parents[k % parents.shape[0], 0])
        parent2_idx = int(parents[(k + 1) % parents.shape[0], 0])
        
        p1_expr = POPULATION_EXPRS[parent1_idx]
        p2_expr = POPULATION_EXPRS[parent2_idx]
        
        p2_sub = get_random_subtree_from_parent(p2_expr)
        p1_sub = get_random_subtree_from_parent(p1_expr)

        t0 = time.time()
        print(f"  [CROSSOVER {k}] subs start: p1={p1_expr}, p1_sub={p1_sub}, p2_sub={p2_sub}")
        child_expr = p1_expr.subs(p1_sub, p2_sub)
        print(f"  [CROSSOVER {k}] subs done ({time.time()-t0:.2f}s) -> {child_expr}")

        t1 = time.time()
        print(f"  [CROSSOVER {k}] clean_and_validate start")
        try:
            child_expr = clean_and_validate(child_expr, p1_expr, LIMIT_OPS, False)
            print(f"  [CROSSOVER {k}] clean_and_validate done ({time.time()-t1:.2f}s) -> {child_expr}")
        except FunctionTimedOut:
            print(f"  [CROSSOVER {k}] clean_and_validate TIMEOUT ({time.time()-t1:.2f}s) — using fallback")
            child_expr = p1_expr
        offspring[k, 0] = register_expr(child_expr)

    return offspring

def mutation_func(offspring, ga_instance):
    """
    Subtree mutation: Replace a random subtree with a newly generated random leaf/expression.
    """
    gen = ga_instance.generations_completed
    print(f"[MUTATION] gen={gen}, registry size={len(POPULATION_EXPRS)}")
    mutation_rate = 0.2
    for idx_in_offspring in range(offspring.shape[0]):
        if random.random() < mutation_rate:
            expr_id = int(offspring[idx_in_offspring, 0])
            expr = POPULATION_EXPRS[expr_id]

            target_sub = get_random_subtree_from_parent(expr)
            new_sub = generate_solvable_function(num_internal_ops=random.randint(1, 4), max_attempts=5)
            if new_sub is None:
                new_sub = x

            t0 = time.time()
            print(f"  [MUTATION {idx_in_offspring}] subs start: expr={expr}, target={target_sub}, new={new_sub}")
            mutated = expr.subs(target_sub, new_sub)
            print(f"  [MUTATION {idx_in_offspring}] subs done ({time.time()-t0:.2f}s) -> {mutated}")

            t1 = time.time()
            print(f"  [MUTATION {idx_in_offspring}] clean_and_validate start")
            try:
                mutated = clean_and_validate(mutated, expr, LIMIT_OPS, False)
                print(f"  [MUTATION {idx_in_offspring}] clean_and_validate done ({time.time()-t1:.2f}s) -> {mutated}")
            except FunctionTimedOut:
                print(f"  [MUTATION {idx_in_offspring}] clean_and_validate TIMEOUT ({time.time()-t1:.2f}s) — using fallback")
                mutated = expr

            offspring[idx_in_offspring, 0] = register_expr(mutated)

    return offspring
