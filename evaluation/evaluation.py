import pandas as pd
from sympy import Expr, Integral, pretty
from sympy.abc import x
from sympy.integrals.manualintegrate import integral_steps, manualintegrate
from evaluation.controllability import get_symbol_count
from evaluation.evaluation_score import get_evaluation_score_saved_model
from test_suite.integral_data import RULE_NAMES
from utils.tree_solution import get_solution_vector_from_tree, generate_tree
from func_timeout import FunctionTimedOut, func_set_timeout

# IMPORTANT!!!! >.<
def return_vector_evaluation(expr: Expr) -> pd.DataFrame:
    tree = generate_tree(repr(integral_steps(expr, x)))
    depth = tree.depth() + 1
    solution = manualintegrate(expr, x)
    control_score = get_symbol_count(solution)
    rules_vector = get_solution_vector_from_tree(tree)
    
    if (rules_vector[-1] > 0):
        return pd.DataFrame()

    temp_dict = {
        "ExpressionDepth": [depth],
        "SolvableControllabilityScore": [control_score]
    }
    
    for i, rule in enumerate(RULE_NAMES):
        temp_dict[rule] = [rules_vector[i]]
        
    vector = pd.DataFrame(temp_dict)
    return vector

# also important
def get_entire_evaluation(expr: Expr) -> str:
    """
    Returns the entire evaluation suite (solution, tree, scores) as a formatted string.
    """
    tree = generate_tree(repr(integral_steps(expr, x)))
    depth = tree.depth() + 1
    solution = manualintegrate(expr, x)
    control_score = get_symbol_count(solution)
    rules_vector = get_solution_vector_from_tree(tree)
    
    temp_dict = {
        "ExpressionDepth": [depth],
        "SolvableControllabilityScore": [control_score]
    }
    
    for i, rule in enumerate(RULE_NAMES):
        temp_dict[rule] = [rules_vector[i]]
        
    vector = pd.DataFrame(temp_dict)
    if (rules_vector[-1] > 0):
        vector = pd.DataFrame()
    return f"""Expression:
{pretty(Integral(expr, x))}
Solution:
{solution}

Solution Tree:
{str(tree.show(stdout=False)).strip()}

Max Depth:
{depth}
Controllability Score:
{control_score}
Solution Rule Vector:
{rules_vector}

Overall Evaluation Score (using xgboost):
{get_evaluation_score_saved_model(vector)}"""

@func_set_timeout(5)
def get_solution_score(expr: Expr) -> float:
    try:
        vector = return_vector_evaluation(expr)
        if vector.empty:
            return 0.0
        return get_evaluation_score_saved_model(vector)
    except FunctionTimedOut:
        return 0.0
    except Exception:
        return 0.0