"""Write the synthetic score matrices in data/ (deterministic: same seed, same files).

    uv run --project <repo root> python make_data.py            # rewrite data/*.csv
    uv run --project <repo root> python make_data.py --models 5 # one more model, to try a new model

Each CSV is one benchmark: one row per sample, columns `sample_id`, `difficulty`, then one column per model.
A model's chance of solving a sample follows a logistic curve of (ability - sample hardness), so stronger models
solve more and hard samples are solved less, with noise.

- code_bench.csv:    300 samples, score 0 or 1 (the generated program passed its tests or not).
- longctx_bench.csv: 100 samples, score in [0, 1] (a judge model's grade, rounded to 0.1).
"""
from __future__ import annotations

import argparse
import csv
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
ABILITY = {"model_a": 1.25, "model_b": 0.75, "model_c": 0.25, "model_d": -0.35, "model_e": 0.5}


def _label(hardness: float, rng: random.Random) -> str:
    """The benchmark's own difficulty tag: follows the true hardness, but not perfectly."""
    h = hardness + rng.gauss(0, 0.5)
    return "easy" if h < -0.6 else ("hard" if h > 0.6 else "medium")


def make(name: str, n: int, models: list[str], binary: bool, seed: int) -> Path:
    rng = random.Random(seed)
    path = HERE / "data" / f"{name}.csv"
    path.parent.mkdir(exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["sample_id", "difficulty", *models])
        for i in range(n):
            hardness = rng.gauss(0, 1.3)
            row = [f"{name[:4]}-{i:03d}", _label(hardness, rng)]
            for m in models:
                p = 1 / (1 + math.exp(-1.7 * (ABILITY[m] - hardness)))
                if binary:
                    row.append(1 if rng.random() < p else 0)
                else:
                    row.append(round(min(1.0, max(0.0, p + rng.gauss(0, 0.15))), 1))
            w.writerow(row)
    return path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", type=int, default=4, help="3 to 5 models")
    a = ap.parse_args()
    models = list(ABILITY)[: max(3, min(5, a.models))]
    for p in (make("code_bench", 300, models, True, 7), make("longctx_bench", 100, models, False, 11)):
        print("wrote", p.relative_to(HERE))


if __name__ == "__main__":
    main()
