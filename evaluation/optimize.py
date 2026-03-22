"""
Hyperparameter optimization over all parameters:
  - 6 bell-curve params  (optimum + deviation for solvability, depth, controllability)
  - 16 rule score params (one integer weight per rule in points_table)

Objective: maximise the mean evaluation score across a random sample of
ALL_EXPRESSIONS (all known-good integration-bee integrals).

Usage:
        python -m evaluation.optimize                           # default sklearn optimizer
        python -m evaluation.optimize --method random           # random search baseline
        python -m evaluation.optimize --trials 200 --sample 40 --seed 7
    python -m evaluation.optimize --overnight  # 3 long runs, logs to text files
"""
import argparse
import math
import random
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import numpy as np
import utils.tree_solution as _ts
from scipy.stats import norm

from evaluation.evaluation import get_evaluation_components
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


def _format_params(params: list[float]) -> dict[str, float]:
    rounded = [round(p, 2) for p in params]
    return dict(zip(ALL_PARAM_NAMES, rounded))


def _bell(value: float, optimum: float, deviation: float) -> float:
    peak = norm.pdf(optimum, loc=optimum, scale=deviation)
    return norm.pdf(value, loc=optimum, scale=deviation) / peak


def _stable_hmean(values: list[float]) -> float:
    # Harmonic mean in log-space avoids overflow from 1/x when x is tiny.
    neg_logs = [-math.log(v) for v in values]
    max_neg_log = max(neg_logs)
    scaled_sum = sum(math.exp(v - max_neg_log) for v in neg_logs)
    return math.exp(math.log(len(values)) - (max_neg_log + math.log(scaled_sum)))


def _score_expr(expr, params: list[float]) -> float | None:
    solv_opt, solv_dev, depth_opt, depth_dev, ctrl_opt, ctrl_dev = params[:N_BELL]
    rule_values = [round(v) for v in params[N_BELL:]]

    # patch points_table for this trial
    original_table = _ts.points_table.copy()
    _ts.points_table.update(dict(zip([n for n, _ in RULE_PARAMS], rule_values)))

    try:
        with redirect_stdout(StringIO()):
            s, d, c = get_evaluation_components(expr)
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
        return float(_stable_hmean(adjusted))
    except Exception:
        return None


def _objective(params: list[float], exprs) -> float:
    scores = [s for e in exprs if (s := _score_expr(e, params)) is not None]
    return sum(scores) / len(scores) if scores else 0.0


def _print_best_result(best_params: list[float], best_score: float) -> None:
    bell_best = best_params[:N_BELL]
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


def _sample_params(rng: random.Random) -> list[float]:
    return [rng.uniform(lo, hi) for lo, hi in ALL_BOUNDS]


def _to_unit_cube(params: list[float]) -> list[float]:
    scaled = []
    for p, (lo, hi) in zip(params, ALL_BOUNDS):
        span = hi - lo
        scaled.append((p - lo) / span if span > 0 else 0.0)
    return scaled


def _from_unit_cube(coords: list[float]) -> list[float]:
    params = []
    for c, (lo, hi) in zip(coords, ALL_BOUNDS):
        clipped = min(1.0, max(0.0, c))
        params.append(lo + clipped * (hi - lo))
    return params


