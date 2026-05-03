import random
import numpy as np
from sympy import preorder_traversal, Expr
from baseline_integrals.solvable_integrals import generate_solvable_function
from utils.validation import _safe_simplify, _is_valid_integrand
from sympy.abc import x

# Common registry for expressions to share indices across GA components
POPULATION_EXPRS: list[Expr] = []
# Registry for high-fitness expressions found during evaluation
HIGH_FITNESS_INTEGRALS: set[Expr] = set()

def register_expr(expr: Expr) -> int:
    """Adds an expression to the registry and returns its index."""
    POPULATION_EXPRS.append(expr)
    print(f"Registered new expression: {expr} (Total: {len(POPULATION_EXPRS)})")
    return len(POPULATION_EXPRS) - 1

def clean_and_validate(expr: Expr, fallback: Expr) -> Expr:
    """Simplifies and validates an expression, returning fallback if invalid."""
    expr = _safe_simplify(expr)
    if _is_valid_integrand(expr):
        return expr
    return fallback

def get_random_subtree(expr: Expr) -> Expr:
    """Extracts a random node (subtree) from the syntax tree using traversal."""
    nodes = list(preorder_traversal(expr))
    return random.choice(nodes) if nodes else expr

def crossover_func(parents, offspring_size, ga_instance):
    """
    Subtree crossover: Pick two parents, swap one's subtree with the other's.
    """
    offspring = np.empty(offspring_size, dtype=int)
    for k in range(offspring_size[0]):
        parent1_idx = int(parents[k % parents.shape[0], 0])
        parent2_idx = int(parents[(k + 1) % parents.shape[0], 0])
        
        p1_expr = POPULATION_EXPRS[parent1_idx]
        p2_expr = POPULATION_EXPRS[parent2_idx]
        
        p2_sub = get_random_subtree(p2_expr)
        p1_sub = get_random_subtree(p1_expr)
        
        child_expr = p1_expr.subs(p1_sub, p2_sub)
        child_expr = clean_and_validate(child_expr, p1_expr)
        
        offspring[k, 0] = register_expr(child_expr)

    return offspring

def mutation_func(offspring, ga_instance):
    """
    Subtree mutation: Replace a random subtree with a newly generated random leaf/expression.
    """
    mutation_rate = 0.2
    for idx_in_offspring in range(offspring.shape[0]):
        if random.random() < mutation_rate:
            expr_id = int(offspring[idx_in_offspring, 0])
            expr = POPULATION_EXPRS[expr_id]
            
            target_sub = get_random_subtree(expr)
            # Replace random_expression with generate_solvable_function to ensure solvability
            new_sub = generate_solvable_function(num_internal_ops=random.randint(1, 4), max_attempts=5)
            if new_sub is None:
                new_sub = x
            
            mutated = expr.subs(target_sub, new_sub)
            mutated = clean_and_validate(mutated, expr)
            
            offspring[idx_in_offspring, 0] = register_expr(mutated)
            
    return offspring
