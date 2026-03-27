import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import joblib

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
    log_reg = LogisticRegression(max_iter=10000)
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

    # --- Random Forest ---
    print("\n--- Random Forest (Non-Linear) ---")
    rf = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=10)
    rf.fit(X_train, y_train) # Random Forest doesn't need scaled data
    
    y_pred_rf = rf.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred_rf):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_rf))
    print("\nFeature Importances (Random Forest):")
    importances = pd.DataFrame({
        "Feature": X.columns, 
        "Importance": rf.feature_importances_
    }).sort_values(by="Importance", ascending=False)
    print(importances.to_string(index=False))

    # --- XGBoost ---
    print("\n--- XGBoost (Gradient Boosted Trees) ---")
    xgb = XGBClassifier(
        n_estimators=200, 
        max_depth=6, 
        learning_rate=0.1, 
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    xgb.fit(X_train, y_train) # Also doesn't strictly need scaled data
    
    y_pred_xgb = xgb.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred_xgb):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_xgb))
    
    print("\nFeature Importances (XGBoost):")
    xgb_importances = pd.DataFrame({
        "Feature": X.columns, 
        "Importance": xgb.feature_importances_
    }).sort_values(by="Importance", ascending=False)
    print(xgb_importances.to_string(index=False))

    # --- Save the best model and scaler ---
    # We save both the model and the scaler because any new data must be 
    # scaled exactly the same way the training data was before making a prediction.
    print("\nSaving models to disk...")
    joblib.dump(log_reg, 'optimize/logistic_model.pkl')
    joblib.dump(rf, 'optimize/random_forest_model.pkl')
    joblib.dump(xgb, 'optimize/xgboost_model.pkl')
    joblib.dump(scaler, 'optimize/scaler.pkl')
    print("Saved as .pkl files in the optimize/ directory!")
