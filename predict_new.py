import joblib
import pandas as pd
from sympy import *
from evaluation.controllability import get_controllability_score
from evaluation.expression_depth import get_expression_depth
from evaluation.solvability import is_solvable
from test_suite.integral_data import RULE_NAMES
from utils.tree_solution import get_solution_vector

# (You will need to import your actual depth and controllability calculation functions here)
# For example: 
# from evaluation.expression_depth import get_depth
# from evaluation.controllability import get_controllability_score
# from some_file import get_solvability_vector

def predict_expression_desirability(expression: Expr) -> float:
    """
    Takes a new SymPy expression, calculates its features, and uses the 
    pretrained XGBoost model to predict if it is desirable (solvable).
    """
    # 1. Load the trained model
    # (If using Logistic Regression, you would ALSO need to load the scaler.pkl and transform the data)
    try:
        model = joblib.load("optimize/xgboost_model.pkl")
    except FileNotFoundError:
        print("Model not found! Run optimize_logistic.py first to train and save the model.")
        return False
        
    # 2. Calculate the features for this new expression
    # NOTE: You need to replace these mock functions with your actual pipeline 
    # that generates the data in test_suite/integral_data.py
    
    depth = get_expression_depth(expression)
    control_score = get_controllability_score(expression)
    rules_vector = get_solution_vector(expression) # Returns list of 16 ints
    
    # 3. Format the features into a Pandas DataFrame exactly matching the training data structure
    feature_dict = {
        "ExpressionDepth": [depth],
        "SolvableControllabilityScore": [control_score]
    }
    
    for i, rule in enumerate(RULE_NAMES):
        feature_dict[rule] = [rules_vector[i]]
        
    df_features = pd.DataFrame(feature_dict)
    
    # 4. Predict
    # model.predict returns an array of predictions (e.g., [1] or [0])
    prediction = model.predict(df_features)[0] 
    
    # Optional: Get the probability (confidence) of the prediction
    # probabilities = model.predict_proba(df_features)[0]
    # print(f"Confidence: {probabilities[1]*100:.2f}%")
    
    return model.predict_proba(df_features)[0][1]

if __name__ == "__main__":
    x = Symbol('x')
    test_expr = exp(-x**2) # Example expression; replace with any SymPy expression you want to test
    
    is_desirable = predict_expression_desirability(test_expr)
    
    print(f"Expression: {test_expr}")
    print(f"is solvable?: {is_solvable(test_expr)}", )
    print(f"Predicted Desirable: {is_desirable}")
