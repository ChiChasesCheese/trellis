"""JUnit XML from repeated CI runs -> failure signatures -> regression / flaky / infra per test.

    uv run --project <repo root> python solution.py runs/*.xml
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
    """One Outcome per <testcase>. <failure> and <error> both count as fail; <skipped> as skip. The root may be
    <testsuites> or a single <testsuite>."""
    path = Path(path)
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        raise ValueError(f"{path.name}: not valid XML ({e})") from None
    if root.tag not in ("testsuites", "testsuite"):
        raise ValueError(f"{path.name}: root is <{root.tag}>, not a JUnit report")
    run = run or path.stem
    out = []
    for case in root.iter("testcase"):
        cls, name = case.get("classname", ""), case.get("name", "")
        test = f"{cls}::{name}" if cls else name
        bad = case.find("failure")
        if bad is None:
            bad = case.find("error")
        if bad is not None:
            msg = bad.get("message") or next((ln for ln in (bad.text or "").splitlines() if ln.strip()), "")
            out.append(Outcome(test, run, "fail", msg.strip()))
        elif case.find("skipped") is not None:
            out.append(Outcome(test, run, "skip"))
        else:
            out.append(Outcome(test, run, "pass"))
    return out


# ---------------------------------------------------------------- Part 2: signatures

# Order matters: the specific shapes go first, or the number rule would chew them into pieces.
NOISE = [
    (re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I), "<UUID>"),
    (re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?Z?"), "<TS>"),
    (re.compile(r"0x[0-9a-f]+", re.I), "<ADDR>"),
    (re.compile(r"\b\d{1,3}(\.\d{1,3}){3}(:\d+)?\b"), "<IP>"),
    (re.compile(r"(/tmp|/private/var|/var/folders|/var/tmp)/[^\s'\"]*"), "<TMP>"),
    (re.compile(r"\d+(\.\d+)?"), "<N>"),
    (re.compile(r"\s+"), " "),
]
INFRA_PATTERNS = [r"connection refused", r"connection reset by peer", r"no space left on device",
                  r"timed out waiting for device", r"oomkilled|out of memory", r"could not resolve host",
                  r"resource temporarily unavailable"]


def signature(message: str, max_len: int = 200) -> str:
    """The message with the run-specific parts replaced, so the same bug gets the same text in every run."""
    s = message.strip()
    for pattern, repl in NOISE:
        s = pattern.sub(repl, s)
    return s.strip()[:max_len]


def is_infra(sig: str, patterns: list[str] = INFRA_PATTERNS) -> bool:
    return any(re.search(p, sig, re.I) for p in patterns)


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
    """history = one test's outcomes in run order (runs where it was absent simply have no entry).
    Infra failures say nothing about the code: drop them, then read the pass/fail sequence that is left:
    all pass -> pass; P..P F..F -> regression since the first F (all F: since the first run); F..F P..P -> fixed;
    anything else -> flaky."""
    test = history[0].test if history else ""
    ran = [o for o in history if o.status != "skip"]
    sigs = Counter(signature(o.message) for o in ran if o.status == "fail")
    fails = sum(sigs.values())
    if not ran:
        return TestReport(test, "skipped", None, 0, 0, sigs)
    if fails == 0:
        return TestReport(test, "pass", None, 0, len(ran), sigs)
    real = [o for o in ran if not (o.status == "fail" and is_infra(signature(o.message), patterns))]
    if not any(o.status == "fail" for o in real):
        return TestReport(test, "infra", None, fails, len(ran), sigs)
    seq = "".join("F" if o.status == "fail" else "P" for o in real)
    changes = sum(a != b for a, b in zip(seq, seq[1:]))
    if seq[-1] == "F" and changes <= 1:
        return TestReport(test, "regression", real[seq.index("F")].run, fails, len(ran), sigs)
    if seq[0] == "F" and changes == 1:
        return TestReport(test, "fixed", real[seq.index("P")].run, fails, len(ran), sigs)
    return TestReport(test, "flaky", None, fails, len(ran), sigs)


def analyze(paths: list[str | Path], patterns: list[str] = INFRA_PATTERNS) -> list[TestReport]:
    """paths in run order. Tests in first-seen order."""
    by_test: dict[str, list[Outcome]] = {}
    for p in paths:
        for o in parse_junit(p):
            by_test.setdefault(o.test, []).append(o)
    return [classify(h, patterns) for h in by_test.values()]


# ---------------------------------------------------------------- Part 4: the table

ORDER = {"regression": 0, "flaky": 1, "infra": 2, "fixed": 3, "skipped": 4, "pass": 5}


def table(reports: list[TestReport]) -> str:
    rows = sorted(reports, key=lambda r: (ORDER[r.kind], r.test))
    width = max([len(r.test) for r in rows] + [4])
    lines = [f"{'test':{width}s}  {'verdict':10s}  {'since':7s}  fails  signature"]
    for r in rows:
        lines.append(f"{r.test:{width}s}  {r.kind:10s}  {r.since or '-':7s}  {r.fails}/{r.runs:<3d}  {r.top_signature}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    paths = sorted(argv if argv is not None else sys.argv[1:])
    if not paths:
        raise SystemExit("usage: solution.py runs/*.xml")
    print(table(analyze(paths)))


if __name__ == "__main__":
    main()
