# bs04 confmgr — solution notes (not shown to the candidate; read after `ref`)

## Bug 1 — `TTLCache.get_or_compute`: check-then-act split across two lock scopes

The buggy implementation:
```python
def get_or_compute(self, key, factory):
    cached = self.get(key)      # takes self._lock, reads, releases self._lock
    if cached is not None:
        return cached
    value = factory()           # NOT holding self._lock -- this can take arbitrarily long
    self.set(key, value)        # takes self._lock again, writes, releases
    return value
```
`self.get(key)` and `self.set(key, value)` are each individually thread-safe (each takes
`self._lock` for its own duration) — but the *combination* is not, because the lock is released
between them. Two threads that both call `get_or_compute("k", factory)` on a cold key at close to
the same time can both execute `self.get("k")`, both see `None`, and both go on to call
`factory()` and `self.set("k", ...)` — the cache did not, in fact, prevent the second thread's
redundant work, which is the entire reason a cache like this exists. This is the classic "cache
stampede" bug (also called "dog-piling"): the point of a `get_or_compute`-style API is that a
miss triggers *one* recomputation shared by every waiter, not one recomputation per waiter that
happened to arrive before anyone had written a result yet.

The failing test (`test_get_or_compute_calls_factory_at_most_once_under_concurrent_misses`)
forces this deterministically rather than leaving it to chance: `factory` sleeps for 0.2s before
returning, which is enormously longer than the few microseconds it takes to execute
`self.get(key)` — so on unpatched code, **every** run has both threads observe the miss before
either one calls `set()`. A `threading.Barrier(2)` starts both threads at (as close to) the same
instant so the race window isn't left to whatever the OS scheduler happens to do first. This is
why the test is 100% reproducible rather than flaky: the 0.2s gap dominates any scheduling jitter,
in either direction, by several orders of magnitude.

### The fix
Hold `self._lock` across the *entire* operation — the check, the (potentially slow) call to
`factory`, and the write — instead of composing two separately-locked helper calls:
```python
def get_or_compute(self, key, factory):
    with self._lock:
        entry = self._store.get(key)
        if entry is not None:
            value, expires_at = entry
            if expires_at > time.monotonic():
                return value
        value = factory()
        self._store[key] = (value, time.monotonic() + self._ttl)
        return value
```
With this fix, when two threads race for the same cold key: whichever thread's `with self._lock:`
wins acquires it, checks (miss), computes, stores, and releases — the *entire* sequence, including
the slow `factory()` call, happens while holding the lock. The second thread blocks on
`with self._lock:` for the whole time (it never even reaches its own `self._store.get(key)` call)
and only proceeds once the lock is free — at which point it finds a fresh, non-expired entry and
returns it directly, never calling `factory` at all. `factory` runs exactly once per genuine miss.

This does mean the cache's lock is held for the duration of a slow `factory` call, which is a
real, known trade-off of this "hold the lock across the whole miss path" fix (it serializes misses
for *different* keys too, not just the same key) — worth mentioning if a candidate raises it, but
not required to pass the tests here. A production system with many independent hot keys and an
expensive `factory` might instead use a per-key `asyncio.Future`/threading `Event` so concurrent
misses on *different* keys don't block each other; that's a larger, riskier change than this
fixture's 45-minute scope calls for.

## Bug 2 — `ConfigManager.reload()` never clears the cache

The buggy `reload()`:
```python
def reload(self):
    if self._file_path:
        self._file_layer = load_file_layer(self._file_path)
    if self._env_prefix:
        self._env_layer = load_env_layer(self._env_prefix)
```
This correctly replaces `self._file_layer` and `self._env_layer` with freshly-read data — but
`self._cache` (a `TTLCache` instance, a field on `ConfigManager` set up in `__init__` and never
touched again outside of `get`/`set_override`/`clear_override`) is left completely untouched.
Any key that was already cached (i.e. anyone had already called `get()` for it before `reload()`
was called) keeps returning its pre-reload value until that specific cache entry's own TTL
naturally expires — `reload()` has no effect on it at all. This is a textbook "instance field that
should be reset on some lifecycle event but isn't" bug: `_file_layer` and `_env_layer` are the two
fields `reload()` remembers to refresh, but `_cache` — a field whose correctness depends on the
other two — is not treated as part of what "reloading" means.

The failing test (`test_reload_picks_up_new_file_contents_immediately`) uses a long TTL (100s) so
there's no ambiguity about whether the value would have expired on its own anyway — with the real
fix, the *only* way the new value can show up before 100 seconds pass is if `reload()` itself
invalidated the stale entry.

### The fix
One line, at the end of `reload()`:
```python
def reload(self):
    if self._file_path:
        self._file_layer = load_file_layer(self._file_path)
    if self._env_prefix:
        self._env_layer = load_env_layer(self._env_prefix)
    self._cache.clear()
```
`clear()` drops every cached entry (not just ones for keys defined in the file/env layers) —
simpler and safer than trying to invalidate only "affected" keys, since a key that used to fall
through to `defaults` might now be defined in the freshly-reloaded file layer (or vice versa) and
`reload()` has no cheap way to know in advance which keys changed meaning without just re-running
`_resolve` for every key that's ever been queried.

## What a graded run should look like
- Candidate runs `pytest tests -q`, sees 2 failures.
- For bug 1: reads the concurrency test, understands the barrier + sleep are there to force
  determinism (not just make the test slow for no reason); reads `get_or_compute`, notices it's
  built out of two separately-locked calls (`self.get` then `self.set`) with unprotected work in
  between; fixes it by inlining the check+compute+write into one `with self._lock:` block.
- For bug 2: reads the reload test, notices the TTL is set deliberately high (ruling out "it just
  hadn't expired yet" as an explanation); reads `reload()` top to bottom, notices it touches
  `_file_layer`/`_env_layer` but never `_cache`; adds `self._cache.clear()`.
- Total diff: ~10 changed lines in `cache.py`'s one method + 1 new line in `manager.py`.
  Candidates who introduce a global lock across `ConfigManager` itself, or restructure
  `_resolve`'s precedence logic, have gone looking for a bug that isn't there.
