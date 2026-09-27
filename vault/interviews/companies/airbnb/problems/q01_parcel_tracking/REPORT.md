# REPORT · q01 Parcel Tracking System

## Summary

A CodeSignal ICF 4-level project. Level 1 is verbatim from photos of a live assessment; Levels 2–4 are reconstructed
from the isomorphic In-Memory Database problem, which FastPrep attributes to Airbnb. It tests extensible state
modelling, not algorithms.

## Sources & confidence

| Part | Confidence | Source |
|---|---|---|
| Format (4 levels, 25 tests, 90 min, 3 s, Python unittest) | high | photos → `../../catalog/raw/codesignal_parcel_tracking_photos.md` |
| Level 1 spec + example | high | photos, verbatim |
| Level 2–4 one-line summaries | high | photos, verbatim |
| Level 2–4 names, signatures, formats, TTL-on-restore rule | medium, **(reconstructed)** | `../../catalog/raw/in_memory_db_isomorph.md` |
| Company = Airbnb | medium | Chi + FastPrep isomorph label; the photos name no company |

The real hidden tests call the real Level 2–4 method names, which we have not seen. What transfers is the data model
and the semantics, not the names.

## Approach by level

1. `dict[parcel_id, dict[tag, _Tag]]`, where `_Tag` carries `expires_at`. Private primitives take `timestamp=None`.
2. One `_list(parcel_id, prefix, timestamp)`: filter alive, `startswith`, `sorted`, format `tag(value)`.
3. `expires_at = timestamp + ttl`; lazy expiry via `alive(ts)`: `ts < expires_at`.
4. Checkpoint = fresh tuples of alive tags with `remaining = expires_at - ts`; restore = `bisect_right - 1`,
   then rebuild `_Tag`s with `restore_ts + remaining`.

## Pitfalls the tests target (all verified by mutation, see below)

Inclusive expiry boundary · truthiness check on `""` · shallow-copy checkpoint · restore aliasing the snapshot ·
TTL not re-anchored at the restore time · `True` on removing an expired tag · insertion order instead of sorted ·
substring instead of prefix · restoring the earliest checkpoint instead of the latest ≤ t · counting parcels whose tags
are all expired.

## Complexity + measured

set/get/remove O(1); list O(k log k); checkpoint O(N); restore O(N + log C).
`test_level_3_case_08` (50k TTL sets + 5k gets + 500 prefix lists): 0.031 s on Python 3.11 (limit 3 s).

## Test inventory

32 tests, 8 per level (`tests/test_level_{1..4}.py`). The real assessment has 25; ours are not a copy of theirs.

- Reference `solution.py`: 32/32 pass (`python3 -m unittest discover -s tests -p "test_*.py"`, also under pytest).
- Empty `starter.py`: 22/32 fail; every level has failures (L1 5, L2 4, L3 6, L4 7). The 10 that pass do so because
  the interface defaults (`None`, `False`, `[]`) happen to match, plus the perf test.
- Mutation check (10 hand-written bugs, one per pitfall above): 10/10 killed.

## Skills exercised

State modelling for changing requirements · half-open intervals · lazy TTL expiry · snapshot isolation (deep copy both
ways) · relative vs absolute time · `bisect_right - 1` for "latest version ≤ t" · exact return types.
