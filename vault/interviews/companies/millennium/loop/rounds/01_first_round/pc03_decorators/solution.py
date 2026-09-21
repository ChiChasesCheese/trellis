"""pc03 Decorators -- reference solution.

Four decorators, each a standard interview shape:

Part1: `timed` and `memoize` are plain (unparametrised) decorators -- `def deco(func): ...` --
the baseline every candidate should be able to write cold, including `functools.wraps` so the
wrapped function keeps its `__name__`/`__doc__` (without it, stacking two decorators or
introspecting the function at runtime silently breaks).

Part2: `retry` is a *parametrised* decorator -- a factory that takes arguments and returns the
actual decorator (`def retry(times, ...): def decorator(func): def wrapper(...): ...`). `sleep`
is injected so tests never actually sleep.

Part3 (reconstructed): `rate_limited` is a stateful class-based decorator (state -- the sliding
window of call timestamps -- lives on the decorator instance, not the wrapped function), with an
injectable `clock` for determinism, same "lazy eviction on the next call" idiom as a token-bucket
rate limiter.
"""

from __future__ import annotations

import functools
import sys
import time
from collections import deque
from typing import Callable


# --------------------------------------------------------------------------- Part 1
def timed(func: Callable) -> Callable:
    """Wraps `func`; after each call, `wrapper.last_seconds` holds that call's wall-clock
    duration (time.perf_counter based). Preserves __name__/__doc__ via functools.wraps."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        wrapper.last_seconds = time.perf_counter() - start
        return result

    wrapper.last_seconds = 0.0
    return wrapper


def memoize(func: Callable) -> Callable:
    """Caches results by (args, sorted(kwargs.items())); both must be hashable. Exposes
    `wrapper.hits` / `wrapper.misses` (call counters) and `wrapper.cache_clear()`. Preserves
    __name__/__doc__ via functools.wraps."""
    cache: dict = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            wrapper.hits += 1
        else:
            cache[key] = func(*args, **kwargs)
            wrapper.misses += 1
        return cache[key]

    wrapper.hits = 0
    wrapper.misses = 0

    def _clear():
        cache.clear()
        wrapper.hits = 0
        wrapper.misses = 0

    wrapper.cache_clear = _clear
    return wrapper


# --------------------------------------------------------------------------- Part 2
def retry(
    times: int,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
    backoff: float | Callable[[int], float] = 0,
    sleep: Callable[[float], None] = lambda s: None,
) -> Callable[[Callable], Callable]:
    """Parametrised decorator factory. The wrapped call is attempted up to `times` times total
    (>= 1); only exceptions matching `exceptions` are retried, anything else propagates on the
    first attempt. Between failed attempts, calls `sleep(delay)` where `delay = backoff(attempt)`
    if `backoff` is callable, else the constant `backoff`. Raises the last exception once
    attempts are exhausted. `wrapper.attempts` holds the attempt count used by the most recent
    call. `times < 1` raises ValueError immediately (at decoration time, not call time)."""
    if times < 1:
        raise ValueError(f"times must be >= 1, got {times}")

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc: BaseException | None = None
            for attempt in range(1, times + 1):
                try:
                    result = func(*args, **kwargs)
                    wrapper.attempts = attempt
                    return result
                except exceptions as exc:
                    last_exc = exc
                    wrapper.attempts = attempt
                    if attempt < times:
                        delay = backoff(attempt) if callable(backoff) else backoff
                        sleep(delay)
            assert last_exc is not None
            raise last_exc

        wrapper.attempts = 0
        return wrapper

    return decorator


def make_flaky(fail_times: int) -> Callable[[], str]:
    """Returns a zero-arg function with its own private call counter: it raises ValueError on
    each of its first `fail_times` calls, then returns "ok" on every call after that."""
    state = {"calls": 0}

    def flaky() -> str:
        state["calls"] += 1
        if state["calls"] <= fail_times:
            raise ValueError(f"transient failure #{state['calls']}")
        return "ok"

    return flaky


# --------------------------------------------------------------------------- Part 3 (reconstructed)
class RateLimitExceeded(Exception):
    """Raised when a rate_limited-wrapped call happens too often."""


def rate_limited(
    n: int, per_seconds: float, clock: Callable[[], float] = time.monotonic
) -> Callable[[Callable], Callable]:
    """Class-based stateful decorator: at most `n` calls in any trailing window of
    `per_seconds`, evaluated as the half-open interval `(clock() - per_seconds, clock()]` (same
    lazy-eviction idiom as a sliding-window rate limiter -- expired timestamps are dropped on the
    next call, not on a timer). Raises RateLimitExceeded instead of calling `func` when the
    window is already full. `n < 1` or `per_seconds <= 0` raises ValueError immediately."""
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    if per_seconds <= 0:
        raise ValueError(f"per_seconds must be > 0, got {per_seconds}")

    class _RateLimiter:
        def __init__(self, func: Callable) -> None:
            functools.update_wrapper(self, func)
            self._func = func
            self._calls: deque[float] = deque()

        def __call__(self, *args, **kwargs):
            now = clock()
            while self._calls and now - self._calls[0] >= per_seconds:
                self._calls.popleft()
            if len(self._calls) >= n:
                raise RateLimitExceeded(f"more than {n} calls within {per_seconds}s")
            self._calls.append(now)
            return self._func(*args, **kwargs)

    def decorator(func: Callable) -> Callable:
        return _RateLimiter(func)

    return decorator


# --------------------------------------------------------------------------- line-driven wrappers
def part1(lines: list[str]) -> list[str]:
    """Each line is one command:
    'MEMO <a> <b>'  -> call a memoized two-arg add(a, b), print the sum
    'MEMO CALLS'    -> print how many times the underlying add() actually ran (proves caching)
    'TIMED <x>'     -> call a timed one-arg square(x), print the result
    """
    calls = {"add": 0}

    def _add(a: int, b: int) -> int:
        calls["add"] += 1
        return a + b

    def _square(x: int) -> int:
        return x * x

    memo_add = memoize(_add)
    timed_square = timed(_square)

    out = []
    for line in lines:
        parts = line.split()
        if parts[0] == "MEMO" and parts[1] == "CALLS":
            out.append(str(calls["add"]))
        elif parts[0] == "MEMO":
            out.append(str(memo_add(int(parts[1]), int(parts[2]))))
        elif parts[0] == "TIMED":
            out.append(str(timed_square(int(parts[1]))))
        else:
            raise ValueError(f"unknown command {line!r}")
    return out


def part2(lines: list[str]) -> list[str]:
    """Each line: 'RETRY <times> <fail_times>' -> build a fresh flaky() with `fail_times`
    failures, wrap it with retry(times, exceptions=(ValueError,)), call it once, print
    'ok <attempts>' or 'error <ExceptionType> <attempts>'."""
    out = []
    for line in lines:
        _, times_s, fail_s = line.split()
        flaky = make_flaky(int(fail_s))
        wrapped = retry(int(times_s), exceptions=(ValueError,))(flaky)
        try:
            wrapped()
            out.append(f"ok {wrapped.attempts}")
        except ValueError as exc:
            out.append(f"error {type(exc).__name__} {wrapped.attempts}")
    return out


def part3(lines: list[str]) -> list[str]:
    """First line: 'LIMIT <n> <per_seconds>'. Each following line: 'CALL <t>' -> advance a fake
    clock to `t` and invoke a rate_limited(n, per_seconds)-wrapped no-op, printing 'ok' or
    'limited'."""
    if not lines or not lines[0].startswith("LIMIT "):
        raise ValueError("part3 input must start with 'LIMIT <n> <per_seconds>'")
    _, n_s, per_s = lines[0].split()
    current = [0.0]
    limited_noop = rate_limited(int(n_s), float(per_s), clock=lambda: current[0])(lambda: "ok")

    out = []
    for line in lines[1:]:
        _, t_s = line.split()
        current[0] = float(t_s)
        try:
            limited_noop()
            out.append("ok")
        except RateLimitExceeded:
            out.append("limited")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
