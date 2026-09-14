"""fetch_with_retry tests: recovers from a server that fails a few times then succeeds, and
gives up cleanly once retries are exhausted."""

import asyncio

from fetchrace.http_client import FetchError
from fetchrace.retry import fetch_with_retry


def test_retries_until_the_flaky_endpoint_succeeds(http_server):
    """The test server's /flaky/<id> route (see tests/support/server.py) fails the first
    `fail_times` (2, by default) requests to a given id, then succeeds -- fetch_with_retry's
    default of 3 retries should be just enough to ride that out."""

    async def scenario():
        return await fetch_with_retry(f"{http_server}/flaky/abc", backoff_base=0.01)

    assert asyncio.run(scenario()) == b"ok:abc"


def test_gives_up_after_exhausting_retries(http_server):
    async def scenario():
        return await fetch_with_retry(f"{http_server}/always-fail", retries=2, backoff_base=0.01)

    try:
        asyncio.run(scenario())
    except FetchError:
        pass
    else:
        raise AssertionError("expected FetchError once retries are exhausted")


def test_stops_retrying_as_soon_as_a_call_succeeds():
    calls = []

    async def fetcher(url):
        calls.append(url)
        return b"first try worked"

    async def scenario():
        return await fetch_with_retry("http://example.invalid", backoff_base=0.01, fetch=fetcher)

    assert asyncio.run(scenario()) == b"first try worked"
    assert calls == ["http://example.invalid"]
