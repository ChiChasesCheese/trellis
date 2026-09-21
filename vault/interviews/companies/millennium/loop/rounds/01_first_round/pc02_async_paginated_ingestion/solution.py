"""pc02 Async Paginated API Ingestion -- reference solution.

The interview can't have a candidate hit a real network from a HackerRank sandbox, so every
report abstracts the HTTP client into an injectable async function:

    fetch_page(page: int) -> {"items": list[str], "total_pages": int}

`total_pages` is only meaningful on page 1's response (real paginated APIs put the total count /
total pages on the first response, or in a response header) -- later pages just echo it back so
callers don't have to special-case "did we already learn total_pages".

Part1 walks pages 1..total_pages one coroutine at a time: `await` blocks until each page lands
before starting the next, so output order is trivially page order.
Part2 is the interview follow-up ("asyncio -- write working code and explain how coroutines
work"): fetch page 1 first (there is no other way to learn total_pages), then fan out pages
2..total_pages behind an asyncio.Semaphore(max_concurrency) with asyncio.gather, but assemble the
final list by PAGE INDEX, not completion order -- a slow page 2 must never let a fast page 7 jump
ahead of it in the output. This is also the fix for the paired report "Debug missing output in
Python async HTTP flow": the classic bug is building the output list by *appending* inside each
task in whatever order they happen to finish, which is exactly what "missing" (really:
misordered/nondeterministic) output looks like under concurrency.
Part3 (reconstructed) adds exponential-backoff retry on a `TransientError` (any other exception
still propagates unretried) and idempotent de-duplication of items, because retries -- and, more
generally, any at-least-once delivery -- can hand the same item back twice.
"""
from __future__ import annotations

import asyncio
import sys
from typing import Awaitable, Callable

PageResult = dict  # {"items": list[str], "total_pages": int}
FetchPage = Callable[[int], Awaitable[PageResult]]


class TransientError(Exception):
    """Raised by an injected fetch_page to simulate a retryable failure (timeout, 5xx, ...)."""


# --------------------------------------------------------------------------- Part 1
async def fetch_all_sequential(fetch_page: FetchPage) -> list[str]:
    """Page 1, 2, ... in order, one `await` at a time. No concurrency -- output order is simply
    the order pages were requested."""
    first = await fetch_page(1)
    total_pages = first["total_pages"]
    if total_pages < 1:
        raise ValueError(f"total_pages must be >= 1, got {total_pages!r}")
    items: list[str] = list(first["items"])
    for page in range(2, total_pages + 1):
        result = await fetch_page(page)
        items.extend(result["items"])
    return items


# --------------------------------------------------------------------------- Part 2
async def fetch_all_concurrent(fetch_page: FetchPage, max_concurrency: int) -> list[str]:
    """Fetch page 1 first to learn total_pages, then fetch pages 2..total_pages concurrently,
    bounded by asyncio.Semaphore(max_concurrency). Results are written into a pre-sized list
    indexed by page number, so the final concatenation is in page order regardless of which
    coroutine happens to finish first."""
    if max_concurrency < 1:
        raise ValueError("max_concurrency must be >= 1")
    first = await fetch_page(1)
    total_pages = first["total_pages"]
    if total_pages < 1:
        raise ValueError(f"total_pages must be >= 1, got {total_pages!r}")

    pages_items: list[list[str]] = [list(first["items"])] + [[] for _ in range(total_pages - 1)]
    if total_pages > 1:
        semaphore = asyncio.Semaphore(max_concurrency)

        async def _fetch(page: int) -> None:
            async with semaphore:
                result = await fetch_page(page)
                pages_items[page - 1] = result["items"]

        await asyncio.gather(*(_fetch(page) for page in range(2, total_pages + 1)))

    items: list[str] = []
    for page_items in pages_items:
        items.extend(page_items)
    return items


