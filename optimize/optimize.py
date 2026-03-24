import numpy as np
import pandas as pd
from scipy.stats import norm, hmean
from test_suite.integral_data import create_integral_dataframe

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

def normalize_bell(value, optimum, deviation):
    peak = norm.pdf(optimum, loc=optimum, scale=deviation)
    return norm.pdf(value, loc=optimum, scale=deviation) / peak

def evaluate_params(df, params):
    #analogous to get_evaluation_score
    bell_kwargs = {name: params[i] for i, (name, _) in enumerate(BELL_PARAMS)}
    rule_kwargs = {name: params[i + len(BELL_PARAMS)] for i, (name, _) in enumerate(RULE_PARAMS)}
    scores = []
    for _, row in df.iterrows():
        rule_vector = row.get('SolvabilityResultVector', [0]*len(RULE_PARAMS))
        solv_score = sum(rule_vector[i] * rule_kwargs[name] for i, (name, _) in enumerate(RULE_PARAMS))
        
        depth = row.get('ExpressionDepth', 0)
        ctrl = row.get('SolvableControllabilityScore', 0)
        
        norm_solv = normalize_bell(solv_score, bell_kwargs['solv_opt'], bell_kwargs['solv_dev'])
        norm_depth = normalize_bell(depth, bell_kwargs['depth_opt'], bell_kwargs['depth_dev'])
        norm_ctrl = normalize_bell(ctrl, bell_kwargs['ctrl_opt'], bell_kwargs['ctrl_dev'])
        
        cmp_scores = [norm_solv, norm_depth, norm_ctrl]
        cmp_weights = [bell_kwargs['solv_weight'], bell_kwargs['depth_weight'], bell_kwargs['ctrl_weight']]

        if any(s == 0 for s in cmp_scores):
            base_score = 0.0
        else:
            base_score = hmean(cmp_scores, weights=cmp_weights)

        target = row.get('Desirable', 0)
        #L1 loss here
        scores.append(abs(target - base_score))
            
    return sum(scores) / len(scores) if scores else 0.0

def random_search(df, num_iterations=1000):
    best_loss = float('inf')
    best_params = None
    print(f"Starting Random Search for {num_iterations} iterations...")
    for i in range(num_iterations):
        current_params = []
        for name, (lo, hi) in BELL_PARAMS:
            current_params.append(np.random.uniform(lo, hi))
        for name, (lo, hi) in RULE_PARAMS:
            current_params.append(np.random.randint(lo, hi + 1))
            
        loss = evaluate_params(df, current_params)
        
        if loss < best_loss:
            best_loss = loss
            best_params = current_params
            print(f"Iteration {i}: New best loss: {best_loss:.4f}")
            
    return best_params, best_loss

if __name__ == "__main__":
    mode = 0
    num_iterations=200000
    df = create_integral_dataframe(mode=mode)
    
    best_params, best_loss = random_search(df, num_iterations=num_iterations)
    
    print("\noptimization finished!")
    print(f"Best Loss: {best_loss:.4f}")
    print("mode", mode)
    print("Number of iterations:", num_iterations)
    print("\nBest Bell-curve params:")
    bell_best = best_params[:len(BELL_PARAMS)]
    print(f"    bell_curve_score(solvability,     optimum={round(bell_best[0], 2)}, deviation={round(bell_best[1], 2)}), weight={round(bell_best[6], 2)}")
    print(f"    bell_curve_score(depth,           optimum={round(bell_best[2], 2)}, deviation={round(bell_best[3], 2)}), weight={round(bell_best[7], 2)}")
    print(f"    bell_curve_score(controllability, optimum={round(bell_best[4], 2)}, deviation={round(bell_best[5], 2)}), weight={round(bell_best[8], 2)}")
    
    print("\nBest Rule score params:")
    rules_best = best_params[len(BELL_PARAMS):]
    for (name, _), val in zip(RULE_PARAMS, rules_best):
        print(f'    "{name}": {round(val)},')