def sklearn_search(
    n_trials: int = 100,
    sample_size: int | None = 20,
    seed: int = 42,
    expression_pool: list | None = None,
    n_initial: int | None = None,
    candidate_pool: int = 200,
    xi: float = 0.01,
) -> list[float]:
    try:
        from sklearn.gaussian_process import GaussianProcessRegressor
        from sklearn.gaussian_process.kernels import ConstantKernel, Matern, WhiteKernel
    except ImportError as exc:
        raise ImportError(
            "scikit-learn is required for --method sklearn. Install it with: pip install scikit-learn"
        ) from exc

    rng = random.Random(seed)
    np_rng = np.random.default_rng(seed)
    pool = expression_pool if expression_pool is not None else SOLVABLE_EXPRESSIONS
    if not pool:
        raise ValueError("expression_pool must contain at least one expression")

    if sample_size is None:
        sample = list(pool)
    else:
        sample = rng.sample(pool, min(sample_size, len(pool)))

    if n_initial is None:
        n_initial = max(10, min(30, n_trials // 4))
    n_initial = min(max(1, n_initial), n_trials)

    x_seen: list[list[float]] = []
    y_seen: list[float] = []
    best_params: list[float] = []
    best_score = -1.0

    # Start with random points so the surrogate has enough signal.
    for trial in range(n_initial):
        params = _sample_params(rng)
        score = _objective(params, sample)
        x_seen.append(_to_unit_cube(params))
        y_seen.append(score)

        print(f"[{trial + 1:>4}/{n_trials}]  score={score:.4f}  {_format_params(params)}")
        if score > best_score:
            best_score = score
            best_params = params[:]
            print("           ^ new best")

    for trial in range(n_initial, n_trials):
        kernel = (
            ConstantKernel(1.0, (1e-3, 1e3))
            * Matern(length_scale=np.ones(len(ALL_BOUNDS)), nu=2.5)
            + WhiteKernel(noise_level=1e-5, noise_level_bounds=(1e-9, 1e-1))
        )
        gp = GaussianProcessRegressor(
            kernel=kernel,
            normalize_y=True,
            random_state=seed,
            n_restarts_optimizer=2,
        )

        next_params: list[float] | None = None
        try:
            x_train = np.array(x_seen, dtype=float)
            y_train = np.array(y_seen, dtype=float)
            gp.fit(x_train, y_train)

            candidates_unit = np_rng.random((candidate_pool, len(ALL_BOUNDS)))
            mu, sigma = gp.predict(candidates_unit, return_std=True)
            sigma = np.maximum(sigma, 1e-12)

            best_y = max(y_seen)
            improvement = mu - best_y - xi
            z = improvement / sigma
            ei = improvement * norm.cdf(z) + sigma * norm.pdf(z)
            best_idx = int(np.argmax(ei))
            next_params = _from_unit_cube(candidates_unit[best_idx].tolist())
        except Exception:
            next_params = None

        if next_params is None:
            next_params = _sample_params(rng)

        score = _objective(next_params, sample)
        x_seen.append(_to_unit_cube(next_params))
        y_seen.append(score)

        print(f"[{trial + 1:>4}/{n_trials}]  score={score:.4f}  {_format_params(next_params)}")
        if score > best_score:
            best_score = score
            best_params = next_params[:]
            print("           ^ new best")

    _print_best_result(best_params, best_score)
    return best_params


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
        params = _sample_params(rng)
        score = _objective(params, sample)

        print(f"[{trial + 1:>4}/{n_trials}]  score={score:.4f}  {_format_params(params)}")

        if score > best_score:
            best_score = score
            best_params = params[:]
            print("           ^ new best")

    _print_best_result(best_params, best_score)

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


def _run_sklearn_search_to_file(
    output_path: Path,
    *,
    n_trials: int,
    sample_size: int | None,
    seed: int,
    expression_pool: list,
    run_title: str,
    n_initial: int | None,
    candidate_pool: int,
    xi: float,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f, redirect_stdout(f):
        print(run_title)
        print(f"trials={n_trials}, sample_size={sample_size}, seed={seed}, pool_size={len(expression_pool)}")
        print(f"optimizer=sklearn, n_initial={n_initial}, candidate_pool={candidate_pool}, xi={xi}")
        print("-" * 80)
        sklearn_search(
            n_trials=n_trials,
            sample_size=sample_size,
            seed=seed,
            expression_pool=expression_pool,
            n_initial=n_initial,
            candidate_pool=candidate_pool,
            xi=xi,
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
        #(
         #   "all_solvable_500_trials.txt",
          #  "Random search on all solvable expressions",
           # 500,
            #None,
         #   seed + 2,
          #  SOLVABLE_EXPRESSIONS,
        #),
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
    parser = argparse.ArgumentParser(description="Hyperparameter optimiser")
    parser.add_argument(
        "--method",
        choices=["random", "sklearn"],
        default="sklearn",
        help="optimizer method (default: sklearn)",
    )
    parser.add_argument("--trials", type=int, default=100, help="number of random candidates (default 100)")
    parser.add_argument("--sample", type=int, default=20,  help="integrals evaluated per trial  (default 20)")
    parser.add_argument("--seed",   type=int, default=42,  help="RNG seed (default 42)")
    parser.add_argument(
        "--n-initial",
        type=int,
        default=None,
        help="number of initial random trials before GP fitting (sklearn method)",
    )
    parser.add_argument(
        "--candidate-pool",
        type=int,
        default=200,
        help="candidate count per GP step for expected-improvement maximization",
    )
    parser.add_argument(
        "--xi",
        type=float,
        default=0.01,
        help="exploration parameter for expected improvement (sklearn method)",
    )
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
        if args.method == "random":
            random_search(n_trials=args.trials, sample_size=args.sample, seed=args.seed)
        else:
            sklearn_search(
                n_trials=args.trials,
                sample_size=args.sample,
                seed=args.seed,
                n_initial=args.n_initial,
                candidate_pool=args.candidate_pool,
                xi=args.xi,
            )
