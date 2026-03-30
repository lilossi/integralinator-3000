import joblib
import pandas as pd
from sympy import *
from evaluation.controllability import get_controllability_score
from evaluation.evaluation import get_solution_score
from evaluation.expression_depth import get_expression_depth
from evaluation.solvability import is_solvable
from test_suite.integral_data import RULE_NAMES
from utils.tree_solution import get_solution_vector


def get_evaluation_score_saved_model(df: pd.DataFrame) -> float:
    if df.empty:
        print("not solvable!")
        return 0
    try:
        model = joblib.load("optimize/optimization_runs/saved_models/xgboost_model.pkl")
    except FileNotFoundError:
        print("Model not found! Run optimize_logistic.py first to train and save the model.")
        return -1.0

    feature_cols = ["ExpressionDepth", "SolvableControllabilityScore"] + RULE_NAMES
    df_features = df[feature_cols]
    
    return model.predict_proba(df_features)[0][1]

if __name__ == "__main__":
    x = Symbol('x')
    test_expr = exp(-x**2) # Example expression; replace with any SymPy expression you want to test
    
    is_desirable = get_solution_score(test_expr)
    
    print(f"Expression: {test_expr}")
    print(f"is solvable?: {is_solvable(test_expr)}", )
    print(f"Predicted Desirable: {is_desirable}")
