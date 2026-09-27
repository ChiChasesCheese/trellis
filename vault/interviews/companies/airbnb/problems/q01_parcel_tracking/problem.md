# q01 · Parcel Tracking System (CodeSignal ICF, 4 levels)

- **Format:** CodeSignal Industry Coding Framework (ICF/ICA): one project, 4 levels unlocked in sequence, 90 minutes,
  25 unit tests (10 of them Level 1), Python 3 + `unittest`; the page says 3 s, but every test carries `@timeout(0.4)`.
- **Source:** phone photos of a live assessment → `../../catalog/raw/codesignal_parcel_tracking_photos.md`.
  Levels 1 and 3 are verbatim (high confidence). Levels 2 and 4 are **(reconstructed)** from one-line summaries plus the
  isomorphic "In-Memory Database" problem → `../../catalog/raw/in_memory_db_isomorph.md` (medium confidence).
- **Company:** Airbnb per Chi; the photos name no company. FastPrep lists the isomorph as an Airbnb OA.

## Files

| File | Role |
|---|---|
| `parcel_tracking_system.py` | the locked ABC interface (all levels, default implementations) |
| `starter_template.py` → `starter.py` | your file (CodeSignal's `parcel_tracking_system_impl.py`) |
| `solution.py` | reference solution |
| `solution_level1.py` | Level 1 standard answer on its own (plain dict of dicts) |
| `solution_level2.py` | Level 2 standard answer: `solution_level1.py` + two listing methods |
| `solution_level3.py` | Level 3 standard answer: `solution_level2.py` refactored once for `(value, expires_at)` |
| `tests/test_level_{1..4}.py` | 36 `unittest` cases (L1 10, 01–04 copied from the real file; L2 8; L3 10, 01–02 the statement's examples; L4 8); `IMPL=starter` runs them against your file |
| `run_single_test.sh` | `bash run_single_test.sh case_03` |

## Level 1 — basic tag operations (verbatim)

Each parcel is accessed with a unique identifier `parcel_id` (string). A parcel contains several `tag`–`value` pairs,
both strings.

- `set_tag(parcel_id, tag, value) -> None` — set or overwrite `tag` to `value`.
- `get_tag(parcel_id, tag) -> str | None` — the value, or `None` if the parcel or tag does not exist.
- `remove_tag(parcel_id, tag) -> bool` — `True` if removed, `False` if the tag did not exist.

| Query | Result |
|---|---|
| `set_tag("parcel1", "status", "in-transit")` | sets |
| `get_tag("parcel1", "status")` | `"in-transit"` |
| `set_tag("parcel1", "status", "delivered")` | overwrites |
| `get_tag("parcel1", "status")` | `"delivered"` |
| `remove_tag("parcel1", "status")` | `True` |
| `get_tag("parcel1", "status")` | `None` |
| `remove_tag("parcel1", "status")` | `False` |

## Level 2 — listing tags (names and format confirmed by the real interface docstrings)

- `list_tags(parcel_id) -> list[str]` — every tag as `"<tag>(<value>)"`, sorted lexicographically by tag; `[]` if the
  parcel does not exist or has no tags.
- `list_tags_by_prefix(parcel_id, prefix) -> list[str]` — same, only tags starting with `prefix`.

Example: tags `status=in-transit, eta=mon, carrier=ups, city_to=SF, city_from=NYC` →
`list_tags` = `["carrier(ups)", "city_from(NYC)", "city_to(SF)", "eta(mon)", "status(in-transit)"]`,
`list_tags_by_prefix(.., "city")` = `["city_from(NYC)", "city_to(SF)"]`.

## Level 3 — timestamps and TTL (verbatim)

The `timestamp` argument is non-decreasing across all operations from Level 3 onward; `ttl` is never negative.

- `set_tag_at(parcel_id, tag, value, timestamp) -> None` — set or overwrite; does not expire unless overwritten.
- `get_tag_at(parcel_id, tag, timestamp) -> str | None` — the value as it was at `timestamp`; `None` if it did not
  exist or had expired.
- `remove_tag_at(parcel_id, tag, timestamp) -> bool` — remove only if valid at `timestamp` (a tag expiring at
  `timestamp` is already expired). `False` if the parcel does not exist, the tag was never set, already removed, or
  already expired.
- `set_tag_with_hold(parcel_id, tag, value, timestamp, ttl) -> None` — set or overwrite with a TTL; expires at
  `timestamp + ttl`. **If `ttl` is `0`, the tag does not expire.**
- `list_tags_at(parcel_id, timestamp) -> list[str]` — tags valid at `timestamp`, sorted lexicographically by tag,
  each `"tag(value)"`.
- `list_tags_by_prefix_at(parcel_id, prefix, timestamp) -> list[str]` — same, only tags starting with `prefix`.

| Query | Result |
|---|---|
| `set_tag_with_hold("parcel1", "status", "held", 100, 50)` | expires at 150 |
| `get_tag_at("parcel1", "status", 120)` | `"held"` |
| `get_tag_at("parcel1", "status", 150)` | `None` (exclusive boundary) |
| `get_tag_at("parcel1", "status", 180)` | `None` |

| Query | Result |
|---|---|
| `set_tag_with_hold("parcel1", "status", "held", 20, 60)` | expires at 80 |
| `remove_tag_at("parcel1", "status", 50)` | `True` |
| `set_tag_with_hold("parcel1", "hold_reason", "customs", 20, 60)` | expires at 80 (note: ts goes back from 50 to 20, contradicting the guarantee) |
| `remove_tag_at("parcel1", "hold_reason", 80)` | `False` (already expired) |
| `remove_tag_at("parcel1", "priority", …)` | `False` (never set) |

## Level 4 — checkpoints (reconstructed)

- `checkpoint(timestamp) -> int` — save every parcel's state including each tag's remaining TTL; return the number of
  parcels with at least one tag alive at `timestamp`.
- `restore(timestamp, timestamp_to_restore) -> None` — restore the latest checkpoint taken at or before
  `timestamp_to_restore` (guaranteed to exist). A tag with `r` units left at checkpoint time expires at `timestamp + r`.

| Query | Result |
|---|---|
| `set_tag_with_hold("p1", "a", "x", 1, 10)` | alive on [1, 11) |
| `set_tag_at("p2", "b", "y", 2)` | |
| `checkpoint(3)` | `2` (p1.a has 8 left) |
| `set_tag_at("p1", "c", "z", 4)` | |
| `remove_tag_at("p2", "b", 5)` | `True` |
| `restore(20, 3)` | p1.a now expires at 28; p1.c gone; p2.b back |
| `get_tag_at("p1", "a", 27)` / `(.., 28)` | `"x"` / `None` |

## Edge cases the tests pin

Missing parcel vs missing tag · parcel ids and tags are separate namespaces (real `case_04`) · empty-string value is a value · `bool` returns, not truthy values · uppercase sorts
before lowercase · prefix ≠ substring · expiry end exclusive · `ttl == 0` never expires · equal timestamps allowed · plain set clears an old TTL · overwrite resets TTL ·
expired tag cannot be removed · checkpoint count skips expired and emptied parcels · checkpoint isolated from later
writes · restoring twice gives the same state · tag expired at checkpoint time never returns · restore drops parcels
created after the checkpoint.

## What this tests

Not algorithms — **extensible state modelling under changing requirements**: pick a data model at Level 1 that
Levels 3–4 extend without a rewrite, isolate snapshots from live state, and get half-open intervals right.
