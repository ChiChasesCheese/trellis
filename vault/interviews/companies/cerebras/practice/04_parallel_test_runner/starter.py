"""Bounded parallel runner for shell commands: max concurrency, per-command timeout that kills the whole process
group, retries only on transient exit codes, and a summary.

    uv run --project <repo root> python starter.py commands.txt --jobs 3 --timeout 2 --retries 1 --transient 75
    (commands.txt: one "name: shell command" per line; blank lines and # comments ignored)
"""
from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

# ---------------------------------------------------------------- Part 1: one command, with a timeout


@dataclass
class Attempt:
    returncode: int | None  # None when it was killed for running too long
    timed_out: bool
    seconds: float
    output: str  # stdout and stderr together, last 2000 characters


def run_once(cmd: str, timeout: float, tail: int = 2000) -> Attempt:
    raise NotImplementedError


def _kill_group(proc: subprocess.Popen, grace: float = 0.5) -> None:
    raise NotImplementedError


# ---------------------------------------------------------------- Part 2: retry policy


@dataclass
class Result:
    name: str
    cmd: str
    status: str  # pass | fail | timeout
    returncode: int | None
    attempts: list[Attempt] = field(default_factory=list)

    @property
    def seconds(self) -> float:
        return sum(a.seconds for a in self.attempts)


def run_with_retries(name: str, cmd: str, timeout: float, retries: int, transient: frozenset[int]) -> Result:
    raise NotImplementedError


# ---------------------------------------------------------------- Part 3: in parallel, bounded


def run_all(commands: list[tuple[str, str]], jobs: int, timeout: float, retries: int = 0,
            transient: set[int] | frozenset[int] = frozenset()) -> list[Result]:
    raise NotImplementedError


# ---------------------------------------------------------------- Part 4: summary


def summarize(results: list[Result], wall: float | None = None) -> str:
    raise NotImplementedError


def parse_commands(text: str) -> list[tuple[str, str]]:
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    raise NotImplementedError


if __name__ == "__main__":
    sys.exit(main())
