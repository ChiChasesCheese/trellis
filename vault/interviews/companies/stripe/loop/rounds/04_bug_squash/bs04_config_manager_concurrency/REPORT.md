# bs04 confmgr (layered config manager, concurrency) — report

## Summary
A ~150-line layered configuration manager (`layers.py` → `cache.py`'s `TTLCache` → `manager.py`'s
`ConfigManager`, merging defaults/file/env/runtime-override layers behind a TTL cache) with two
independent bugs injected, both drawn from the "跨调用残留状态" (state that should reset across
calls but doesn't) and general concurrency-bug families named in `loop/LOOP_GUIDE.md` §4 and
`catalog/discovery/2026-09/rounds_material.md` §1.2 (leonstaff.com, 2026-08-13): a cache-stampede
race (check-then-act split across two separately-locked operations) and a stale-cache-after-
reload bug (an instance field that should be reset on a lifecycle event but isn't). Unlike bs01,
this fixture is not a direct port of one specific real GitHub issue — bs01–bs03 already cover
that ground for this round set (`requests`/`Mako`, per `rounds_material.md` §1.1) — bs04/bs05 were
commissioned specifically to cover the **concurrency** shape of bug squash that those three don't
touch (`threading`/`asyncio`), using bug *patterns* (cache stampede, semaphore-permit leak on an
exception path) that are extremely common in real Python codebases rather than one pinned issue
number.

## Sources & confidence
High for "跨调用残留状态" and the four-category bug taxonomy this round's two bugs are drawn from:
`loop/LOOP_GUIDE.md` §4 ("四类典型 bug...**跨调用残留的状态**（该重置没重置）"), sourced from
`catalog/discovery/2026-09/rounds_material.md` §1.2 (leonstaff.com, published 2026-08-13, "a state
variable that persists across calls when it should reset"). High for "these two rounds exist to
cover concurrency, which bs01–bs03 don't": `loop/tasks/todo.md` T17 and this task's own framing
("并发主题，这是 bs01–bs03 没覆盖的"). Medium-low for "cache stampede" and "semaphore not released
on an exception path" as *specific* real-world bug patterns — no single pinned GitHub issue is
cited for either (unlike bs01's Mako path-traversal bug, which maps to `sqlalchemy/mako` issue
#434 exactly); these are instead extremely well-documented, recurring bug *shapes* in the general
Python ecosystem (check-then-act races around memoization without a lock spanning the whole miss
path; semaphore/connection-pool permit leaks on exception paths are a standing category of
aiohttp/asyncpg-adjacent bug reports), reconstructed here as a self-contained fixture rather than
diffed from one upstream commit.

## Bugs injected
1. **`cache.py`: `TTLCache.get_or_compute()` composes `self.get()` and `self.set()` as two
   separately-locked calls, with the (potentially slow) `factory()` call unlocked in between.**
   Two threads racing a cold key can both observe a miss and both invoke `factory()` — a cache
   stampede. The failing test forces this deterministically (not flaky) via a `factory` that
   sleeps 0.2s (dwarfing any scheduling jitter) plus a `threading.Barrier(2)` to start both
   threads together, and asserts `factory` ran exactly once.
2. **`manager.py`: `ConfigManager.reload()` refreshes `_file_layer`/`_env_layer` but never calls
   `self._cache.clear()`.** A key that was already cached before `reload()` keeps returning its
   stale value until its own TTL expires on its own, defeating the purpose of calling `reload()`
   at all. The failing test uses a 100-second TTL specifically to rule out "it just hadn't expired
   yet" as an innocent explanation.

## Debugging path (from a failing assertion to the fix)
- Run `pytest tests -q`: 2 of 25 fail.
- `test_get_or_compute_calls_factory_at_most_once_under_concurrent_misses` fails with
  `AssertionError: factory should run exactly once per miss, ran 2 time(s)`. Reading the test's
  own docstring explains *why* the 0.2s sleep and the barrier are there (forcing, not hoping for,
  the interleaving). Reading `get_or_compute` shows it's built from `self.get(key)` (which takes
  and releases `self._lock` on its own) followed by unlocked work followed by `self.set(key, ...)`
  (which takes and releases `self._lock` again) — two independently-safe operations composed into
  one *unsafe* one.
- `test_reload_picks_up_new_file_contents_immediately` fails with `assert 'hi' == 'bonjour'` —
  calling `ConfigManager.get()` after `reload()` still returns the pre-reload value. This test is
  independent of bug 1 — it never spins up a second thread, and the separate
  `test_reload_replaces_env_layer_contents` test (which reads `mgr._env_layer` directly, bypassing
  `get()`/the cache) confirms `reload()` itself correctly refreshes the layer data, narrowing the
  bug to what happens *between* the layer refresh and the next `get()` — i.e. the cache.

## Minimal fix
`solution/FIX.patch` — 2 files, +10/-6 lines (16 changed lines total; `cache.py`'s
`get_or_compute` rewritten to hold one lock across check+compute+store; one new line,
`self._cache.clear()`, in `manager.py`'s `reload()`). Verified: `git apply --check` clean against
a fresh copy; after applying, 25/25 pass.

## 面试官评分看什么
- Recognizes the concurrency test's `sleep`+`Barrier` combination as a deliberate determinism
  device, not incidental slowness — and doesn't try to "fix" the test by removing them.
- For bug 1: articulates *why* two separately-locked operations aren't equivalent to one locked
  operation (the gap between them is where the race lives), not just "add more locking somewhere
  until the test passes."
- For bug 2: notices the passing `test_reload_replaces_env_layer_contents` test already rules out
  "the layer itself wasn't refreshed" — narrowing where to look before touching code.
- Fix size stays proportional: bug 1 touches one method; bug 2 adds one line. A candidate who adds
  a lock spanning all of `ConfigManager`, or who makes `reload()` return a new `ConfigManager`
  instance instead of mutating in place, has drifted into a redesign.

## 常见跑偏
- Making `TTLCache.get_or_compute` synchronous by having `ConfigManager.get()` acquire a
  *second*, coarser lock around the whole call instead of fixing `get_or_compute` itself — papers
  over the actual bug (which is inside `TTLCache`, a class meant to be safe to use on its own) and
  leaves a caller-must-remember-to-lock footgun for the next place `TTLCache` gets used.
- "Fixing" bug 2 by shortening the default `cache_ttl` instead of calling `self._cache.clear()`
  in `reload()` — makes the specific failing test's exact numbers pass by coincidence without
  fixing the actual defect (stale-until-natural-expiry is still true for any TTL longer than the
  time between reload and the next read).
- Rewriting `_resolve`'s four-layer precedence chain, or the `_overrides_lock`/`_cache` split into
  a single lock for the whole `ConfigManager` — neither bug lives there.

## Test inventory
25 tests, plain pytest, split across `test_layers.py` (5, all pass — pure functions, nothing to
race), `test_cache.py` (9: 8 pass, 1 fails — bug 1), `test_manager.py` (11: 10 pass, 1 fails —
bug 2). After `git apply solution/FIX.patch`: 25/25 pass. Re-running the unpatched suite 20 times
in a row produces "2 failed, 23 passed" every single time (verified as part of this task) — the
concurrency test is deterministic, not flaky, by construction (the 0.2s `factory` delay plus
`threading.Barrier(2)` dominate any OS scheduling variance by several orders of magnitude).

## Skills exercised
S16 lock scope / critical-section boundaries · S17 cache-stampede / dog-piling recognition ·
S19 instance-lifecycle state that must be reset on a specific event (`reload()`) · S20
root-causing from a failing assertion (including reading a test's own docstring for *why* it's
built the way it is) rather than guess-and-check editing
