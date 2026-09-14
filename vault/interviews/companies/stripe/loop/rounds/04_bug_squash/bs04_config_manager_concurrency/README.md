# confmgr — a small layered, thread-safe configuration manager

`confmgr` gives an app one `get(key)` call that merges four configuration sources, highest
precedence last: **defaults** (baked into the code) < **file** (a JSON file on disk) <
**environment variables** (a prefix-matched slice of `os.environ`) < **runtime overrides** (set
in-process, e.g. from an admin endpoint). A `reload()` call re-reads the file and environment
layers without restarting the process. Results are served from a small TTL cache so a hot key
isn't re-resolved across all four layers on every single call. The whole thing is meant to be
called from multiple threads at once (a web server's request-handling threads all calling
`config.get(...)`, plus a background thread calling `reload()` on a timer).

## Layout
```
src/confmgr/
  layers.py     load_file_layer(path), load_env_layer(prefix) -- stateless loaders, no caching
  cache.py      TTLCache: get/set/invalidate/clear, plus get_or_compute(key, factory)
  manager.py    ConfigManager: combines the four layers + a TTLCache into one get()/reload() API
tests/
  test_layers.py    load_file_layer / load_env_layer in isolation
  test_cache.py     TTLCache in isolation, including one concurrency test
  test_manager.py   ConfigManager: precedence, overrides, reload()
```

## Running the tests
```
python -m pytest tests -q
```
Most tests pass as shipped. Two do not — see the issue below.

## The issue (as filed against this repo)

**Bug report 1 — under concurrent load, the same cache key gets resolved more than once**

> We cache every `ConfigManager.get(key)` result behind a TTL so we're not walking all four
> config layers on every call. Our load-testing setup calls `get()` for the same key from many
> threads at once right after startup (before anything is cached yet), and we're seeing the
> layer-resolution logic run more times than there are distinct keys — sometimes 2x, sometimes
> more depending on how many threads pile up on the same cold key at once.
>
> This matters because our layer-resolution logic isn't just a dict lookup for us in production —
> it also does some bookkeeping (a metrics counter, in our real deployment) that's supposed to
> happen exactly once per cache miss, not once per thread that happened to see a miss.
>
> Repro: have two threads call `cache.get_or_compute("k", factory)` for the same, not-yet-cached
> key at close to the same time, where `factory` takes long enough to run that both threads are
> virtually guaranteed to still see a miss when they check. Expected: `factory` runs once.
> Actual: it runs once per thread that got there before anyone had stored a result yet.

**Bug report 2 — after `reload()`, `get()` keeps returning the old value until the TTL expires**

> We call `ConfigManager.reload()` after deploying a new config file, expecting the very next
> `get()` for any key that file touches to reflect the new value immediately. Instead we keep
> getting the pre-reload value back until the cache entry's TTL naturally expires on its own —
> which, for a key that was already warm, defeats the entire point of calling `reload()` instead
> of just waiting.
>
> Repro: `get()` a key (populating the cache), change the underlying file, call `reload()`, `get()`
> the same key again with a TTL long enough that it hasn't expired on its own. Expected: the new
> value. Actual: the value from before `reload()` was called.

If you get stuck: both bugs are narrowly scoped to one method each (`cache.py`'s
`get_or_compute`; `manager.py`'s `reload`) — if your fix touches more than a handful of lines, or
you find yourself redesigning the locking strategy or the layer-precedence logic, you've drifted
from the actual bug into a redesign. Come back to the failing assertion and follow it.
