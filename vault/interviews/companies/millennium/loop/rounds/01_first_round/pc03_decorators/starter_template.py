"""pc03 Decorators -- YOUR implementation. Run tests against this file with IMPL=starter.

timed / memoize (plain decorators) -> retry (parametrised decorator factory) -> rate_limited
(stateful class-based decorator with an injectable clock).
"""

from __future__ import annotations

import functools
import sys
import time
from collections import deque
from typing import Callable


def timed(func: Callable) -> Callable:
    """Part1: wraps func; wrapper.last_seconds holds the most recent call's duration.
    Preserve __name__/__doc__ (functools.wraps)."""
    # TODO
    return func


def memoize(func: Callable) -> Callable:
    """Part1: caches by (args, sorted(kwargs.items())). Exposes wrapper.hits / wrapper.misses
    and wrapper.cache_clear(). Preserve __name__/__doc__."""
    # TODO
    return func


def retry(
    times: int,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
    backoff: float | Callable[[int], float] = 0,
    sleep: Callable[[float], None] = lambda s: None,
) -> Callable[[Callable], Callable]:
    """Part2: parametrised decorator factory. `times < 1` -> ValueError immediately. Retries up
    to `times` attempts total; only `exceptions` are retried; calls sleep(delay) between failed
    attempts (delay = backoff(attempt) if callable else backoff); wrapper.attempts holds the
    most recent call's attempt count; re-raises the last exception once attempts are exhausted."""
    # TODO
    def decorator(func):
        return func

    return decorator


def make_flaky(fail_times: int) -> Callable[[], str]:
    """Returns a zero-arg function that raises ValueError on each of its first `fail_times`
    calls (own private counter), then returns "ok" forever after."""
    # TODO
    def flaky():
        return "ok"

    return flaky


class RateLimitExceeded(Exception):
    """Raised when a rate_limited-wrapped call happens too often."""


def rate_limited(
    n: int, per_seconds: float, clock: Callable[[], float] = time.monotonic
) -> Callable[[Callable], Callable]:
    """Part3 (reconstructed): stateful class-based decorator. At most `n` calls within any
    trailing `per_seconds` window (half-open: `(clock() - per_seconds, clock()]`), expired
    timestamps evicted lazily on the next call. Raises RateLimitExceeded when the window is
    full. `n < 1` or `per_seconds <= 0` -> ValueError immediately."""
    # TODO
    def decorator(func):
        return func

    return decorator


def part1(lines: list[str]) -> list[str]:
    """'MEMO <a> <b>' -> memoized add(a, b); 'MEMO CALLS' -> underlying-call count;
    'TIMED <x>' -> timed square(x)."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """'RETRY <times> <fail_times>' -> 'ok <attempts>' or 'error <ExceptionType> <attempts>'."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """First line 'LIMIT <n> <per_seconds>'; each following 'CALL <t>' -> 'ok' or 'limited'."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