# --------------------------------------------------------------------------- Part 3 (reconstructed)
async def fetch_all_with_retry(
    fetch_page: FetchPage,
    max_concurrency: int = 1,
    max_retries: int = 3,
    base_delay: float = 0.1,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> list[str]:
    """Same page-order-preserving concurrent pipeline as Part2, plus:
    - retry: a TransientError from fetch_page is retried up to `max_retries` times with
      exponential backoff (`base_delay * 2**attempt`, via the injectable `sleep` so tests never
      really wait); any other exception propagates immediately, unretried.
    - idempotent de-dup: items are merged in page order, first-seen order within that; an item
      value already emitted (from an earlier page, or a superseded earlier delivery of the same
      page) is dropped instead of appended again.
    """
    if max_concurrency < 1:
        raise ValueError("max_concurrency must be >= 1")
    if max_retries < 0:
        raise ValueError("max_retries must be >= 0")

    async def _fetch_with_retry(page: int) -> PageResult:
        attempt = 0
        while True:
            try:
                return await fetch_page(page)
            except TransientError:
                if attempt >= max_retries:
                    raise
                await sleep(base_delay * (2 ** attempt))
                attempt += 1

    first = await _fetch_with_retry(1)
    total_pages = first["total_pages"]
    if total_pages < 1:
        raise ValueError(f"total_pages must be >= 1, got {total_pages!r}")

    pages_items: list[list[str]] = [list(first["items"])] + [[] for _ in range(total_pages - 1)]
    if total_pages > 1:
        semaphore = asyncio.Semaphore(max_concurrency)

        async def _fetch(page: int) -> None:
            async with semaphore:
                result = await _fetch_with_retry(page)
                pages_items[page - 1] = result["items"]

        await asyncio.gather(*(_fetch(page) for page in range(2, total_pages + 1)))

    items: list[str] = []
    seen: set[str] = set()
    for page_items in pages_items:
        for item in page_items:
            if item not in seen:
                seen.add(item)
                items.append(item)
    return items


# --------------------------------------------------------------------------- line-driven wrappers
def _parse_items(field: str) -> list[str]:
    """'-' encodes an empty page (a real blank line would be stripped by main()'s blank-line
    filter, so '-' is the explicit "no items" token)."""
    return [] if field == "-" else field.split(",")


def _take_page_lines(lines: list[str], total_pages: int, start: int) -> list[str]:
    page_lines = lines[start : start + total_pages]
    if len(page_lines) != total_pages:
        raise ValueError(f"expected {total_pages} page lines, got {len(page_lines)}")
    return page_lines


def part1(lines: list[str]) -> list[str]:
    """lines[0] = '<total_pages>', then one page per line ('-' or comma-separated items)."""
    if not lines:
        raise ValueError("missing '<total_pages>' header line")
    total_pages = int(lines[0].strip())
    if total_pages < 1:
        raise ValueError("total_pages must be >= 1")
    pages = [_parse_items(pl) for pl in _take_page_lines(lines, total_pages, 1)]

    async def fetch_page(page: int) -> PageResult:
        return {"items": pages[page - 1], "total_pages": total_pages}

    return asyncio.run(fetch_all_sequential(fetch_page))


def part2(lines: list[str]) -> list[str]:
    """lines[0] = '<total_pages> <max_concurrency>', then one page per line."""
    if not lines:
        raise ValueError("missing header line")
    header = lines[0].split()
    if len(header) != 2:
        raise ValueError("first line must be '<total_pages> <max_concurrency>'")
    total_pages, max_concurrency = int(header[0]), int(header[1])
    if total_pages < 1:
        raise ValueError("total_pages must be >= 1")
    pages = [_parse_items(pl) for pl in _take_page_lines(lines, total_pages, 1)]

    async def fetch_page(page: int) -> PageResult:
        return {"items": pages[page - 1], "total_pages": total_pages}

    return asyncio.run(fetch_all_concurrent(fetch_page, max_concurrency))


def part3(lines: list[str]) -> list[str]:
    """lines[0] = '<total_pages> <max_concurrency> <max_retries>', then one page per line:
    '<items>|<fail_times>' -- the page raises TransientError `fail_times` times before it
    succeeds. Retries here never really sleep (base_delay=0, a no-op injected `sleep`) since the
    io wrapper's job is to exercise the wiring, not real backoff timing (that's covered by
    dedicated unit tests with an instrumented fake sleep)."""
    if not lines:
        raise ValueError("missing header line")
    header = lines[0].split()
    if len(header) != 3:
        raise ValueError("first line must be '<total_pages> <max_concurrency> <max_retries>'")
    total_pages, max_concurrency, max_retries = int(header[0]), int(header[1]), int(header[2])
    if total_pages < 1:
        raise ValueError("total_pages must be >= 1")
    page_lines = _take_page_lines(lines, total_pages, 1)
    specs: list[tuple[list[str], int]] = []
    for pl in page_lines:
        items_part, _, fail_part = pl.partition("|")
        specs.append((_parse_items(items_part), int(fail_part) if fail_part else 0))
    attempts = {page: 0 for page in range(1, total_pages + 1)}

    async def fetch_page(page: int) -> PageResult:
        items, fail_times = specs[page - 1]
        if attempts[page] < fail_times:
            attempts[page] += 1
            raise TransientError(f"simulated transient failure on page {page}")
        return {"items": items, "total_pages": total_pages}

    async def _no_sleep(_seconds: float) -> None:
        return None

    return asyncio.run(
        fetch_all_with_retry(
            fetch_page, max_concurrency, max_retries, base_delay=0.0, sleep=_no_sleep
        )
    )


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln for ln in stdin.read().splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("PART "):
        raise ValueError("first line must be 'PART <n>'")
    n = int(lines[0].split()[1])
    out = {1: part1, 2: part2, 3: part3}[n](lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
