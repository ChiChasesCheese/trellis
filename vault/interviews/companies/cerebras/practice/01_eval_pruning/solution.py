"""Eval pruning: the smallest subset of a benchmark that keeps the model ranking and the go/no-go verdict.

    uv run --project <repo root> python solution.py      # report for data/*.csv
"""
from __future__ import annotations

import csv
import math
import statistics
from dataclasses import dataclass, field
from pathlib import Path

META_COLUMNS = ("sample_id", "difficulty")
THRESHOLDS = {"code_bench": 0.5, "longctx_bench": 0.55}  # the customer's pass mark per benchmark
EPS = 1e-12


@dataclass
class Bench:
    name: str
    sample_ids: list[str]
    difficulty: list[str]
    scores: dict[str, list[float]]  # model -> one score per sample, same order as sample_ids

    @property
    def models(self) -> list[str]:
        return list(self.scores)

    def __len__(self) -> int:
        return len(self.sample_ids)


# ---------------------------------------------------------------- Part 1: load, score, compare


def load_bench(path: str | Path, name: str | None = None) -> Bench:
    """Read one benchmark CSV. Every column that is not a metadata column is a model, so a new model needs no code."""
    path = Path(path)
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        missing = [c for c in META_COLUMNS if c not in header]
        if missing:
            raise ValueError(f"{path.name}: missing column(s) {missing}")
        models = [c for c in header if c not in META_COLUMNS]
        if not models:
            raise ValueError(f"{path.name}: no model columns")
        ids: list[str] = []
        difficulty: list[str] = []
        scores: dict[str, list[float]] = {m: [] for m in models}
        for line_no, row in enumerate(reader, start=2):
            ids.append(row["sample_id"])
            difficulty.append((row["difficulty"] or "").strip() or "unknown")
            for m in models:
                raw = (row[m] or "").strip()
                try:
                    v = float(raw)
                except ValueError:
                    raise ValueError(f"{path.name}:{line_no}: {m} score {raw!r} is not a number") from None
                if not 0.0 <= v <= 1.0:  # also rejects NaN, which fails every comparison
                    raise ValueError(f"{path.name}:{line_no}: {m} score {v} outside [0, 1]")
                scores[m].append(v)
    if not ids:
        raise ValueError(f"{path.name}: no samples")
    if len(set(ids)) != len(ids):
        raise ValueError(f"{path.name}: duplicate sample_id")
    return Bench(name or path.stem, ids, difficulty, scores)


def model_means(bench: Bench, idx: list[int] | None = None, models: list[str] | None = None) -> dict[str, float]:
    """Average score per model over the samples in idx (all samples when idx is None)."""
    idx = range(len(bench)) if idx is None else idx
    if len(idx) == 0:
        raise ValueError("empty subset")
    return {m: sum(bench.scores[m][i] for i in idx) / len(idx) for m in (models or bench.models)}


def _sign(x: float) -> int:
    return 0 if abs(x) <= EPS else (1 if x > 0 else -1)


def kendall_tau(a: dict[str, float], b: dict[str, float]) -> float:
    """Agreement of two rankings of the same models, from -1 (reversed) to 1 (identical).

    For every pair of models: +1 if both rankings order it the same way (a tie in both counts as the same),
    -1 if they order it the opposite way, 0 if only one of them calls it a tie. Divide by the number of pairs.
    """
    keys = sorted(set(a) & set(b))
    if len(keys) < 2:
        raise ValueError("need at least 2 models in common")
    total = pairs = 0
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            sa = _sign(a[keys[i]] - a[keys[j]])
            sb = _sign(b[keys[i]] - b[keys[j]])
            total += 1 if sa == sb else (-1 if sa * sb < 0 else 0)
            pairs += 1
    return total / pairs


def verdicts(means: dict[str, float], threshold: float) -> dict[str, bool]:
    """Go (True) when the model's score reaches the pass mark."""
    return {m: s >= threshold - EPS for m, s in means.items()}


# ---------------------------------------------------------------- Part 2: choose the subset


def item_stats(bench: Bench, models: list[str]) -> tuple[list[float], list[float]]:
    """Per sample: difficulty = mean score over the models (low = hard), discrimination = spread of their scores."""
    p, d = [], []
    for i in range(len(bench)):
        row = [bench.scores[m][i] for m in models]
        p.append(sum(row) / len(row))
        d.append(statistics.pstdev(row))
    return p, d


def allocate(sizes: dict[str, int], k: int) -> dict[str, int]:
    """Split k picks across strata in proportion to their size (largest remainder; ties go to the stratum name
    that sorts first). Never gives a stratum more than it has."""
    n = sum(sizes.values())
    k = min(k, n)
    raw = {s: k * c / n for s, c in sizes.items()}
    quota = {s: math.floor(r) for s, r in raw.items()}
    left = k - sum(quota.values())
    for s in sorted(sizes, key=lambda s: (-(raw[s] - quota[s]), s))[:left]:
        quota[s] += 1
    return quota


