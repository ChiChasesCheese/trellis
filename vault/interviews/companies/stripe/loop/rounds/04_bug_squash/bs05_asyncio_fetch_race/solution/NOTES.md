# bs05 fetchrace — solution notes (not shown to the candidate; read after `ref`)

## Bug 1 — `crawler.py`: `fetch_one` releases the semaphore only on the success path

The buggy implementation:
```python
async def fetch_one(sem, url, fetcher):
    await sem.acquire()
    result = await fetcher(url)   # if this raises, we never reach the line below
    sem.release()
    return FetchResult(url, result)
```
`sem.release()` is written as a plain statement after the call to `fetcher(url)`, not in a
`finally` block. If `fetcher(url)` raises (which it will, for any URL that exhausts its retries in
`fetch_with_retry`, or for a fake fetcher a test wires up to simulate a failure), the coroutine
propagates that exception straight out of `fetch_one` without ever executing `sem.release()`. The
permit that `sem.acquire()` took is gone for good — the semaphore's internal counter is now
permanently one lower than it should be.

Because `fetch_all` wraps every `fetch_one` call in `asyncio.gather(..., return_exceptions=True)`,
an individual failure doesn't crash the whole run or even look alarming in isolation — the
`Exception` just becomes one more entry in the results list. The problem only becomes visible once
enough failures have accumulated to exhaust the semaphore's starting permit count: at that point,
every *remaining* `fetch_one` call blocks forever on `await sem.acquire()`, because nothing is
ever going to call `release()` again to give a permit back. `asyncio.gather` then never completes,
because it's waiting on tasks that are never going to finish.

The failing test (`test_fetch_all_does_not_deadlock_when_some_urls_fail_under_low_concurrency`)
sets `concurrency=2` and makes exactly the first two URLs (`u1`, `u2`) fail — consuming both of
the semaphore's starting permits and never returning them — so `u3` and `u4` are left waiting on
a semaphore that will never again go above zero. `asyncio.wait_for(..., timeout=0.5)` is there so
the test fails cleanly with `TimeoutError` instead of hanging the test suite outright. This is
**not** a timing-dependent flaky test: `asyncio` runs one coroutine at a time on a single thread,
so which two URLs fail and in what order is entirely determined by the fixture's own fake
`fetcher` function, not by OS thread scheduling — the deadlock reproduces identically on every run.

### The fix
Wrap the fetch call in `try`/`finally` so the permit is returned on every path, success or
failure:
```python
async def fetch_one(sem, url, fetcher):
    await sem.acquire()
    try:
        result = await fetcher(url)
    finally:
        sem.release()
    return FetchResult(url, result)
```
`fetcher(url)`'s exception, if any, still propagates out of `fetch_one` after the `finally` block
runs `sem.release()` — `finally` doesn't swallow it, it just guarantees `release()` happens first.
`asyncio.gather(..., return_exceptions=True)` then catches that propagated exception the same way
it always did, but now the semaphore's permit count is correct: a failed URL frees up its slot for
the next URL waiting on it, exactly like a successful one does.

## Bug 2 — `crawler.py`: `aggregate` counts every result as a success, including exceptions

The buggy implementation:
```python
def aggregate(results):
    stats = Stats(total=len(results))
    for item in results:
        stats.succeeded += 1                 # runs for every item, exception or not
        if isinstance(item, Exception):
            stats.errors.append(item)        # correctly recorded...
        else:
            stats.bodies[item.url] = item.body
        # stats.failed is never incremented anywhere
    return stats
```
`stats.succeeded += 1` sits *before* the `isinstance` check, so it runs unconditionally for every
item in `results` — including the ones that are `Exception` instances. Those exceptions are
correctly appended to `stats.errors`, so the failure is visible there, but `stats.failed` (a
separate counter meant to mirror `len(stats.errors)`) is never touched at all and stays 0 forever.
The net effect: every failed fetch is counted as *both* a success (in `stats.succeeded`) and a
failure (in `stats.errors`) at the same time, and `stats.failed` is dead code that always reads 0.
This is exactly the failure mode this task's prompt names directly: an exception that
`return_exceptions=True` turned into a plain return value gets folded into the "everything
succeeded" bucket by code that isn't actually checking which kind of value it received before
counting it.

### The fix
Move `stats.succeeded += 1` into the `else` branch, and add the missing `stats.failed += 1` to the
`if` branch:
```python
def aggregate(results):
    stats = Stats(total=len(results))
    for item in results:
        if isinstance(item, Exception):
            stats.failed += 1
            stats.errors.append(item)
        else:
            stats.succeeded += 1
            stats.bodies[item.url] = item.body
    return stats
```
Now every item lands in exactly one of `succeeded`/`failed`, matching the invariant
`stats.succeeded + stats.failed == stats.total` that a candidate should be able to state out loud
even without it being spelled out anywhere in the code.

## What a graded run should look like
- Candidate runs `pytest tests -q`, sees 2 failures.
- For bug 1: reads the test's docstring (which explains the timeout is there to fail cleanly
  rather than hang, and why the reproduction is deterministic); reproduces the hang locally with a
  debugger or a manual `print` of the semaphore's internal counter; reads `fetch_one`, notices
  `sem.release()` is not protected by `try`/`finally`; wraps it.
- For bug 2: calls `aggregate()` directly with a two-item list (one `FetchResult`, one exception)
  to isolate the bug from any `asyncio` machinery; sees `succeeded == 2` when it should be 1;
  reads `aggregate`, notices `stats.succeeded += 1` sits outside the `if`/`else` rather than in the
  `else` branch, and that `stats.failed` is never assigned to anywhere in the function.
- Total diff: `fetch_one` gains a `try`/`finally` (4 changed lines); `aggregate`'s loop body is
  rearranged (4 changed lines). Candidates who rewrite `fetch_with_retry`'s backoff logic, or
  replace `asyncio.gather` with `asyncio.as_completed`, have gone looking for a bug that isn't
  there.
