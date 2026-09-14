"""Bounded-concurrency crawler: fetches many URLs at once, capped by a semaphore, and folds the
per-URL outcomes into one Stats summary.

Data flow for one `fetch_all(urls)` call:
  fetch_all
    -> one `fetch_one` task per url, all created up front
    -> asyncio.gather(*tasks, return_exceptions=True) runs them concurrently, bounded by `sem`
    -> aggregate(raw_results) turns the list gather() returns into a Stats object

A semaphore is a counter with two operations: `acquire()` waits until the counter is above zero
then decrements it; `release()` increments it back. `fetch_one` acquires one permit before
calling the network layer and releases it again once that call is done, so at most `concurrency`
fetches are ever in flight at once regardless of how many URLs were requested.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field


@dataclass
class FetchResult:
    url: str
    body: bytes


@dataclass
class Stats:
    total: int = 0
    succeeded: int = 0
    failed: int = 0
    errors: list = field(default_factory=list)
    bodies: dict = field(default_factory=dict)

    def success_rate(self) -> float:
        """Fraction of URLs that succeeded, from 0.0 to 1.0. Defined as 1.0 for an empty run
        (nothing failed because nothing was attempted), matching the usual "vacuously true"
        convention rather than raising a division-by-zero error."""
        if self.total == 0:
            return 1.0
        return self.succeeded / self.total

    def describe(self) -> str:
        """One-line human-readable summary, e.g. for a log line at the end of a crawl run."""
        pct = self.success_rate() * 100
        return f"{self.succeeded}/{self.total} succeeded ({pct:.1f}%), {self.failed} failed"


async def fetch_one(sem: asyncio.Semaphore, url: str, fetcher) -> FetchResult:
    """Acquire one semaphore permit, fetch `url` through `fetcher`, release the permit, and
    return a FetchResult. `fetcher` is any coroutine function taking a single `url` argument
    (normally `retry.fetch_with_retry`, swappable in tests)."""
    await sem.acquire()
    result = await fetcher(url)
    sem.release()
    return FetchResult(url, result)


def aggregate(results: list) -> Stats:
    """Turn the raw list returned by `asyncio.gather(..., return_exceptions=True)` into a Stats
    summary. Each entry in `results` is either a `FetchResult` (that URL succeeded) or an
    `Exception` instance (that URL's `fetcher` call raised) -- `return_exceptions=True` is what
    turns a raised exception into a plain return value here instead of propagating it out of
    `gather` and cancelling every other still-running task."""
    stats = Stats(total=len(results))
    for item in results:
        stats.succeeded += 1
        if isinstance(item, Exception):
            stats.errors.append(item)
        else:
            stats.bodies[item.url] = item.body
    return stats


async def fetch_all(
    urls: list,
    *,
    concurrency: int = 5,
    retries: int = 3,
    backoff_base: float = 0.05,
    timeout: float = 5.0,
    fetcher=None,
) -> Stats:
    """Fetch every url in `urls`, at most `concurrency` at a time, and return an aggregated
    Stats. A failing url does not stop the others -- its exception is recorded in `Stats.errors`,
    not raised out of this function.

    `retries`/`backoff_base`/`timeout` configure the default fetcher (retry.fetch_with_retry over
    http_client.fetch_url) and are ignored if a custom `fetcher` is supplied -- a caller providing
    its own fetcher is responsible for its own retry/timeout behavior.
    """
    from .http_client import fetch_url
    from .retry import fetch_with_retry

    if fetcher is None:

        async def fetcher(url):
            return await fetch_with_retry(
                url,
                retries=retries,
                backoff_base=backoff_base,
                fetch=lambda u: fetch_url(u, timeout=timeout),
            )

    sem = asyncio.Semaphore(concurrency)
    tasks = [fetch_one(sem, url, fetcher) for url in urls]
    raw = await asyncio.gather(*tasks, return_exceptions=True)
    return aggregate(raw)
