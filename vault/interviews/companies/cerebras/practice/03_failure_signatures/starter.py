"""JUnit XML from repeated CI runs -> failure signatures -> regression / flaky / infra per test.

    uv run --project <repo root> python starter.py runs/*.xml
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------- Part 1: parse


@dataclass(frozen=True)
class Outcome:
    test: str  # "classname::name"
    run: str  # which CI run (the file stem by default)
    status: str  # pass | fail | skip
    message: str = ""  # raw failure text ("" for pass and skip)


def parse_junit(path: str | Path, run: str | None = None) -> list[Outcome]:
    raise NotImplementedError


# ---------------------------------------------------------------- Part 2: signatures

# (compiled pattern, replacement) pairs, applied in order: fill in
NOISE: list[tuple[re.Pattern, str]] = []
INFRA_PATTERNS = [r"connection refused", r"connection reset by peer", r"no space left on device",
                  r"timed out waiting for device", r"oomkilled|out of memory", r"could not resolve host",
                  r"resource temporarily unavailable"]


def signature(message: str, max_len: int = 200) -> str:
    raise NotImplementedError


def is_infra(sig: str, patterns: list[str] = INFRA_PATTERNS) -> bool:
    raise NotImplementedError


# ---------------------------------------------------------------- Part 3: classify


@dataclass
class TestReport:
    test: str
    kind: str  # regression | flaky | infra | fixed | pass | skipped
    since: str | None  # regression: first run of the final failing streak; fixed: first passing run
    fails: int  # failing runs, infra included
    runs: int  # runs where the test ran (not skipped, not absent)
    signatures: Counter = field(default_factory=Counter)

    @property
    def top_signature(self) -> str:
        return self.signatures.most_common(1)[0][0] if self.signatures else ""


def classify(history: list[Outcome], patterns: list[str] = INFRA_PATTERNS) -> TestReport:
    raise NotImplementedError


def analyze(paths: list[str | Path], patterns: list[str] = INFRA_PATTERNS) -> list[TestReport]:
    raise NotImplementedError


# ---------------------------------------------------------------- Part 4: the table

ORDER = {"regression": 0, "flaky": 1, "infra": 2, "fixed": 3, "skipped": 4, "pass": 5}


def table(reports: list[TestReport]) -> str:
    raise NotImplementedError


def main(argv: list[str] | None = None) -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
