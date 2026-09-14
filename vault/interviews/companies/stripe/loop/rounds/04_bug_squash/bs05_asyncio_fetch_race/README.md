# fetchrace — a small bounded-concurrency async fetcher

`fetchrace` fetches a list of URLs concurrently with `asyncio`, capped by a `Semaphore` so at most
`concurrency` requests are ever in flight at once, retrying each URL with exponential backoff
before giving up on it, and folding every outcome (success or failure) into one `Stats` summary —
a failing URL doesn't stop the others or blow up the whole run.

## Layout
```
src/fetchrace/
  http_client.py   fetch_url(url): one GET, run on a worker thread via run_in_executor,
                   raises FetchError on any network failure or non-2xx/3xx status
  retry.py         fetch_with_retry(url): retries fetch_url with exponential backoff
  crawler.py       fetch_one() (one URL, semaphore-bounded), aggregate() (raw results ->
                   Stats), fetch_all() (the public entry point: many URLs -> one Stats)
tests/
  support/server.py   a tiny local http.server used as the thing being fetched (not part
                       of the library -- test infrastructure, same role as loop/mockserver/)
  test_http_client.py fetch_url() against the local server: success, 500, connection refused
  test_retry.py       fetch_with_retry() recovering from a flaky endpoint, giving up cleanly
  test_crawler.py     aggregate() in isolation, and fetch_all() end to end
```

## Running the tests
```
python -m pytest tests -q
```
Most tests pass as shipped. Two do not — see the issue below.

## The issue (as filed against this repo)

**Bug report 1 — `fetch_all()` hangs forever once enough URLs fail under low concurrency**

> Repro:
> ```python
> import asyncio
> from fetchrace.crawler import fetch_all
>
> async def fetcher(url):
>     if url in ("u1", "u2"):
>         raise RuntimeError("simulated failure")
>     return b"ok"
>
> asyncio.run(fetch_all(["u1", "u2", "u3", "u4"], concurrency=2, fetcher=fetcher))
> ```
> Expected: completes quickly with a `Stats` showing 2 successes and 2 failures — a failing URL
> shouldn't be able to affect the other URLs' ability to run.
>
> Actual: this never returns. With `concurrency=2` and the first two URLs both failing, the third
> and fourth URLs simply never get a turn — something about a failure is eating one of the two
> concurrency slots permanently instead of giving it back.
>
> This isn't intermittent — with these exact four URLs and `concurrency=2`, it hangs on every
> single run, not just sometimes.

**Bug report 2 — failed fetches are counted as successes in the final `Stats`**

> We changed nothing about how many URLs we're fetching, but after a routine deploy our success
> rate metric jumped to what looks like 100% even on runs where we know some URLs are failing
> (we can see the failures land in `Stats.errors`). `Stats.succeeded` is counting entries that are
> also present in `Stats.errors`, which shouldn't be possible — an outcome should be exactly one
> of "succeeded" or "failed," never both.
>
> Repro: call `aggregate()` directly with a hand-built list containing one real result and one
> exception. Expected: `stats.succeeded == 1`, `stats.failed == 1`. Actual: `stats.succeeded == 2`,
> `stats.failed == 0`.

If you get stuck: both bugs are narrowly scoped to one function each (`crawler.py`'s `fetch_one`;
`crawler.py`'s `aggregate`) — if your fix touches `retry.py`, `http_client.py`, or the shape of
`fetch_all` itself, you've drifted from the actual bug into a redesign. Come back to the failing
assertion and follow it.
