import joblib
import pandas as pd
from sympy import *
from test_suite.integral_data import RULE_NAMES

# (You will need to import your actual depth and controllability calculation functions here)
# For example: 
# from evaluation.expression_depth import get_depth
# from evaluation.controllability import get_controllability_score
# from some_file import get_solvability_vector

def predict_expression_desirability(expression: Expr) -> bool:
    """
    Takes a new SymPy expression, calculates its features, and uses the 
    pretrained Random Forest model to predict if it is desirable (solvable).
    """
    # 1. Load the trained model
    # (If using Logistic Regression, you would ALSO need to load the scaler.pkl and transform the data)
    try:
        model = joblib.load("optimize/random_forest_model.pkl")
    except FileNotFoundError:
        print("Model not found! Run optimize_logistic.py first to train and save the model.")
        return False
        
    # 2. Calculate the features for this new expression
    # NOTE: You need to replace these mock functions with your actual pipeline 
    # that generates the data in test_suite/integral_data.py
    
    # depth = get_depth(expression)
    # control_score = get_controllability_score(expression)
    # rules_vector = get_solvability_vector(expression) # Returns list of 16 ints
    
    # -- MOCK DATA FOR DEMONSTRATION -- 
    depth = 4          
    control_score = 15      
    rules_vector = [0] * len(RULE_NAMES) 
    # ---------------------------------
    
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
    
    return bool(prediction == 1)

if __name__ == "__main__":
    x = Symbol('x')
    test_expr = sin(x) * exp(x)
    
    is_desirable = predict_expression_desirability(test_expr)
    
    print(f"Expression: {test_expr}")
    print(f"Predicted Desirable: {is_desirable}")
