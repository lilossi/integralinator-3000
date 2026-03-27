import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score

from test_suite.integral_data import create_integral_dataframe, RULE_NAMES

def prepare_data(df: pd.DataFrame):
    """
    Prepares the feature matrix (X) and target vector (y).
    """
    # The dataframe already has RULE_NAMES expanded into columns
    feature_cols = ["ExpressionDepth", "SolvableControllabilityScore"] + RULE_NAMES
    X = df[feature_cols]
    y = df["Desirable"]
    
    return X, y

if __name__ == "__main__":
    mode = 0
    print(f"Loading data with mode {mode}...")
    df = create_integral_dataframe(mode=mode)
    
    X, y = prepare_data(df)

    # Split the dataset into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train Logistic Regression
    print("--- Logistic Regression ---")
    log_reg = LogisticRegression(max_iter=1000)
    log_reg.fit(X_train_scaled, y_train)
    
    # Predictions and evaluation
    y_pred_lr = log_reg.predict(X_test_scaled)
    print(f"Accuracy: {accuracy_score(y_test, y_pred_lr):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_lr))

    # Look at the learned feature weights to see what drives desirability
    print("\nLearned Weights (Logistic Regression Coefficients):")
    coefficients = pd.DataFrame({
        "Feature": X.columns, 
        "Weight": log_reg.coef_[0]
    }).sort_values(by="Weight", ascending=False)
    print(coefficients.to_string(index=False))
