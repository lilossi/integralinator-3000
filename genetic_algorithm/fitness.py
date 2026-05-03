import numpy as np
from evaluation.evaluation import get_solution_score
from func_timeout import FunctionTimedOut
from sympy import Expr
from genetic_algorithm.ga_operators import POPULATION_EXPRS, HIGH_FITNESS_INTEGRALS

THRESHOLD = 0.8 # Define a reasonable threshold

def evaluate_expression(expr: Expr) -> float:
    """Calculates fitness by passing the expression features to the pre-trained model."""
    try:
        # print(f"Evaluating: {expr}")
        return float(get_solution_score(expr))
    except FunctionTimedOut:
        print(f"Timeout: {expr}")
        return 0.0
    except ValueError:
        print(f"Value error during evaluation for: {expr}")
        return 0.0
    except Exception:
        return 0.0

def fitness_func(ga_instance, solution, solution_idx):
    """PyGAD delegates to this function to find fitness for a given chromosome."""
    expr_index = int(solution[0])
    expr = POPULATION_EXPRS[expr_index]
    fitness = evaluate_expression(expr)
    
    # Save if fitness is above threshold
     # Define a reasonable threshold
    if fitness >= THRESHOLD:
        HIGH_FITNESS_INTEGRALS.add(expr)
        print(f"High-fitness integral found: {expr} (Fitness: {fitness:.4f})")
    return fitness

def on_generation(ga_instance):
    generation = ga_instance.generations_completed
    fitnesses = ga_instance.last_generation_fitness
    if fitnesses is not None:
        avg_fitness = np.mean(fitnesses)
        print(f"Generation {generation} - Average Fitness: {avg_fitness:.4f}")
