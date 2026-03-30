from langchain_core.tools import tool
from sympy import sympify, SympifyError
from evaluation.evaluation import get_entire_evaluation

@tool
def get_entire_evaluation_tool(expression: str) -> str:
    """
    Evaluates a mathematical expression and returns its full integral evaluation suite.
    This includes the solution, solution tree, solvability score, expression depth, 
    controllability score, and overall evaluation score.
    
    Args:
        expression (str): A string representing the mathematical expression (e.g., 'x**2 * sin(x)').
    """
    try:
        # Convert the string provided by the LLM into a valid SymPy expression
        expr = sympify(expression)
    except SympifyError as e:
        return f"Error: Could not parse expression '{expression}'. Please ensure it is valid Python/SymPy syntax. Details: {str(e)}"
    except Exception as e:
        return f"Error: Unexpected error parsing expression: {str(e)}"

    try:
        result = get_entire_evaluation(expr)
    except Exception as e:
        result = f"Error evaluating expression '{expression}': {str(e)}"
        
    return result
