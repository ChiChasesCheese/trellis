"""pc02 Async Paginated API Ingestion -- YOUR implementation. Run the tests against this file
with IMPL=starter.

fetch_page(page: int) -> Awaitable[{"items": list[str], "total_pages": int}] is the injected
async HTTP client stand-in; page is 1-based and total_pages is only reliably known after page 1.
"""
from __future__ import annotations

import asyncio
import sys
from typing import Awaitable, Callable

PageResult = dict
FetchPage = Callable[[int], Awaitable[PageResult]]


class TransientError(Exception):
    """Raised by an injected fetch_page to simulate a retryable failure."""


async def fetch_all_sequential(fetch_page: FetchPage) -> list[str]:
    """Part1: page 1, 2, ... in order. ValueError if total_pages < 1."""
    # TODO
    return []


async def fetch_all_concurrent(fetch_page: FetchPage, max_concurrency: int) -> list[str]:
    """Part2: page 1 first, then pages 2..total_pages concurrently (asyncio.Semaphore bound),
    output assembled in PAGE ORDER regardless of completion order. ValueError if
    max_concurrency < 1 or total_pages < 1."""
    # TODO
    return []


async def fetch_all_with_retry(
    fetch_page: FetchPage,
    max_concurrency: int = 1,
    max_retries: int = 3,
    base_delay: float = 0.1,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> list[str]:
    """Part3: like fetch_all_concurrent, plus exponential-backoff retry on TransientError (other
    exceptions propagate unretried) and idempotent de-dup of items (first-seen order, by page then
    within-page position). ValueError if max_concurrency < 1 or max_retries < 0."""
    # TODO
    return []


def part1(lines: list[str]) -> list[str]:
    """lines[0] = '<total_pages>', then one page per line ('-' for an empty page, else
    comma-separated items)."""
    # TODO
    return []


def part2(lines: list[str]) -> list[str]:
    """lines[0] = '<total_pages> <max_concurrency>', then one page per line."""
    # TODO
    return []


def part3(lines: list[str]) -> list[str]:
    """lines[0] = '<total_pages> <max_concurrency> <max_retries>', then one page per line:
    '<items>|<fail_times>'."""
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
