import subprocess
import sys
import pygad
import numpy as np
import pandas as pd
import random
from sympy import Expr, preorder_traversal
from sympy.abc import x
from evaluation.controllability import get_controllability_score
from evaluation.expression_depth import get_expression_depth
from test_suite.integral_data import RULE_NAMES
from utils.tree_solution import get_solution_score, get_solution_vector
from evaluation.evaluation_score import get_evaluation_score_saved_model
from baseline_integrals.random_integrals import generate_random_function, random_expression
from func_timeout import FunctionTimedOut

POPULATION_EXPRS: list[Expr] = []

def register_expr(expr: Expr) -> int:
    """Adds an expression to the registry and returns its index."""
    POPULATION_EXPRS.append(expr)
    return len(POPULATION_EXPRS) - 1

def evaluate_expression(expr: Expr) -> float:
    """Calculates fitness by passing the expression features to the pre-trained model."""
    print(f"Evaluating: {expr}")
    try:
        return float(get_solution_score(expr))
    except FunctionTimedOut:
        return 0.0
    except Exception as e:
        return 0.0


def fitness_func(ga_instance, solution, solution_idx):
    """PyGAD delegates to this function to find fitness for a given chromosome."""
    expr_index = int(solution[0])
    expr = POPULATION_EXPRS[expr_index]
    return evaluate_expression(expr)

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

            new_sub = random_expression(n_ops=random.randint(1, 4))
            
            mutated = expr.subs(target_sub, new_sub)
            
            offspring[idx_in_offspring, 0] = register_expr(mutated)
            
    return offspring

def run_genetic_algorithm(population_size: int = 50, generations: int = 30):
    global POPULATION_EXPRS
    POPULATION_EXPRS.clear()
    
    initial_pop_indices = []
    print(f"Generating initial population of {population_size} expressions...")
    for _ in range(population_size):
        expr = generate_random_function(n_ops=7, max_attempts=10)
        if expr is None: expr = x
        idx = register_expr(expr)
        initial_pop_indices.append([idx])
        
    initial_population = np.array(initial_pop_indices)

    ga_instance = pygad.GA(
        num_generations=generations,
        num_parents_mating=population_size // 2,
        initial_population=initial_population,
        fitness_func=fitness_func,
        parent_selection_type="rws",
        parallel_processing=8, 
        crossover_type=crossover_func,
        mutation_type=mutation_func,
        keep_elitism=1
    )

    print("Starting optimization...")
    ga_instance.run()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    best_expr = POPULATION_EXPRS[int(solution[0])]
    print(f"Parameters of the best solution: {best_expr}")
    print(f"Fitness value of the best solution: {solution_fitness}")
    
    return best_expr, solution_fitness

if __name__ == "__main__":
    run_genetic_algorithm()
