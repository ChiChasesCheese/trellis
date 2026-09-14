"""Retry wrapper around a single fetch call: retries a failed fetch a fixed number of times,
waiting longer between each attempt (exponential backoff) so a struggling server gets breathing
room instead of an immediate hammering.

`asyncio.sleep(delay)` is itself an `await` point -- while one coroutine is sleeping here, the
event loop is free to run any other coroutine that's ready, including other fetches started by
the same crawler run.
"""

from __future__ import annotations

import asyncio

from .http_client import FetchError, fetch_url


async def fetch_with_retry(
    url: str,
    *,
    retries: int = 3,
    backoff_base: float = 0.05,
    backoff_cap: float | None = 2.0,
    fetch=fetch_url,
):
    """Call `fetch(url)` up to `retries` times in total, doubling the delay between attempts
    starting from `backoff_base` seconds and never exceeding `backoff_cap` seconds (pass `None`
    for an uncapped, ever-doubling delay -- not recommended against a real server, but useful in
    tests that want to see the raw doubling sequence). Returns the first successful result;
    re-raises the last `FetchError` if every attempt fails."""
    attempt = 0
    delay = backoff_base
    while True:
        try:
            return await fetch(url)
        except FetchError:
            attempt += 1
            if attempt >= retries:
                raise
            await asyncio.sleep(delay)
            delay *= 2
            if backoff_cap is not None:
                delay = min(delay, backoff_cap)
