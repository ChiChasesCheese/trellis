"""crawler tests: aggregate() in isolation (no asyncio involved at all), fetch_all() against the
local test server for the happy path, and fetch_all() under induced failures to check that the
semaphore's concurrency limit survives a failing fetch.
"""

import asyncio

from fetchrace.crawler import FetchResult, aggregate, fetch_all


# ---------------------------------------------------------------- aggregate() (no asyncio)
def test_aggregate_counts_a_pure_success_list():
    results = [FetchResult("a", b"A"), FetchResult("b", b"B")]
    stats = aggregate(results)
    assert stats.total == 2
    assert stats.succeeded == 2
    assert stats.failed == 0
    assert stats.bodies == {"a": b"A", "b": b"B"}
    assert stats.errors == []


def test_aggregate_separates_exceptions_from_successes():
    boom = ValueError("boom")
    results = [FetchResult("a", b"A"), boom, FetchResult("b", b"B")]
    stats = aggregate(results)
    assert stats.total == 3
    assert stats.succeeded == 2
    assert stats.failed == 1
    assert stats.errors == [boom]
    assert stats.bodies == {"a": b"A", "b": b"B"}


def test_aggregate_of_empty_list_is_all_zero():
    stats = aggregate([])
    assert stats.total == 0
    assert stats.succeeded == 0
    assert stats.failed == 0


def test_stats_success_rate_and_describe_on_a_clean_run():
    stats = aggregate([FetchResult("a", b"A"), FetchResult("b", b"B")])
    assert stats.success_rate() == 1.0
    assert stats.describe() == "2/2 succeeded (100.0%), 0 failed"


def test_stats_success_rate_of_empty_run_is_one():
    stats = aggregate([])
    assert stats.success_rate() == 1.0


# ---------------------------------------------------------------- fetch_all(): happy path
def test_fetch_all_against_real_server_returns_every_body(http_server):
    urls = [f"{http_server}/ok/{i}" for i in range(5)]

    stats = asyncio.run(fetch_all(urls, concurrency=2))

    assert stats.total == 5
    assert stats.succeeded == 5
    assert stats.failed == 0
    for i in range(5):
        assert stats.bodies[f"{http_server}/ok/{i}"] == f"ok:{i}".encode()


def test_fetch_all_forwards_retry_options_to_its_default_fetcher(http_server):
    """No custom fetcher is given here, so fetch_all must build its own default fetcher out of
    the retries/backoff_base it was given -- against /flaky/<id> (fails twice, then succeeds per
    tests/support/server.py), 2 retries is not enough but 3 is."""
    url = f"{http_server}/flaky/only-two-retries"
    stats = asyncio.run(fetch_all([url], retries=2, backoff_base=0.01, fetcher=None))
    assert len(stats.errors) == 1
    assert stats.bodies == {}

    url = f"{http_server}/flaky/three-retries"
    stats = asyncio.run(fetch_all([url], retries=3, backoff_base=0.01, fetcher=None))
    assert stats.errors == []
    assert stats.bodies == {url: b"ok:three-retries"}


def test_fetch_all_with_a_fake_fetcher_and_no_failures():
    async def fetcher(url):
        return f"body-for-{url}".encode()

    urls = ["u1", "u2", "u3"]
    stats = asyncio.run(fetch_all(urls, concurrency=2, fetcher=fetcher))

    assert stats.succeeded == 3
    assert stats.failed == 0
    assert stats.bodies["u2"] == b"body-for-u2"


# ---------------------------------------------------------------- fetch_all(): failures under contention
def test_fetch_all_does_not_deadlock_when_some_urls_fail_under_low_concurrency():
    """concurrency=2 with two starter permits; u1 and u2 always fail. If a failed fetch doesn't
    give its permit back, the semaphore is left with 0 permits and u3/u4 can never acquire one --
    fetch_all() would then hang forever, so this wraps it in a timeout. Because asyncio runs one
    coroutine at a time on a single thread, this reproduces identically on every run: it isn't a
    matter of how the OS happens to schedule anything."""

    async def fetcher(url):
        if url in ("u1", "u2"):
            raise RuntimeError(f"simulated failure for {url}")
        return b"ok"

    async def scenario():
        urls = ["u1", "u2", "u3", "u4"]
        return await asyncio.wait_for(fetch_all(urls, concurrency=2, fetcher=fetcher), timeout=0.5)

    stats = asyncio.run(scenario())

    assert stats.total == 4
    assert stats.succeeded == 2
    assert stats.failed == 2
