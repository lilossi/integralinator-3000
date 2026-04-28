import joblib
import pandas as pd
from sympy import *
from test_suite.integral_data import RULE_NAMES


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
