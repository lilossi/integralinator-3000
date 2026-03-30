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
    feature_cols = ["ExpressionDepth", "SolvableControllabilityScore"] + RULE_NAMES
    X = df[feature_cols]
    y = df["Desirable"]
    
    return X, y

if __name__ == "__main__":
    df = create_integral_dataframe()
    X, y = prepare_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=44)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("--- Logistic Regression ---")
    log_reg = LogisticRegression(
        C=10.0,
        max_iter=1000,
        random_state=42
    )
    log_reg.fit(X_train_scaled, y_train)
    
    # Predictions and evaluation
    y_pred_lr = log_reg.predict(X_test_scaled)
    print(f"Accuracy: {accuracy_score(y_test, y_pred_lr):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred_lr))
    print("\nLearned Weights (Logistic Regression Coefficients):")
    coefficients = pd.DataFrame({
        "Feature": X.columns, 
        "Weight": log_reg.coef_[0]
    }).sort_values(by="Weight", ascending=False)
    print(coefficients.to_string(index=False))

    # --- XGBoost ---
    print("\n--- XGBoost (Gradient Boosted Trees) ---")
    xgb = XGBClassifier(
        n_estimators=50, 
        max_depth=2, 
        learning_rate=0.1, 
        random_state=44,
        eval_metric='logloss'
    )
    xgb.fit(X_train, y_train)
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

    print("\nSaving models to disk...")
    joblib.dump(log_reg, 'optimize/optimization_runs/saved_models/logistic_model.pkl')
    joblib.dump(scaler, 'optimize/optimization_runs/saved_models/scaler.pkl')
    joblib.dump(xgb, 'optimize/optimization_runs/saved_models/xgboost_model.pkl')