def select_subset(bench: Bench, k: int, models: list[str] | None = None) -> list[int]:
    """k sample indices. Strata = the benchmark's difficulty tag (a property of the sample, not of any model); quota
    per stratum in proportion to its size. Inside a stratum, line the samples up from hard to easy (mean score of
    `models`; equal ones: the more discriminating first) and take evenly spaced positions, so the subset keeps the
    stratum's spread of difficulty and therefore each model's absolute score.
    Only the scores of `models` are read, so a held-out model cannot influence the choice."""
    if k <= 0:
        raise ValueError("k must be positive")
    models = models or bench.models
    p, disc = item_stats(bench, models)
    strata: dict[str, list[int]] = {}
    for i, tag in enumerate(bench.difficulty):
        strata.setdefault(tag, []).append(i)
    quota = allocate({s: len(v) for s, v in strata.items()}, k)
    chosen: list[int] = []
    for s, members in strata.items():
        line = sorted(members, key=lambda i: (p[i], -disc[i], i))
        n, q = len(line), quota[s]
        chosen += [line[int((j + 0.5) * n / q)] for j in range(q)]  # step n/q >= 1, so positions never repeat
    return sorted(chosen)


# ---------------------------------------------------------------- Part 3: check it and find the smallest


@dataclass
class Report:
    bench: str
    n_full: int
    size: int
    tau: float
    verdict_agreement: float  # fraction of models whose go/no-go is unchanged
    max_gap: float  # largest |subset score - full score| over the models
    ok: bool
    indices: list[int] = field(default_factory=list, repr=False)


def evaluate_subset(bench: Bench, idx: list[int], threshold: float, models: list[str] | None = None,
                    max_gap: float = 0.05) -> Report:
    models = models or bench.models
    full = model_means(bench, None, models)
    sub = model_means(bench, idx, models)
    tau = kendall_tau(full, sub)
    vf, vs = verdicts(full, threshold), verdicts(sub, threshold)
    agree = sum(vf[m] == vs[m] for m in models) / len(models)
    gap = max(abs(full[m] - sub[m]) for m in models)
    ok = tau >= 1 - EPS and agree >= 1 - EPS and gap <= max_gap + EPS
    return Report(bench.name, len(bench), len(idx), tau, agree, gap, ok, sorted(idx))


def smallest_subset(bench: Bench, threshold: float, models: list[str] | None = None,
                    max_gap: float = 0.05) -> Report:
    """Smallest k from which every larger budget also passes. The first k that passes can pass by luck (four models
    are only six pairs to order), so scan down from the full set and stop at the first failure."""
    best = evaluate_subset(bench, select_subset(bench, len(bench), models), threshold, models, max_gap)
    for k in range(len(bench) - 1, 0, -1):
        r = evaluate_subset(bench, select_subset(bench, k, models), threshold, models, max_gap)
        if not r.ok:
            break
        best = r
    return best


# ---------------------------------------------------------------- Part 4: leave one model out


@dataclass
class HoldOut:
    held_out: str
    size: int
    verdict_kept: bool  # the held-out model's go/no-go on the subset equals its full-set verdict
    gap: float  # |subset score - full score| of the held-out model
    tau_all: float  # ranking of all models, held-out included, subset vs full
    indices: list[int] = field(default_factory=list, repr=False)


def leave_one_model_out(bench: Bench, threshold: float, max_gap: float = 0.05) -> list[HoldOut]:
    """Choose the subset without one model, then check that model: does the method work for a model it never saw?"""
    if len(bench.models) < 3:
        raise ValueError("leave-one-model-out needs at least 3 models")
    out = []
    full = model_means(bench)
    for m in bench.models:
        others = [x for x in bench.models if x != m]
        r = smallest_subset(bench, threshold, others, max_gap)
        sub = model_means(bench, r.indices)
        out.append(HoldOut(m, r.size, verdicts(full, threshold)[m] == verdicts(sub, threshold)[m],
                           abs(full[m] - sub[m]), kendall_tau(full, sub), r.indices))
    return out


def main() -> None:
    data = Path(__file__).resolve().parent / "data"
    for path in sorted(data.glob("*.csv")):
        bench = load_bench(path)
        threshold = THRESHOLDS.get(bench.name, 0.5)
        r = smallest_subset(bench, threshold)
        print(f"{bench.name}: {r.size}/{r.n_full} samples ({r.size / r.n_full:.0%}), tau={r.tau:.2f}, "
              f"verdicts kept={r.verdict_agreement:.0%}, max gap={r.max_gap:.3f}, threshold={threshold}")
        for m, s in model_means(bench).items():
            print(f"    {m:10s} full={s:.3f} subset={model_means(bench, r.indices)[m]:.3f}")
        print("    leave one model out:")
        for h in leave_one_model_out(bench, threshold):
            print(f"    - without {h.held_out:10s} size={h.size:3d} verdict kept={h.verdict_kept!s:5s} "
                  f"gap={h.gap:.3f} tau(all)={h.tau_all:.2f}")


if __name__ == "__main__":
    main()
