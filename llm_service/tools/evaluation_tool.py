from langchain_core.tools import tool
from sympy import sympify, SympifyError
from func_timeout import FunctionTimedOut
from evaluation.evaluation import get_entire_evaluation

pending_evaluations: dict[str, float] = {}

def reset_pending_evaluations() -> None:
    pending_evaluations.clear()


@tool
def get_entire_evaluation_tool(expression: str) -> str:
    """
    Evaluates a mathematical expression and returns its full integral evaluation suite.
    This includes the solution, solution tree, solvability score, expression depth,
    controllability score, and overall evaluation score.
    Args:
        expression (str): A string representing the mathematical expression (e.g., 'x**2 * sin(x)').
    """
    print(f"Received expression for evaluation: {expression}")
    try:
        expr = sympify(expression)
    except SympifyError as e:
        return f"Error: Could not parse expression '{expression}'. Please ensure it is valid Python/SymPy syntax. Details: {str(e)}"
    except Exception as e:
        return f"Error: Unexpected error parsing expression: {str(e)}"

    try:
        result = get_entire_evaluation(expr)
        # Record the score (last line of the result) for fallback submission
        try:
            pending_evaluations[expression] = float(result.strip().split('\n')[-1])
        except (ValueError, IndexError):
            pending_evaluations[expression] = 0.0
        return result
    except FunctionTimedOut:
        return f"Error: Evaluation of '{expression}' timed out (>30s). SymPy could not solve it in time — skip this expression."
    except Exception as e:
        return f"Error evaluating expression '{expression}': {str(e)}"
