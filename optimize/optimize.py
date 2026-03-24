"""
Random search hyperparameter optimization using randomized arrays from precomputed values

Objective: maximise the mean evaluation score across the precomputed results of 
ALL_EXPRESSIONS (all known-good integration-bee integrals).
"""
import math
from scipy.stats import norm
from sklearn.model_selection import RandomizedSearchCV
from scipy.optimize import minimize
from sklearn.base import BaseEstimator
import numpy as np
from scipy.stats import uniform, randint
from test_suite.solvability_result_vectors import SOLVABILITY_RESULT_VECTORS
from test_suite.expression_depth_data import EXPRESSION_DEPTHS
from test_suite.solvable_controllability_data import SOLVABLE_CONTROLLABILITY_SCORES

# ── bell-curve param names and (lo, hi) bounds ───────────────────────────────
BELL_PARAMS = [
    ("solv_opt",  (1,  800)),
    ("solv_dev",  (1,  250)),
    ("depth_opt", (1,  20)),
    ("depth_dev", (0.5, 10)),
    ("ctrl_opt",  (1,  70)),
    ("ctrl_dev",  (0.5, 20)),
    ("solv_weight", (0.01, 10.0)),
    ("depth_weight", (0.01, 10.0)),
    ("ctrl_weight", (0.01, 10.0)),
]

# ── rule score param names and (lo, hi) bounds ───────────────────────────────
RULE_PARAMS = [
    ("AddRule",           (0, 100)),
    ("URule",             (0, 100)),
    ("PartsRule",         (0, 150)),
    ("CyclicPartsRule",   (0, 150)),
    ("RewriteRule",       (0, 100)),
    ("ConstantTimesRule", (0, 100)),
    ("ConstantRule",      (0, 100)),
    ("PowerRule",         (0, 100)),
    ("SinRule",           (0, 100)),
    ("CosRule",           (0, 100)),
    ("TrigRule",          (0, 150)),
    ("ExpRule",           (0, 100)),
    ("ReciprocalRule",    (0, 100)),
    ("ArctanRule",        (0, 100)),
    ("AlternativeRule",   (0, 100)),
    ("DontKnowRule",      (0, 200)),
]

class IntegralEvaluator(BaseEstimator):
    def __init__(self, solv_opt=400, solv_dev=125, depth_opt=10, depth_dev=5.0, ctrl_opt=35, ctrl_dev=10,
                 solv_weight=1.0, depth_weight=1.0, ctrl_weight=1.0,
                 AddRule=50, URule=50, PartsRule=75, CyclicPartsRule=75, RewriteRule=50, ConstantTimesRule=50,
                 ConstantRule=50, PowerRule=50, SinRule=50, CosRule=50, TrigRule=75, ExpRule=50,
                 ReciprocalRule=50, ArctanRule=50, AlternativeRule=50, DontKnowRule=100):
        self.solv_opt = solv_opt
        self.solv_dev = solv_dev
        self.depth_opt = depth_opt
        self.depth_dev = depth_dev
        self.ctrl_opt = ctrl_opt
        self.ctrl_dev = ctrl_dev
        self.solv_weight = solv_weight
        self.depth_weight = depth_weight
        self.ctrl_weight = ctrl_weight
        self.AddRule = AddRule
        self.URule = URule
        self.PartsRule = PartsRule
        self.CyclicPartsRule = CyclicPartsRule
        self.RewriteRule = RewriteRule
        self.ConstantTimesRule = ConstantTimesRule
        self.ConstantRule = ConstantRule
        self.PowerRule = PowerRule
        self.SinRule = SinRule
        self.CosRule = CosRule
        self.TrigRule = TrigRule
        self.ExpRule = ExpRule
        self.ReciprocalRule = ReciprocalRule
        self.ArctanRule = ArctanRule
        self.AlternativeRule = AlternativeRule
        self.DontKnowRule = DontKnowRule

    def fit(self, X, y=None):
        return self

    def score(self, X, y=None):
        scores = []
        for i in range(len(X)):
            # If X is a DataFrame, we can extract values by name directly.
            # Convert to dictionary or series for easy column lookup:
            row = X.iloc[i]
            
            # Rule counts are stored precisely as the parameter names
            rule_weights = [getattr(self, name) for name, _ in RULE_PARAMS]
            solv_score = sum(row[name] * weight for (name, _), weight in zip(RULE_PARAMS, rule_weights))

            depth = row['depth']
            ctrl = row['controllability']

            def _bell(value: float, optimum: float, deviation: float) -> float:
                peak = norm.pdf(optimum, loc=optimum, scale=deviation)
                return norm.pdf(value, loc=optimum, scale=deviation) / peak

            norm_solv = _bell(solv_score, self.solv_opt, self.solv_dev)
            norm_depth = _bell(depth, self.depth_opt, self.depth_dev)
            norm_ctrl = _bell(ctrl, self.ctrl_opt, self.ctrl_dev)
            
            raw_score = (norm_ctrl * self.ctrl_weight) + (norm_depth * self.depth_weight) + (norm_solv * self.solv_weight)
            total_weight = self.ctrl_weight + self.depth_weight + self.solv_weight
            base_score = raw_score / total_weight if total_weight > 0 else 0.0

            is_negative = (getattr(row, "target_score", None) == 0) or (y is not None and y.iloc[i] == 0)
            if is_negative:
                # We want base_score to be as low as possible for negative examples
                scores.append(1.0 - base_score)
            else:
                # We want base_score to be as high as possible for positive examples
                scores.append(base_score)
                
        return sum(scores) / len(scores) if scores else 0.0

