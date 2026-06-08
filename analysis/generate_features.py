import sys
import time
from pathlib import Path

import pandas as pd
from sympy import Expr, sympify, Integral
from sympy.abc import x
from sympy.integrals.manualintegrate import integral_steps, manualintegrate
from func_timeout import func_set_timeout, func_timeout, FunctionTimedOut

sys.path.insert(0, str(Path(__file__).parent.parent))

from evaluation.controllability import get_symbol_count
from evaluation.evaluation_score import get_evaluation_score_saved_model
from utils.tree_solution import generate_tree, get_solution_vector_from_tree
from test_suite.integral_data import RULE_NAMES

FEATURE_COLS = ["ExpressionDepth", "SolvableControllabilityScore"] + RULE_NAMES


def parse_expr(expr_str):
    try:
        return func_timeout(5.0, sympify, args=(expr_str,))
    except Exception:
        return None


@func_set_timeout(120.0)
def get_entire_evaluation_dict(expr: Expr) -> dict:
    tree = generate_tree(repr(integral_steps(expr, x)))
    depth = tree.depth() + 1
    solution = manualintegrate(expr, x)
    rules_vector = get_solution_vector_from_tree(tree)
    rule_dict = {rule: rules_vector[i] for i, rule in enumerate(RULE_NAMES)}

    if solution.has(Integral):
        return {"status": "unsolvable", "ExpressionDepth": depth, "SolvableControllabilityScore": None, **rule_dict, "eval_score": None}
    
    control_score = get_symbol_count(solution)
    feature_df = pd.DataFrame([{"ExpressionDepth": depth, "SolvableControllabilityScore": control_score, **rule_dict}])
    eval_score = get_evaluation_score_saved_model(feature_df)

    return {"status": "ok", "ExpressionDepth": depth, "SolvableControllabilityScore": control_score, **rule_dict, "eval_score": eval_score}


def main():
    df_in   = pd.read_pickle("analysis/expressions.pkl")
    total   = len(df_in)
    results = []

    t0 = time.time()
    for i, row in enumerate(df_in.itertuples(index=False)):
        expr = parse_expr(row.expression_str)

        if expr is None:
            features = {"status": "parse_error", **{c: None for c in FEATURE_COLS}, "eval_score": None}
        else:
            try:
                features = get_entire_evaluation_dict(expr)
            except FunctionTimedOut:
                features = {"status": "timeout", **{c: None for c in FEATURE_COLS}, "eval_score": None}
            except Exception as e:
                features = {"status": f"error:{type(e).__name__}", **{c: None for c in FEATURE_COLS}, "eval_score": None}

        results.append({"algorithm": row.algorithm, "expression_str": row.expression_str, **features})

        rate = (i + 1) / (time.time() - t0)
        eta  = (total - i - 1) / rate if rate > 0 else 0
        print(f"[{i+1}/{total}] {row.algorithm} | {features['status']} | ETA {eta/60:.1f}min")

    df_out = pd.DataFrame(results)
    df_out.to_pickle("analysis/features_v2.pkl")
    df_out.to_csv("analysis/features_v2.csv", index=False)
    print(f"Saved {len(df_out)} rows.")


if __name__ == "__main__":
    main()
