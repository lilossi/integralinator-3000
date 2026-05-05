import pygad
import numpy as np
from probabilistic_grammar.trainable_grammar import TrainableGrammar
from evaluation.evaluation import get_solution_score
from func_timeout.exceptions import FunctionTimedOut

def fitness_func(ga_instance, solution, solution_idx):
    grammar = TrainableGrammar(initial_weights=solution)
    
    try:
        generated_exprs = grammar.generate_valid_expressions(num_expressions=5) # small, quick batch to evaluate fitness
    except Exception as e:
        return 0.0
        
    if not generated_exprs:
        return 0.0

    scores = []
    for expr in generated_exprs:
        try:
            score = float(get_solution_score(expr))
            scores.append(score if score > 0 else 0)
        except FunctionTimedOut:
            scores.append(0.0)
        except Exception:
            scores.append(0.0)

    return float(np.mean(scores))

def main():
    num_genes = 28 # = rules in TrainableGrammar
    
    print("Starting grammar training with PyGAD...")
    ga_instance = pygad.GA(
        num_generations=20,
        num_parents_mating=5,
        fitness_func=fitness_func,
        sol_per_pop=10,
        num_genes=num_genes,
        init_range_low=-2.0,
        init_range_high=2.0,
        mutation_percent_genes=20,
        mutation_type="random",
        #parallel_processing=8,
        parent_selection_type="rws"
    )

    ga_instance.run()

    best_solution, best_solution_fitness, _ = ga_instance.best_solution()
    
    print("\n--- Training Complete ---")
    print(f"Best Fitness Score: {best_solution_fitness}")
    print(f"Best Weights: \n{list(best_solution)}")
    
    best_grammar = TrainableGrammar(initial_weights=best_solution)
    print("\nBest Learned PCFG probabilities:")
    print(best_grammar.get_grammar_string())

if __name__ == "__main__":
    main()
