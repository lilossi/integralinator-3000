import time
from datetime import datetime
import numpy as np
from evaluation.evaluation import get_solution_score
from func_timeout import FunctionTimedOut
from sympy import Expr
from genetic_algorithm.ga_operators import POPULATION_EXPRS, HIGH_FITNESS_INTEGRALS

THRESHOLD = 0.8

# Cache expression string → score so PyGAD doesn't re-evaluate the same expr every generation.
_score_cache: dict[str, float] = {}


def evaluate_expression(expr: Expr) -> float:
    """Calculates fitness. Results are cached by expression string."""
    key = str(expr)
    if key in _score_cache:
        cached = _score_cache[key]
        print(f"[FITNESS] Cache hit: {expr} -> {cached:.4f}")
        return cached

    t0 = time.time()
    print(f"[FITNESS] Evaluating: {expr}")
    try:
        result = float(get_solution_score(expr))
        print(f"[FITNESS] Score={result:.4f} ({time.time()-t0:.2f}s)")
    except FunctionTimedOut:
        print(f"[FITNESS] Timeout ({time.time()-t0:.2f}s): {expr}")
        result = 0.0
    except Exception as e:
        print(f"[FITNESS] Exception {type(e).__name__} ({time.time()-t0:.2f}s): {expr}")
        result = 0.0

    _score_cache[key] = result
    return result


def fitness_func(ga_instance, solution, solution_idx):
    """PyGAD delegates to this function to find fitness for a given chromosome."""
    expr_index = int(solution[0])
    expr = POPULATION_EXPRS[expr_index]
    fitness = evaluate_expression(expr)

    if fitness >= THRESHOLD:
        HIGH_FITNESS_INTEGRALS.add(expr)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] High-fitness integral found: {expr} (Fitness: {fitness:.4f})")
    return fitness


def on_generation(ga_instance):
    generation = ga_instance.generations_completed
    fitnesses = ga_instance.last_generation_fitness
    if fitnesses is not None:
        avg_fitness = np.mean(fitnesses)
        cache_size = len(_score_cache)
        print(f"Generation {generation} - Average Fitness: {avg_fitness:.4f} | Cache size: {cache_size}")
