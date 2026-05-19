import joblib
import pandas as pd
from sympy import *
from test_suite.integral_data import RULE_NAMES

MODEL = None

def _load_model():
    global _MODEL
    if _MODEL is None:
        try:
            _MODEL = joblib.load("optimize/optimization_runs/saved_models/xgboost_model.pkl")
        except FileNotFoundError:
            raise FileNotFoundError(
                "Model not found. Run optimize/optimize_advanced.py first to train and save the model."
            )
    return _MODEL


def get_evaluation_score_saved_model(df: pd.DataFrame) -> float:
    if df.empty:
        print("not solvable!")
        return 0.0
    try:
        model = _load_model()
    except FileNotFoundError as e:
        print(e)
        return -1.0

    feature_cols = ["ExpressionDepth", "SolvableControllabilityScore"] + RULE_NAMES
    df_features = df[feature_cols]
    
    return model.predict_proba(df_features)[0][1]
