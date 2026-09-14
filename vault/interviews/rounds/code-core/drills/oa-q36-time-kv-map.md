---
nodes: [toolbox.cache, toolbox.sorted, transfer.stripe-oa]
tags: [stripe-oa, q36]
---
# Drill: a time-based key-value store with history and TTL

Sixty minutes, stdin to stdout. Build a versioned key-value store: every `SET
key value time [ttl]` stamps a write with a time, and every `GET key time`
must return the value that was in effect at that time — the version with the
largest write time no later than the query, treating writes as if they can
arrive out of order. Part 1 implements plain set/get. Part 2 adds `GETALL key
time`, the full version history up to a time, ordered by write time. Part 3
adds an optional TTL: a version is live only for a half-open window after its
write, and expiry does not fall back to an older version. Part 4 is an
unrelated warm-up bonus, first-missing-positive over a list of integers.

**Constraints to state and honor**
- Input is a `PART n` header then one command per line; keys/values are plain
  strings, times/ttls non-negative integers.
- Writes may arrive with times out of order; a second write at the same key
  and time overwrites the earlier one.
- `GET` on an unwritten key, or before its first write, is `null`; `GETALL`
  with nothing in range is an empty line, not `null`.
- The TTL window is `[time, time + ttl)` — `time + ttl` itself is already
  expired; `ttl` omitted means never expires.
- Assume large numbers of commands, so an O(n) per-write scan or a per-get
  re-sort doesn't fly — say the target complexity before coding it.

**Grading points**
- `bisect`/`insort` (or an equivalent ordered structure) per key, not a linear
  scan or a re-sort on every query.
- `get` uses `≤`, not `<`, and picks the largest write time — say why out
  loud (interval semantics, not exact match).
- Same-time overwrite and out-of-order insertion are two different code paths
  and both need their own test.
- TTL is modeled as an exclusive end (`time + ttl`), and expiry is evaluated
  only on the version `get` already selected — no silent fallback to an older
  write.
- `GETALL`'s "nothing found" output is a blank line, not the sentinel `GET`
  uses for a miss — the two output shapes must not be conflated.
- Treat Part 4 as an unrelated bonus and don't let it leak into the store's
  design.

**Source**
- `vault/interviews/companies/stripe/problems/q36_time_kv_map/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/q36_time_kv_map.md`, `vault/interviews/companies/stripe/problems/q36_time_kv_map/problem.md`, `vault/interviews/companies/stripe/study/10-solutions/q36_time_kv_map.md`

**Attempt log**
- [ ] Attempt 1 (date, 60 min, self-graded notes):
