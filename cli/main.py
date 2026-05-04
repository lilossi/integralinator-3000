import click
import asyncio
from baseline_integrals.random_integrals import generate_random_function
from baseline_integrals.solvable_integrals import generate_solvable_function
from genetic_algorithm.genetic_algorithm import run_genetic_algorithm
from llm_service.llm_service import llm_service
from probabilistic_grammar.grammar import generate_valid_expressions

@click.group()
def cli():
    """Integralinator-3000 CLI"""
    pass

@cli.command()
@click.option(
    '--method', 
    '-m', 
    type=str, 
    required=True, 
    help='Which method should be used. Examples: llm, ...'
)
@click.option(
    '--num-integrals', 
    '-n', 
    type=int, 
    default=10, 
    show_default=True, 
    help='How many integrals to generate.'
)
def generate(method, num_integrals):
    """Generate integrals using the specific method."""
    click.echo(f"Initializing generation process...")
    click.echo(f"Method: {method}")
    click.echo(f"Total Integrals: {num_integrals}")
    
    if method.lower() == 'llm':
        # uv run -m cli.main generate --method llm --num-integrals 5
        service = llm_service()
        click.echo("LLM Service initialized.")
        click.echo(f"Generating {num_integrals} integrals...")
        
        results = asyncio.run(service.generate_expression(num_integrals))
        
        click.echo("\n--- Final Curated Expressions ---")
        for i, expr in enumerate(results, 1):
            click.echo(f"[{i}] {expr}")

    elif method.lower() == 'baseline':
        # uv run -m cli.main generate --method baseline --num-integrals 5
        click.echo("Baseline initialized.")
        click.echo(f"Generating {num_integrals} integrals...")
        for i in range(1, num_integrals + 1):
            click.echo(f"[{i}] {generate_random_function(num_internal_ops=7)}")

    elif method.lower() == 'baseline_solvable':
        # uv run -m cli.main generate --method baseline_solvable --num-integrals 5
        click.echo("Baseline Solvable initialized.")
        click.echo(f"Generating {num_integrals} integrals...")
        for i in range(1, num_integrals + 1):
            F = generate_solvable_function(num_internal_ops=6)
            if F is None:
                continue
            click.echo(f"[{i}] {F}")
    elif method.lower() == 'genetic':
        # uv run -m cli.main generate --method genetic --num-integrals 1
        click.echo("Genetic Algorithm initialized.")
        click.echo("Running Genetic Algorithm to collect high-fitness expressions...")
        
        all_collected_integrals = []
        for i in range(1, num_integrals + 1):
            click.echo(f"Run {i}/{num_integrals}...")
            collected = run_genetic_algorithm(population_size=20, generations=10)
            all_collected_integrals.extend(collected)
        
        unique_integrals = list(set(all_collected_integrals))
        
        click.echo("\n--- Collected High-Fitness Expressions ---")
        for i, expr in enumerate(unique_integrals, 1):
            click.echo(f"[{i}] {expr}")
    elif method.lower() == 'grammar':
        # uv run -m cli.main generate --method grammar --num-integrals 5
        click.echo("Probabilistic Grammar initialized.")
        click.echo(f"Generating {num_integrals} integrals...")
        
        expressions = generate_valid_expressions(num_integrals)
        
        click.echo("\n--- Final Valid Expressions ---")
        for i, expr in enumerate(expressions, 1):
            click.echo(f"[{i}] {expr}")
    else:
        click.echo(f"Warning: Method '{method}' isn't fully implemented yet.")

if __name__ == '__main__':
    cli()
