import pygad
import numpy as np
from sympy.abc import x
from baseline_integrals.random_integrals import generate_random_function
from genetic_algorithm.ga_operators import POPULATION_EXPRS, register_expr, crossover_func, mutation_func
from genetic_algorithm.fitness import fitness_func, on_generation

def run_genetic_algorithm(population_size: int = 50, generations: int = 30):
    POPULATION_EXPRS.clear()
    
    initial_pop_indices = []
    print(f"Generating initial population of {population_size} expressions...")
    for _ in range(population_size):
        expr = generate_random_function(num_internal_ops=7, max_attempts=10)
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
        keep_elitism=1,
        on_generation=on_generation
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
