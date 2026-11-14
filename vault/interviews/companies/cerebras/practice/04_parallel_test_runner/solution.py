"""Bounded parallel runner for shell commands: max concurrency, per-command timeout that kills the whole process
group, retries only on transient exit codes, and a summary.

    uv run --project <repo root> python solution.py commands.txt --jobs 3 --timeout 2 --retries 1 --transient 75
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
    """Run cmd in a shell, in a new session (= its own process group), so a timeout can kill the shell AND every
    child it started. Killing only the shell would leave grandchildren running and holding the output pipe open."""
    start = time.monotonic()
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                            start_new_session=True)
    try:
        out, _ = proc.communicate(timeout=timeout)  # communicate drains the pipe: no deadlock on big output
        return Attempt(proc.returncode, False, time.monotonic() - start, out[-tail:])
    except subprocess.TimeoutExpired:
        _kill_group(proc)
        out, _ = proc.communicate()
        return Attempt(None, True, time.monotonic() - start, (out or "")[-tail:])


def _kill_group(proc: subprocess.Popen, grace: float = 0.5) -> None:
    """SIGTERM the group (lets well-behaved children clean up), then SIGKILL whatever is still there."""
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        proc.wait(timeout=grace)
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(proc.pid, signal.SIGKILL)  # the group may outlive the shell: kill it regardless
    except ProcessLookupError:
        pass


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
    """Retry only when the exit code says "try again" (a configured transient code). A real failure or a timeout is
    not retried: retrying a real failure hides it, and a timeout already cost the full budget."""
    attempts = []
    for _ in range(retries + 1):
        a = run_once(cmd, timeout)
        attempts.append(a)
        if a.timed_out or a.returncode == 0 or a.returncode not in transient:
            break
    last = attempts[-1]
    status = "timeout" if last.timed_out else ("pass" if last.returncode == 0 else "fail")
    return Result(name, cmd, status, last.returncode, attempts)


# ---------------------------------------------------------------- Part 3: in parallel, bounded


def run_all(commands: list[tuple[str, str]], jobs: int, timeout: float, retries: int = 0,
            transient: set[int] | frozenset[int] = frozenset()) -> list[Result]:
    """Run every (name, cmd) with at most `jobs` at once. Results come back in input order, whatever order the
    commands finish in, so two runs of the same list print the same report.
    Threads are enough: each thread just waits on a child process, so the GIL is not the limit."""
    if jobs < 1:
        raise ValueError("jobs must be >= 1")
    if timeout <= 0:
        raise ValueError("timeout must be > 0")
    names = [n for n, _ in commands]
    if len(set(names)) != len(names):
        raise ValueError("command names must be unique")
    transient = frozenset(transient)
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = [pool.submit(run_with_retries, n, c, timeout, retries, transient) for n, c in commands]
        return [f.result() for f in futures]


# ---------------------------------------------------------------- Part 4: summary


def summarize(results: list[Result], wall: float | None = None) -> str:
    lines = []
    for r in results:
        code = "-" if r.returncode is None else str(r.returncode)
        lines.append(f"{r.status.upper():8s} {r.name:20s} rc={code:>4s} attempts={len(r.attempts)} {r.seconds:6.2f}s")
    counts = {s: sum(r.status == s for r in results) for s in ("pass", "fail", "timeout")}
    retried = sum(len(r.attempts) > 1 for r in results)
    total = sum(r.seconds for r in results)
    tail = f", wall {wall:.2f}s" if wall is not None else ""
    lines.append(f"{len(results)} commands: {counts['pass']} passed, {counts['fail']} failed, "
                 f"{counts['timeout']} timed out, {retried} retried; sum of durations {total:.2f}s{tail}")
    slowest = sorted(results, key=lambda r: -r.seconds)[:3]
    if slowest:
        lines.append("slowest: " + ", ".join(f"{r.name} {r.seconds:.2f}s" for r in slowest))
    return "\n".join(lines)


def parse_commands(text: str) -> list[tuple[str, str]]:
    out = []
    for i, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, sep, cmd = line.partition(":")
        if not sep or not cmd.strip():
            raise ValueError(f"line {i}: expected 'name: command'")
        out.append((name.strip(), cmd.strip()))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout", type=float, default=60)
    ap.add_argument("--retries", type=int, default=0)
    ap.add_argument("--transient", type=int, nargs="*", default=[])
    a = ap.parse_args(argv)
    with open(a.file) as f:
        commands = parse_commands(f.read())
    start = time.monotonic()
    results = run_all(commands, a.jobs, a.timeout, a.retries, set(a.transient))
    print(summarize(results, time.monotonic() - start))
    return 0 if all(r.status == "pass" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
