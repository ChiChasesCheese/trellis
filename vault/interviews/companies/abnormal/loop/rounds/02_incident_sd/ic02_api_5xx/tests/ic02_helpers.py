"""Shared helpers for the ic02 tests (unique module name: several drills live in one pytest session)."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

DRILL = Path(__file__).resolve().parents[1]
ENV = DRILL / "env"


def load_awsim():
    spec = importlib.util.spec_from_file_location("ic02_awsim", DRILL / "awsim.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


awsim = load_awsim()


def q(*argv: str) -> dict:
    """Run one awsim sub-command in-process and return its result dict."""
    a = awsim.build_parser().parse_args(list(argv))
    return a.fn(a)


def series(ns: str, name: str, stat="Average", dims=(), start=None, end=None, period=60) -> dict[str, float]:
    argv = ["metrics", "get", "--namespace", ns, "--name", name, "--stat", stat, "--period", str(period)]
    for d in dims:
        argv += ["--dim", d]
    if start:
        argv += ["--start", start]
    if end:
        argv += ["--end", end]
    return {p["Timestamp"]: p[stat] for p in q(*argv)["Datapoints"]}


def at(s: dict, hhmm: str) -> float:
    day = awsim.meta()["now"][:10]
    return s[f"{day}T{hhmm}:00Z"]


def window_vals(s: dict, lo: str, hi: str) -> list[float]:
    day = awsim.meta()["now"][:10]
    return [v for k, v in s.items() if f"{day}T{lo}:00Z" <= k < f"{day}T{hi}:00Z"]


ISO_ANY = re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(?::\d{2})?(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?")
ISO_OK = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