if __name__ == "__main__":
    
    param_distributions = {}
    for name, (lo, hi) in BELL_PARAMS:
        param_distributions[name] = uniform(loc=lo, scale=hi-lo)

    for name, (lo, hi) in RULE_PARAMS:
        param_distributions[name] = randint(low=lo, high=hi+1)

    # Use our organized DataFrame
    df = INTEGRAL_DATA.copy()
    
    # Target column extraction
    X = df.drop(columns=["target_score"])
    y = df["target_score"]

    # Train/evaluate on a randomized subset of the data
    # Select some positive and some negative examples for the subset
    np.random.seed(42)
    pos_indices = df[df["target_score"] == 1].index.values
    neg_indices = df[df["target_score"] == 0].index.values
    
    n_pos_sample = min(30, len(pos_indices))
    n_neg_sample = min(10, len(neg_indices))
    
    subset_pos = np.random.choice(pos_indices, n_pos_sample, replace=False)
    subset_neg = np.random.choice(neg_indices, n_neg_sample, replace=False)
    subset_indices = np.concatenate([subset_pos, subset_neg])
    np.random.shuffle(subset_indices)
    
    X_subset = X.iloc[subset_indices].reset_index(drop=True)
    y_subset = y.iloc[subset_indices].reset_index(drop=True)

    # Gradient Descent implementation using scipy optimize
    def objective_function(params):
        # Unpack parameters
        bell_params_vals = params[:len(BELL_PARAMS)]
        rule_params_vals = params[len(BELL_PARAMS):]
        
        kwargs = {}
        for i, (name, _) in enumerate(BELL_PARAMS):
            kwargs[name] = bell_params_vals[i]
        for i, (name, _) in enumerate(RULE_PARAMS):
            kwargs[name] = rule_params_vals[i]
            
        estimator = IntegralEvaluator(**kwargs)
        # Minimize the negative score
        return -estimator.score(X_subset, y_subset)

    # Initial guess: midpoints of bounds
    initial_guess = []
    bounds = []
    for name, (lo, hi) in BELL_PARAMS:
        initial_guess.append((lo + hi) / 2.0)
        bounds.append((lo, hi))
    for name, (lo, hi) in RULE_PARAMS:
        initial_guess.append((lo + hi) / 2.0)
        bounds.append((lo, hi))

    print("Starting optimization using L-BFGS-B (Gradient Descent)...")
    res = minimize(
        objective_function,
        initial_guess,
        method='L-BFGS-B',
        bounds=bounds,
        options={'disp': True, 'maxiter': 200}
    )

    print("Best Score:", -res.fun)
    
    print("\nBell-curve params:")
    bell_best = res.x[:len(BELL_PARAMS)]
    print(f"    bell_curve_score(solvability,     optimum={round(bell_best[0], 2)}, deviation={round(bell_best[1], 2)}), weight={round(bell_best[6], 2)}")
    print(f"    bell_curve_score(depth,           optimum={round(bell_best[2], 2)}, deviation={round(bell_best[3], 2)}), weight={round(bell_best[7], 2)}")
    print(f"    bell_curve_score(controllability, optimum={round(bell_best[4], 2)}, deviation={round(bell_best[5], 2)}), weight={round(bell_best[8], 2)}")
    
    print("\nRule score params:")
    rules_best = res.x[len(BELL_PARAMS):]
    for (name, _), val in zip(RULE_PARAMS, rules_best):
        print(f'    "{name}": {round(val)},')

