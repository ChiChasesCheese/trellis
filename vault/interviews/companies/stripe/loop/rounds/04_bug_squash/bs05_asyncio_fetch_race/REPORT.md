# bs05 fetchrace (asyncio concurrent fetcher) — report

## Summary
A ~120-line bounded-concurrency async fetcher (`http_client.py` → `retry.py` → `crawler.py`'s
`fetch_one`/`aggregate`/`fetch_all`, paired with a local `http.server`-based test fixture standing
in for the thing being fetched) with two independent bugs injected: a `Semaphore` permit leak on
an exception path (causing a deterministic deadlock once enough URLs fail under low concurrency),
and `asyncio.gather(..., return_exceptions=True)`'s swallowed exceptions being miscounted as
successes in the final aggregation. Both are named directly in this task's own bug-candidate list
("Semaphore 在异常路径上没释放"; "异常被 gather(..., return_exceptions=True) 吞掉后当成正常结果
计入统计") and correspond to real, recurring bug shapes in async Python codebases rather than one
pinned upstream issue — like bs04, this fixture exists specifically to cover the **concurrency**
half of bug squash that bs01–bs03's non-concurrent library ports (`requests`/`Mako`) don't touch.

## Sources & confidence
High for "these are the two bug shapes this task specified for bs05's main/secondary slots" — the
task's own instructions name "Semaphore 在异常路径上没释放" as one of three acceptable main-bug
candidates and "异常被 return_exceptions=True 吞掉后当成正常结果计入统计" as the (singular) named
secondary-bug candidate; both are used essentially verbatim. High for "concurrency bugs should be
100% deterministic, not flaky, using a barrier or an injected sleep point" —
`loop/tasks/todo.md` T17 and this task's own instructions. Medium for "these specific bugs
correspond to real-world patterns": semaphore/permit leaks on exception paths and
exceptions-miscounted-as-successes under `gather(return_exceptions=True)` are well-known,
frequently-reported bug classes in async Python code (connection-pool checkout/checkin bugs, retry
frameworks that don't distinguish `Exception` results from real ones) but this fixture does not
cite one specific pinned GitHub issue for either, unlike bs01's exact `sqlalchemy/mako` #434
correspondence — these were synthesized to match the named patterns rather than diffed from an
upstream commit.

## Bugs injected
1. **`crawler.py`: `fetch_one()` calls `sem.release()` as a plain statement after `await
   fetcher(url)`, not inside a `try`/`finally`.** If `fetcher(url)` raises (as it will for any URL
   whose retries are exhausted), the semaphore permit taken by `sem.acquire()` is never returned.
   Once enough URLs fail to exhaust the semaphore's starting permit count, every remaining URL
   blocks forever on `await sem.acquire()`, and `asyncio.gather()` never completes. The failing
   test wraps the call in `asyncio.wait_for(..., timeout=0.5)` so it fails cleanly with
   `TimeoutError` rather than hanging outright; because `asyncio` is single-threaded and
   cooperative, which URLs fail is fully determined by the test's own fake `fetcher`, so this
   reproduces identically on every run (no `Barrier`/sleep-based interleaving is needed the way
   bs04's `threading` bug requires — `asyncio`'s single-threaded scheduling is deterministic given
   the same sequence of `await` points).
2. **`crawler.py`: `aggregate()` increments `stats.succeeded` unconditionally for every item in
   the results list, before checking `isinstance(item, Exception)`.** An exception item is
   correctly appended to `stats.errors`, but it is *also* counted toward `stats.succeeded`, and
   `stats.failed` is never incremented anywhere in the function (dead field, always 0). The
   failing test calls `aggregate()` directly with a hand-built two-item list, bypassing all
   `asyncio` machinery, isolating this bug from bug 1 entirely.

## Debugging path (from a failing assertion to the fix)
- Run `pytest tests -q`: 2 of 12 fail.
- `test_fetch_all_does_not_deadlock_when_some_urls_fail_under_low_concurrency` fails with
  `TimeoutError` raised from inside `asyncio.wait_for`, itself raised from `sem.acquire()` inside
  `fetch_one` (visible in the traceback as a `CancelledError` chained from `wait_for`'s own
  cancellation of the hung task). Reading the test's docstring explains the deadlock mechanism
  before reading any source; reading `fetch_one` shows `sem.release()` sitting after the call that
  can raise, not protected by `finally`.
- `test_aggregate_separates_exceptions_from_successes` fails with `assert 3 == 2` (i.e.
  `stats.succeeded` came back one higher than expected). Reading `aggregate`'s loop body shows
  `stats.succeeded += 1` runs before the `isinstance` branch, unconditionally, and `stats.failed`
  is declared on the `Stats` dataclass but never assigned to anywhere in the function.

## Minimal fix
`solution/FIX.patch` — 1 file, +6/-4 lines (10 changed lines total, both in `crawler.py`: a
`try`/`finally` added around `fetch_one`'s fetch call; `aggregate`'s loop body rearranged so
`succeeded`/`failed` are each incremented in exactly one branch). Verified: `git apply --check`
clean against a fresh copy; after applying, 12/12 pass.

## 面试官评分看什么
- Recognizes the `asyncio.wait_for(..., timeout=...)` in the deadlock test as a deliberate "fail
  fast instead of hanging" device, and understands *why* the deadlock is deterministic rather than
  attributing it to "flaky async test."
- For bug 1: can explain the semaphore-permit-accounting invariant ("every `acquire()` needs
  exactly one matching `release()`, on every code path") rather than just wrapping code in
  `try`/`finally` because the test told them to.
- For bug 2: notices `aggregate()` can and should be tested with a hand-built list with no
  `asyncio` involved at all — isolating a pure-function bug from the concurrency bug next to it.
- Fix size stays proportional: bug 1 is a `try`/`finally`; bug 2 is a 4-line rearrangement within
  one existing loop. A candidate who replaces the semaphore with a different concurrency-limiting
  mechanism, or restructures `fetch_all`'s use of `gather`, has gone looking for a bug that isn't
  there.

## 常见跑偏
- "Fixing" bug 1 by increasing `concurrency` in the failing test instead of fixing `fetch_one` —
  makes this specific test's specific numbers stop deadlocking without touching the actual
  resource leak, which would still deadlock at a larger scale (more failures, or a smaller
  concurrency limit).
- "Fixing" bug 2 by making `aggregate` special-case the exact exception message the test uses,
  instead of checking `isinstance(item, Exception)` generically — passes the one test, breaks for
  any other exception type.
- Switching `asyncio.gather(..., return_exceptions=True)` to `return_exceptions=False` (letting
  the first failure cancel everything) to "solve" bug 1 — changes `fetch_all`'s documented
  contract (a failing URL should not stop the others) rather than fixing the actual leak.

## Test inventory
12 tests, plain pytest (no `pytest-asyncio` dependency — every async test wraps its coroutine in a
plain `asyncio.run(...)` call inside an ordinary `def test_...():` function, keeping the fixture
pure-stdlib), split across `test_http_client.py` (3, all pass — exercises the local test server
directly), `test_retry.py` (3, all pass), and `test_crawler.py` (6: 4 pass, 2 fail — one per bug).
After `git apply solution/FIX.patch`: 12/12 pass. Re-running the unpatched suite 20 times in a row
produces "2 failed, 10 passed" every single time (verified as part of this task) — both failures
are fully deterministic: bug 1's deadlock follows directly from which fake-fetcher URLs are wired
to fail (not from OS thread scheduling, since `asyncio` runs one coroutine at a time), and bug 2's
assertion failure follows directly from a hand-built input list with no concurrency involved.

## Skills exercised
S16 lock/semaphore accounting invariants (acquire count == release count on every path) ·
S17 `asyncio.gather(return_exceptions=True)` result-shape handling · S20 root-causing from a
failing assertion / a deliberately-timeout-wrapped hang, and isolating a pure-function bug
(aggregate) from a concurrency bug (fetch_one) that live in the same file
