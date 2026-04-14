import click
import asyncio
from llm_service.llm_service import llm_service

@click.group()
def cli():
    """Integralinator-3000 Command Line Interface."""
    pass

@cli.command()
@click.option(
    '--method', 
    '-m', 
    type=str, 
    required=True, 
    help='Which method should be used.'
)
@click.option(
    '--num-integrals', 
    '-n', 
    type=int, 
    default=100, 
    show_default=True, 
    help='How many integrals to generate.'
)
@click.option(
    '--batch-size', 
    '-b', 
    type=int, 
    default=10, 
    show_default=True,
    help='How many to generate.'
)
def generate(method, num_integrals, batch_size):
    """Generate integrals using the specific method."""
    click.echo(f"Initializing generation process...")
    click.echo(f"Method: {method}")
    click.echo(f"Total Integrals: {num_integrals}")
    click.echo(f"Batch Size: {batch_size}")
    
    if method.lower() == 'llm':
        service = llm_service()
        click.echo("LLM Service initialized.")
        click.echo(f"Generating {num_integrals} integrals in batches of {batch_size}...")
        
        all_results = []
        while len(all_results) < num_integrals:
            current_batch = min(batch_size, num_integrals - len(all_results))
            click.echo(f"Requesting batch of {current_batch} integrals from LLM...")
            results = asyncio.run(service.generate_expression(current_batch))

            valid_results = [r for r in results if not r.startswith("Failed to extract JSON")]
            
            if not valid_results and results:
                click.echo("Failed to generate a valid batch, retrying...")
                continue
                
            all_results.extend(valid_results)

            all_results = all_results[:num_integrals]
        
        click.echo("\n--- Final Curated Expressions ---")
        for i, expr in enumerate(all_results, 1):
            click.echo(f"[{i}] {expr}")
    else:
        click.echo(f"Warning: Method '{method}' isn't fully implemented yet.")

if __name__ == '__main__':
    cli()
