"""Eval pruning: the smallest subset of a benchmark that keeps the model ranking and the go/no-go verdict.

Fill in every function. Run the tests against this file with:
    IMPL=starter uv run --project <repo root> pytest practice/01_eval_pruning -q
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

META_COLUMNS = ("sample_id", "difficulty")
THRESHOLDS = {"code_bench": 0.5, "longctx_bench": 0.55}  # the customer's pass mark per benchmark


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


# Part 1


def load_bench(path: str | Path, name: str | None = None) -> Bench:
    raise NotImplementedError


def model_means(bench: Bench, idx: list[int] | None = None, models: list[str] | None = None) -> dict[str, float]:
    raise NotImplementedError


def kendall_tau(a: dict[str, float], b: dict[str, float]) -> float:
    raise NotImplementedError


def verdicts(means: dict[str, float], threshold: float) -> dict[str, bool]:
    raise NotImplementedError


# Part 2


def item_stats(bench: Bench, models: list[str]) -> tuple[list[float], list[float]]:
    raise NotImplementedError


def allocate(sizes: dict[str, int], k: int) -> dict[str, int]:
    raise NotImplementedError


def select_subset(bench: Bench, k: int, models: list[str] | None = None) -> list[int]:
    raise NotImplementedError


# Part 3


@dataclass
class Report:
    bench: str
    n_full: int
    size: int
    tau: float
    verdict_agreement: float
    max_gap: float
    ok: bool
    indices: list[int] = field(default_factory=list, repr=False)


def evaluate_subset(bench: Bench, idx: list[int], threshold: float, models: list[str] | None = None,
                    max_gap: float = 0.05) -> Report:
    raise NotImplementedError


def smallest_subset(bench: Bench, threshold: float, models: list[str] | None = None,
                    max_gap: float = 0.05) -> Report:
    raise NotImplementedError


# Part 4


@dataclass
class HoldOut:
    held_out: str
    size: int
    verdict_kept: bool
    gap: float
    tau_all: float
    indices: list[int] = field(default_factory=list, repr=False)


def leave_one_model_out(bench: Bench, threshold: float, max_gap: float = 0.05) -> list[HoldOut]:
    raise NotImplementedError


if __name__ == "__main__":
    raise NotImplementedError
