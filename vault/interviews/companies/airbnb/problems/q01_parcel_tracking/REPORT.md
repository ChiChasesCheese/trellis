# REPORT · q01 Parcel Tracking System

## Summary

A CodeSignal ICF 4-level project. Level 1 is verbatim from photos of a live assessment; Levels 2–4 are reconstructed
from the isomorphic In-Memory Database problem, which FastPrep attributes to Airbnb. It tests extensible state
modelling, not algorithms.

## Sources & confidence

| Part | Confidence | Source |
|---|---|---|
| Format (4 levels, 25 tests with 10 in Level 1, 90 min, `@timeout(0.4)` per test, Python unittest) | high | photos → `../../catalog/raw/codesignal_parcel_tracking_photos.md` |
| Level 1 spec + example + test cases 01–04 | high | photos, verbatim |
| Level 2–4 one-line summaries | high | photos, verbatim |
| Level 3 full spec + 2 examples | high | photos (third batch), verbatim |
| Level 2 and 4 names, signatures, formats, TTL-on-restore rule | medium, **(reconstructed)** | `../../catalog/raw/in_memory_db_isomorph.md` |
| Company = Airbnb | medium | Chi + FastPrep isomorph label; the photos name no company |

The real hidden tests call the real Level 2 and 4 method names, which we have not seen (our Level 3 guess got the TTL
method name and `ttl == 0` wrong until the spec arrived). What transfers is the data model
and the semantics, not the names.

## Approach by level

1. `dict[parcel_id, dict[tag, value]]` and three methods, nothing else. At Level 3 the value becomes `(value, expires_at)`
   and the Level 1/2 methods delegate to private helpers with `timestamp=None`.
2. One `_list(parcel_id, prefix, timestamp)`: filter alive, `startswith`, `sorted`, format `tag(value)`.
3. `expires_at = timestamp + ttl`, or `None` when `ttl == 0`; lazy expiry via `_alive(expires_at, ts)`: `ts < expires_at`.
4. Checkpoint = fresh tuples of alive tags with `remaining = expires_at - ts`; restore = `bisect_right - 1`,
   then rebuild fresh tuples with `restore_ts + remaining`.

## Pitfalls the tests target (all verified by mutation, see below)

Inclusive expiry boundary · truthiness check on `""` · shallow-copy checkpoint · restore aliasing the snapshot ·
TTL not re-anchored at the restore time · `True` on removing an expired tag · insertion order instead of sorted ·
substring instead of prefix · `ttl == 0` treated as instant expiry · restoring the earliest checkpoint instead of the latest ≤ t · counting parcels whose tags
are all expired.

## Complexity + measured

set/get/remove O(1); list O(k log k); checkpoint O(N); restore O(N + log C).
`test_level_3_case_08` (50k TTL sets + 5k gets + 500 prefix lists): 0.03 s on Python 3.11 (real per-test timeout 0.4 s; the test asserts < 0.4 s).

## Test inventory

36 tests: Level 1 has 10 like the real file (cases 01–04 copied from the photos, 05–10 ours); Level 2 has 8 (ours);
Level 3 has 10 (01–02 are the statement's examples, the rest ours); Level 4 has 8 (ours). The real Levels 2–4 share 15
tests we have not seen.

- Reference `solution.py`: 36/36 pass (`python3 -m unittest discover -s tests -p "test_*.py"`, also under pytest).
- Empty `starter.py`: 29/36 fail; every level has failures (L1 9, L2 4, L3 9, L4 7). The 7 that pass do so because
  the interface defaults (`None`, `False`, `[]`) happen to match, plus the perf test.
- Mutation check (11 hand-written bugs, one per pitfall above plus `ttl == 0` expiring): 11/11 killed.

## Skills exercised

State modelling for changing requirements · half-open intervals · lazy TTL expiry · snapshot isolation (deep copy both
ways) · relative vs absolute time · `bisect_right - 1` for "latest version ≤ t" · exact return types.
