#!/usr/bin/env python3
"""One entry point for every interview kit's practice suites.

    python3 scripts/kit_suites.py --list                 # table of every kit's suites and their commands
    python3 scripts/kit_suites.py --co stripe [--list]   # one kit (repeatable; default: all kits)
    python3 scripts/kit_suites.py --co headlands --skip-missing   # skip suites whose tool (mvn, a C++ compiler) is absent
    python3 scripts/kit_suites.py --co stripe --ci       # what CI runs: wall-clock `perf` tests are deselected

Exit 0 only when every suite behaves as expected. A suite is one of
  green    exit code 0 (reference solutions, acceptance gates);
  red      learner exercises that are red on purpose: the pytest `failed` count must equal the known number
           and nothing may error (Stripe `loop/study` + `loop/rounds/04_bug_squash`: 82).

`--ci` leaves out the `perf` tests (pytest `-m "not perf"`, jtest/cpptest `--exclude-tag perf` on the reference run).
Their budgets are fixed wall-clock seconds measured on a fast desktop; a shared GitHub runner is 2-4x slower and noisy, so
they would fail without the code being wrong. Run them locally (no flag). Correctness tests are unaffected, and the red
suite (expect_failed) is never filtered: its failure count is part of its contract.

pytest runs through `uv run --project <repo> --with pytest` (the kits import `trellis.kit`), the same way
locally and in CI. `UV_FROZEN=1` keeps uv from rewriting uv.lock.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
COMPANIES = REPO / "vault" / "interviews" / "companies"
AMAZON_CODING = REPO / "vault" / "interviews" / "core" / "coding" / "amazon"
PYTEST_FLAGS = ["-q", "-o", "addopts=", "-p", "no:cacheprovider", "-W", "ignore::DeprecationWarning"]
UV_PYTEST = ["uv", "run", "--project", str(REPO), "--with", "pytest", "python", "-m", "pytest"]
UV_TRELLIS = ["uv", "run", "--project", str(REPO), "trellis"]
PY = sys.executable


@dataclass
class Suite:
    kit: str
    name: str
    cmd: list[str]
    cwd: Path
    expect_failed: int | None = None          # None: must exit 0; N: pytest red, exactly N failures, no errors
    needs: tuple[str, ...] = ()               # executables that must be on PATH
    env: dict[str, str] = field(default_factory=dict)

    def shown(self) -> str:
        cmd = " ".join(("'%s'" % a if " " in a or "*" in a else a) for a in self.cmd)
        cmd = cmd.replace(str(REPO), "<repo>").replace(PY, "python3")
        return f"cd {self.cwd.relative_to(REPO)} && {cmd}" + (f"   # expects exactly {self.expect_failed} red" if self.expect_failed else "")


def pytest(kit: str, name: str, cwd: Path, *args: str, expect_failed: int | None = None, env: dict | None = None,
           ci: bool = False) -> Suite:
    """`ci`: deselect the wall-clock `perf` tests (green suites only; a red suite's failure count must stay exact)."""
    perf = ["-m", "not perf"] if ci and expect_failed is None else []
    return Suite(kit, name, [*UV_PYTEST, *args, *perf, *PYTEST_FLAGS], cwd, expect_failed, ("uv",), env or {})


def unittest_dirs(kit: str, root: Path, pattern: str) -> list[Suite]:
    """One stdlib-unittest suite per directory matching `pattern` under `root` (airbnb problems, roblox games)."""
    out = []
    for d in sorted(root.glob(pattern)):
        start = "tests" if (d / "tests").is_dir() else "."
        out.append(Suite(kit, f"unittest {d.name}", [PY, "-B", "-m", "unittest", "discover", "-s", start, "-p", "test_*.py"], d))
    return out


def build(ci: bool = False) -> dict[str, list[Suite]]:
    c = COMPANIES
    no_perf = ["--exclude-tag", "perf"] if ci else []
    kits: dict[str, list[Suite]] = {}

    kits["amazon"] = [Suite("amazon", "coding solutions + lecture blocks (run_all.py)",
                            [PY, "-B", str(AMAZON_CODING / "run_all.py")], REPO)]

    h = c / "headlands"
    kits["headlands"] = [
        Suite("headlands", "Java 21 problems: jtest verify (reference green, starter red)",
              [PY, "-B", "tools/jtest.py", "verify", "loop/rounds/*/*", *no_perf], h, needs=("javac", "mvn")),
        Suite("headlands", "C++20 problems: cpptest verify (-Werror, ASan+UBSan)",
              [PY, "-B", "tools/cpptest.py", "verify", "loop/rounds/*/*", *no_perf], h, needs=("c++",)),
        Suite("headlands", "mock_maven (JUnit 5, reference solutions): mvn test",
              ["mvn", "-q", "-B", "test"], h / "mock_maven" / "java", needs=("mvn",)),
    ]

    s = c / "stripe"
    kits["stripe"] = [
        pytest("stripe", "OA problems", s, "problems", ci=ci),
        pytest("stripe", "loop rounds (all green except the learner exercises)", s, "loop",
               "--ignore=loop/study", "--ignore=loop/rounds/04_bug_squash", ci=ci),
        pytest("stripe", "loop/study exercises + bug-squash starters: red on purpose", s,
               "loop/study", "loop/rounds/04_bug_squash", expect_failed=82),
    ]

    kits["snowflake"] = [pytest("snowflake", "problems + loop rounds", c / "snowflake", "problems", "loop", ci=ci)]
    kits["millennium"] = [pytest("millennium", "loop/rounds (pytest.ini testpaths)", c / "millennium", ci=ci)]
    kits["airbnb"] = unittest_dirs("airbnb", c / "airbnb" / "problems", "q*")
    kits["roblox"] = unittest_dirs("roblox", c / "roblox" / "games", "*")

    a = c / "abnormal"
    kits["abnormal"] = [
        Suite("abnormal", "AI screen codebases cb*: verify_suites (acceptance + own tests)",
              [*UV_TRELLIS, "kit", "verify_suites", "--co", "abnormal", "loop/rounds/01_ai_screen/cb*"], REPO, needs=("uv",)),
        Suite("abnormal", "code review cr*: verify_suites",
              [*UV_TRELLIS, "kit", "verify_suites", "--co", "abnormal", "loop/rounds/03_code_review/cr*"], REPO, needs=("uv",)),
        pytest("abnormal", "incident ic* + legacy coding pc*", a,
               "loop/rounds/02_incident_sd", "loop/rounds/06_legacy_coding", ci=ci),
    ]
    return kits


COUNT = re.compile(r"(\d+) (passed|failed|errors?|skipped|deselected|xfailed|xpassed)")


def pytest_counts(output: str) -> dict[str, int]:
    last = next((ln for ln in reversed(output.strip().splitlines()) if COUNT.search(ln) and " in " in ln), "")
    counts: dict[str, int] = {}
    for n, word in COUNT.findall(last):
        counts[word.rstrip("s") if word.startswith("error") else word] = int(n)
    return counts


def have(tool: str) -> bool:
    """`c++` stands for any C++ compiler: $CXX, clang++, g++ or c++ (tools/cpptest.py picks the same way)."""
    if tool == "c++":
        return any(shutil.which(x) for x in (os.environ.get("CXX", ""), "clang++", "g++", "c++") if x)
    return shutil.which(tool) is not None


def run_suite(su: Suite, skip_missing: bool) -> tuple[str, str, float]:
    """-> (status, one-line summary, seconds); status is PASS, FAIL or SKIP."""
    missing = [t for t in su.needs if not have(t)]
    if missing:
        return ("SKIP" if skip_missing else "FAIL"), "missing: " + ", ".join(missing), 0.0
    env = dict(os.environ, UV_FROZEN="1", PYTHONDONTWRITEBYTECODE="1", **su.env)
    t0 = time.time()
    p = subprocess.run(su.cmd, cwd=su.cwd, env=env, capture_output=True, text=True)
    dt = time.time() - t0
    out = (p.stdout + p.stderr).strip()
    lines = [ln for ln in out.splitlines() if ln.strip()]
    summary = lines[-1] if lines else "(no output)"
    if su.expect_failed is None:
        ok = p.returncode == 0
    else:
        counts = pytest_counts(out)
        ok = p.returncode == 1 and counts.get("failed") == su.expect_failed and not counts.get("error")
        summary = f"{summary}  [expected {su.expect_failed} failed]"
    if not ok:
        print(f"--- {su.kit}: {su.name} (exit {p.returncode}); last 40 lines ---", file=sys.stderr)
        print("\n".join(lines[-40:]), file=sys.stderr)
    return ("PASS" if ok else "FAIL"), summary[:110], dt


def main(argv: list[str]) -> int:
    ci = "--ci" in argv
    kits = build(ci)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--co", action="append", choices=sorted(kits), help="kit to run (repeatable; default: all)")
    ap.add_argument("--list", action="store_true", help="print the suites and their commands, run nothing")
    ap.add_argument("--skip-missing", action="store_true", help="skip suites whose tool is not installed instead of failing")
    ap.add_argument("--ci", action="store_true", help="deselect the wall-clock `perf` tests (slow shared runners); CI passes this")
    a = ap.parse_args(argv)
    chosen = a.co or sorted(kits)
    suites = [su for co in chosen for su in kits[co]]
    if a.list:
        print(f"{'kit':<11} {'suite':<62} command")
        for su in suites:
            print(f"{su.kit:<11} {su.name:<62} {su.shown()}")
        return 0
    results = []
    for su in suites:
        print(f"== {su.kit}: {su.name}", flush=True)
        status, summary, dt = run_suite(su, a.skip_missing)
        print(f"   {status}  {dt:6.1f}s  {summary}", flush=True)
        results.append((su, status, summary, dt))
    print()
    print(f"{'kit':<11} {'status':<6} {'time':>7}  suite")
    for su, status, _, dt in results:
        print(f"{su.kit:<11} {status:<6} {dt:6.1f}s  {su.name}")
    bad = [r for r in results if r[1] == "FAIL"]
    print(f"{len(results) - len(bad)}/{len(results)} suites as expected" + (f", {len(bad)} unexpected failure(s)" if bad else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
