#!/usr/bin/env python3
"""Print a markdown table summarising every problem: tests by marker, measured perf, status.

Usage: python tools/summary.py [--run]   (--run executes each suite to get pass/fail counts)
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKERS = ["part1", "part2", "part3", "part4", "part5", "edge", "fmt", "perf", "io"]


def count_markers(test_file: Path) -> dict[str, int]:
    src = test_file.read_text()
    return {m: len(re.findall(rf"@pytest\.mark\.{m}\b", src)) for m in MARKERS}


def measured(report: Path) -> str:
    if not report.exists():
        return "—"
    m = re.search(r"Measured:?\s*([^\n]+)", report.read_text())
    return m.group(1).strip()[:60] if m else "—"


def title(problem_md: Path) -> str:
    first = problem_md.read_text().splitlines()[0]
    return first.lstrip("# ").split("·", 1)[-1].strip()[:60]


def run_suite(d: Path) -> str:
    p = subprocess.run(
        [sys.executable, "-m", "pytest", str(d), "-o", "addopts=", "-q", "--tb=no", "-p", "no:cacheprovider", "-W", "ignore"],
        capture_output=True, text=True, cwd=ROOT,
    )
    last = re.sub(r"\x1b\[[0-9;]*m", "", p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "")
    return last


def main() -> None:
    run = "--run" in sys.argv
    rows, totals = [], {m: 0 for m in MARKERS}
    for d in sorted((ROOT / "problems").iterdir()):
        tests = list(d.glob("test_*.py"))
        if not d.is_dir() or not tests:
            continue
        c = count_markers(tests[0])
        for m in MARKERS:
            totals[m] += c[m]
        n = sum(c[m] for m in MARKERS[:5])
        status = run_suite(d) if run else ""
        rows.append((d.name, title(d / "problem.md"), n, c, measured(d / "REPORT.md"), status))
    print("| dir | title | tests | p1/p2/p3/p4/p5 | edge | fmt | perf | io | measured | status |")
    print("|---|---|---:|---|---:|---:|---:|---:|---|---|")
    for name, t, n, c, meas, st in rows:
        parts = "/".join(str(c[f"part{i}"]) for i in range(1, 6))
        print(f"| {name} | {t} | {n} | {parts} | {c['edge']} | {c['fmt']} | {c['perf']} | {c['io']} | {meas} | {st} |")
    print(f"\n**{len(rows)} problems · {sum(totals[m] for m in MARKERS[:5])} tests** "
          f"(edge {totals['edge']} · fmt {totals['fmt']} · perf {totals['perf']} · io {totals['io']})")


if __name__ == "__main__":
    main()
