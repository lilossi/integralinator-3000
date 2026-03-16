"""
Random search over all hyperparameters:
  - 6 bell-curve params  (optimum + deviation for solvability, depth, controllability)
  - 16 rule score params (one integer weight per rule in points_table)

Objective: maximise the mean evaluation score across a random sample of
ALL_EXPRESSIONS (all known-good integration-bee integrals).

Usage:
    python -m evaluation.optimize              # 100 trials, 20-expr sample
    python -m evaluation.optimize --trials 200 --sample 40 --seed 7
"""
import argparse
import random
from contextlib import redirect_stdout
from io import StringIO

import utils.tree_solution as _ts
from scipy.stats import hmean, norm

from evaluation.controllability import get_controllability_score
from evaluation.expression_depth import get_expression_depth
from evaluation.solvability import solvability_score
from test_suite.test_integrals import SOLVABLE_EXPRESSIONS


# ── bell-curve param names and (lo, hi) bounds ───────────────────────────────
BELL_PARAMS = [
    ("solv_opt",  (1,  80)),
    ("solv_dev",  (1,  25)),
    ("depth_opt", (1,  20)),
    ("depth_dev", (0.5, 10)),
    ("ctrl_opt",  (1,  50)),
    ("ctrl_dev",  (0.5, 20)),
]

# ── rule score param names and (lo, hi) bounds ───────────────────────────────
# Each weight is sampled as a float and rounded to the nearest integer [lo, hi].
RULE_PARAMS = [
    ("AddRule",           (0, 10)),
    ("URule",             (0, 10)),
    ("PartsRule",         (0, 15)),
    ("CyclicPartsRule",   (0, 15)),
    ("RewriteRule",       (0, 10)),
    ("ConstantTimesRule", (0, 10)),
    ("ConstantRule",      (0, 10)),
    ("PowerRule",         (0, 10)),
    ("SinRule",           (0, 10)),
    ("CosRule",           (0, 10)),
    ("TrigRule",          (0, 15)),
    ("ExpRule",           (0, 10)),
    ("ReciprocalRule",    (0, 10)),
    ("ArctanRule",        (0, 10)),
    ("AlternativeRule",   (0, 10)),
    ("DontKnowRule",      (0, 20)),
]

ALL_PARAM_NAMES = [n for n, _ in BELL_PARAMS] + [n for n, _ in RULE_PARAMS]
ALL_BOUNDS      = [b for _, b in BELL_PARAMS] + [b for _, b in RULE_PARAMS]
N_BELL          = len(BELL_PARAMS)


def _bell(value: float, optimum: float, deviation: float) -> float:
    peak = norm.pdf(optimum, loc=optimum, scale=deviation)
    return norm.pdf(value, loc=optimum, scale=deviation) / peak


def _score_expr(expr, params: list[float]) -> float | None:
    solv_opt, solv_dev, depth_opt, depth_dev, ctrl_opt, ctrl_dev = params[:N_BELL]
    rule_values = [round(v) for v in params[N_BELL:]]

    # patch points_table for this trial
    original_table = _ts.points_table.copy()
    _ts.points_table.update(dict(zip([n for n, _ in RULE_PARAMS], rule_values)))

    try:
        with redirect_stdout(StringIO()):
            s = solvability_score(expr)
            d = get_expression_depth(expr)
            c = get_controllability_score(expr)
    finally:
        _ts.points_table.update(original_table)

    adjusted = [
        _bell(s, solv_opt, solv_dev),
        _bell(d, depth_opt, depth_dev),
        _bell(c, ctrl_opt, ctrl_dev),
    ]
    if any(v <= 0 for v in adjusted):
        return None
    try:
        return float(hmean(adjusted))
    except Exception:
        return None


def _objective(params: list[float], exprs) -> float:
    scores = [s for e in exprs if (s := _score_expr(e, params)) is not None]
    return sum(scores) / len(scores) if scores else 0.0


def random_search(n_trials: int = 100, sample_size: int = 20, seed: int = 42) -> list[float]:
    rng = random.Random(seed)
    sample = rng.sample(SOLVABLE_EXPRESSIONS, min(sample_size, len(SOLVABLE_EXPRESSIONS)))

    best_params: list[float] = []
    best_score = -1.0

    for trial in range(n_trials):
        params = [rng.uniform(lo, hi) for lo, hi in ALL_BOUNDS]
        score = _objective(params, sample)

        rounded = [round(p, 2) for p in params]
        print(f"[{trial + 1:>4}/{n_trials}]  score={score:.4f}  {dict(zip(ALL_PARAM_NAMES, rounded))}")

        if score > best_score:
            best_score = score
            best_params = params[:]
            print("           ^ new best")

    bell_best  = best_params[:N_BELL]
    rules_best = [round(v) for v in best_params[N_BELL:]]

    print("\n── Best result ─────────────────────────────────────────────")
    print(f"   score = {best_score:.4f}")
    print()
    print("Bell-curve params — paste into evaluation.py → get_evaluation_score:")
    print(f"    bell_curve_score(solvability,     optimum={round(bell_best[0], 2)}, deviation={round(bell_best[1], 2)}),")
    print(f"    bell_curve_score(depth,           optimum={round(bell_best[2], 2)}, deviation={round(bell_best[3], 2)}),")
    print(f"    bell_curve_score(controllability, optimum={round(bell_best[4], 2)}, deviation={round(bell_best[5], 2)}),")
    print()
    print("Rule score params — paste into utils/tree_solution.py → points_table:")
    for (name, _), val in zip(RULE_PARAMS, rules_best):
        print(f'    "{name}": {val},')

    return best_params


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random-search hyperparameter optimiser")
    parser.add_argument("--trials", type=int, default=100, help="number of random candidates (default 100)")
    parser.add_argument("--sample", type=int, default=20,  help="integrals evaluated per trial  (default 20)")
    parser.add_argument("--seed",   type=int, default=42,  help="RNG seed (default 42)")
    args = parser.parse_args()

    random_search(n_trials=args.trials, sample_size=args.sample, seed=args.seed)
