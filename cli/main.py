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
    default=1, 
    show_default=True, 
    help='How many integrals to generate.'
)
@click.option(
    '--batch-size', 
    '-b', 
    type=int, 
    default=1, 
    show_default=True,
    help='How many to generate per batch (if that was your third parameter intent).'
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
        for i in range(num_integrals):
            click.echo(f"\n--- Generating Integral {i+1} of {num_integrals} ---")
            # Generate expressions asynchronously
            result = asyncio.run(service.generate_expression())
            click.echo(f"Result {i+1}:\n{result}")
    else:
        click.echo(f"Warning: Method '{method}' isn't fully implemented yet.")

if __name__ == '__main__':
    cli()
