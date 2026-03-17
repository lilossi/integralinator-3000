"""
Random search over all hyperparameters:
  - 6 bell-curve params  (optimum + deviation for solvability, depth, controllability)
  - 16 rule score params (one integer weight per rule in points_table)

Objective: maximise the mean evaluation score across a random sample of
ALL_EXPRESSIONS (all known-good integration-bee integrals).

Usage:
    python -m evaluation.optimize              # 100 trials, 20-expr sample
    python -m evaluation.optimize --trials 200 --sample 40 --seed 7
    python -m evaluation.optimize --overnight  # 3 long runs, logs to text files
"""
import argparse
import random
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import utils.tree_solution as _ts
from scipy.stats import hmean, norm

from evaluation.controllability import get_controllability_score
from evaluation.expression_depth import get_expression_depth
from evaluation.solvability import solvability_score
from test_suite import test_integrals as _ti
from test_suite.test_integrals import SOLVABLE_EXPRESSIONS


# ── bell-curve param names and (lo, hi) bounds ───────────────────────────────
BELL_PARAMS = [
    ("solv_opt",  (1,  800)),
    ("solv_dev",  (1,  250)),
    ("depth_opt", (1,  20)),
    ("depth_dev", (0.5, 10)),
    ("ctrl_opt",  (1,  70)),
    ("ctrl_dev",  (0.5, 20)),
]

# ── rule score param names and (lo, hi) bounds ───────────────────────────────
# Each weight is sampled as a float and rounded to the nearest integer [lo, hi].
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


def random_search(
    n_trials: int = 100,
    sample_size: int | None = 20,
    seed: int = 42,
    expression_pool: list | None = None,
) -> list[float]:
    rng = random.Random(seed)
    pool = expression_pool if expression_pool is not None else SOLVABLE_EXPRESSIONS
    if not pool:
        raise ValueError("expression_pool must contain at least one expression")

    if sample_size is None:
        sample = list(pool)
    else:
        sample = rng.sample(pool, min(sample_size, len(pool)))

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


def _collect_solvable_pools() -> tuple[list, list]:
    chapter_1_exprs = []
    chapter_2_plus_exprs = []

    for name, value in vars(_ti).items():
        if not name.startswith("chapter_") or not isinstance(value, list):
            continue

        parts = name.split("_")
        if len(parts) != 3:
            continue

        try:
            chapter_no = int(parts[1])
        except ValueError:
            continue

        if chapter_no == 1:
            chapter_1_exprs.extend(value)
        elif chapter_no >= 2:
            chapter_2_plus_exprs.extend(value)

    chapter_1_set = set(chapter_1_exprs)
    chapter_2_plus_set = set(chapter_2_plus_exprs)

    solvable_chapter_1 = [expr for expr in SOLVABLE_EXPRESSIONS if expr in chapter_1_set]
    solvable_chapter_2_plus = [expr for expr in SOLVABLE_EXPRESSIONS if expr in chapter_2_plus_set]
    return solvable_chapter_1, solvable_chapter_2_plus


def _run_random_search_to_file(
    output_path: Path,
    *,
    n_trials: int,
    sample_size: int | None,
    seed: int,
    expression_pool: list,
    run_title: str,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f, redirect_stdout(f):
        print(run_title)
        print(f"trials={n_trials}, sample_size={sample_size}, seed={seed}, pool_size={len(expression_pool)}")
        print("-" * 80)
        random_search(
            n_trials=n_trials,
            sample_size=sample_size,
            seed=seed,
            expression_pool=expression_pool,
        )


def run_overnight(output_dir: str = "evaluation/optimization_runs", seed: int = 42) -> None:
    solvable_chapter_1, solvable_chapter_2_plus = _collect_solvable_pools()

    if not solvable_chapter_1:
        raise ValueError("No solvable chapter 1 expressions found")
    if not solvable_chapter_2_plus:
        raise ValueError("No solvable chapter 2+ expressions found")

    out_dir = Path(output_dir)
    jobs = [
        (
            "chapter1_200_trials.txt",
            "Random search on solvable chapter 1 expressions",
            200,
            None,
            seed,
            solvable_chapter_1,
        ),
        (
            "chapter2plus_200_trials.txt",
            "Random search on solvable chapter 2+ expressions",
            200,
            None,
            seed + 1,
            solvable_chapter_2_plus,
        ),
        (
            "all_solvable_500_trials.txt",
            "Random search on all solvable expressions",
            500,
            None,
            seed + 2,
            SOLVABLE_EXPRESSIONS,
        ),
    ]

    for filename, title, n_trials, sample_size, run_seed, pool in jobs:
        output_path = out_dir / filename
        print(f"Running: {title} -> {output_path}")
        _run_random_search_to_file(
            output_path,
            n_trials=n_trials,
            sample_size=sample_size,
            seed=run_seed,
            expression_pool=pool,
            run_title=title,
        )

    print(f"Overnight optimization completed. Logs written to: {out_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random-search hyperparameter optimiser")
    parser.add_argument("--trials", type=int, default=100, help="number of random candidates (default 100)")
    parser.add_argument("--sample", type=int, default=20,  help="integrals evaluated per trial  (default 20)")
    parser.add_argument("--seed",   type=int, default=42,  help="RNG seed (default 42)")
    parser.add_argument("--overnight", action="store_true", help="run 3 fixed overnight jobs and save full logs")
    parser.add_argument(
        "--output-dir",
        default="evaluation/optimization_runs",
        help="output directory for overnight logs",
    )
    args = parser.parse_args()

    if args.overnight:
        run_overnight(output_dir=args.output_dir, seed=args.seed)
    else:
        random_search(n_trials=args.trials, sample_size=args.sample, seed=args.seed)
