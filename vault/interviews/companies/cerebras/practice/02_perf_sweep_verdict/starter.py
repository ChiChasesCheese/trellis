"""Perf sweep -> SLA verdict per (model, traffic profile) + anomaly flags.

    uv run --project <repo root> python starter.py data/*.csv --concurrency 16 --ttft-ms 1400 --tps-user 300

The only contract with the input is the header table below and the file-name pattern Model_<X>_profile_<N>.csv.
A new model is a new file or new rows: no code changes.
"""
from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------- Part 1: the header contract

# canonical field -> {normalised header: multiplier into the canonical unit}; problem.md lists the names to accept
SYNONYMS: dict[str, dict[str, float]] = {}
NUMERIC = ("input_len", "output_len", "concurrency", "ttft_ms", "tpot_ms", "tps_user", "tps_total")
FILE_NAME = re.compile(r"Model_(?P<model>[^_]+)_profile_(?P<profile>[^_.]+)", re.I)


def normalize_header(h: str) -> str:
    raise NotImplementedError


def map_headers(headers: list[str]) -> dict[str, tuple[str, float]]:
    raise NotImplementedError


@dataclass(frozen=True)
class Point:
    model: str
    profile: str
    input_len: int
    output_len: int
    concurrency: int
    ttft_ms: float
    tpot_ms: float
    tps_user: float
    tps_total: float


@dataclass(frozen=True)
class Anomaly:
    model: str
    profile: str
    concurrency: int | None
    kind: str  # missing_value | duplicate_point | throughput_drop | ttft_drop | total_mismatch | tpot_mismatch
    detail: str


def parse_sweep(path: str | Path) -> tuple[list[Point], list[Anomaly]]:
    raise NotImplementedError


def load_all(paths: list[str | Path]) -> tuple[list[Point], list[Anomaly]]:
    raise NotImplementedError


def curves(points: list[Point]) -> dict[tuple[str, str], list[Point]]:
    raise NotImplementedError


# ---------------------------------------------------------------- Part 2: the verdict


@dataclass(frozen=True)
class SLA:
    concurrency: int  # how many users the customer will run at once
    ttft_ms_max: float  # longest acceptable wait for the first token
    tps_user_min: float  # slowest acceptable reading speed per user
    amber_margin: float = 0.10  # passing by less than this fraction is amber


@dataclass
class Verdict:
    model: str
    profile: str
    color: str  # green | amber | red
    concurrency_used: int | None
    ttft_ms: float | None
    tps_user: float | None
    reasons: list[str] = field(default_factory=list)


def verdict_for(curve: list[Point], sla: SLA, flagged: set[int] = frozenset()) -> Verdict:
    raise NotImplementedError


def verdicts(points: list[Point], sla: SLA, anomalies: list[Anomaly] = ()) -> list[Verdict]:
    raise NotImplementedError


# ---------------------------------------------------------------- Part 3: anomaly flags


def find_anomalies(points: list[Point], step_tol: float = 0.02, ratio_tol: float = 0.10) -> list[Anomaly]:
    raise NotImplementedError


# ---------------------------------------------------------------- Part 4: the report


def report(paths: list[str | Path], sla: SLA) -> str:
    raise NotImplementedError


def main(argv: list[str] | None = None) -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
