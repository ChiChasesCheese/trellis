# Raw: CodeSignal "Parcel Tracking System" — phone photos of a live assessment

- **Source:** 5 phone photos of a CodeSignal assessment screen, found online and supplied by Chi on 2026-09-27.
  The photos are not committed: the repo is public, and they show a live test URL, the taker's browser bookmarks and the
  "codesignal.com is sharing your screen" banner.
- **Company:** the photos do not name a company. The Airbnb attribution comes from Chi. Corroboration: FastPrep lists
  an isomorphic problem as "In-Memory Database (Airbnb Online Assessment)" — see `in_memory_db_isomorph.md`.
- **Confidence:** Level 1 **high** (read verbatim off the screen). Levels 2–4 **one-line summaries only**.

## Environment visible in the photos

- Page title: `Filesystem with Unit Tests` (the CodeSignal project template, not the problem). "Question 1 of 1".
- Counter `0/25` (25 unit tests in total across levels), timer `1h 29m left`, `[execution time limit] 3 seconds`,
  memory limit `6g` (partly cropped).
- Language picker: `Python 3 / unittest`.
- Files: `tests/level_1_tests.py` (locked), `tests/sandbox_tests.py`, `main.sh` (locked),
  `parcel_tracking_system.py` (locked, the ABC interface), `parcel_tracking_system_impl.py` (editable),
  `run_single_test.sh` (locked).
- `run_single_test.sh`:
  ```sh
  #!/bin/sh
  python3 -m unittest discover -s tests -p "*.py" -k "$1" 2>&1
  ```
- `parcel_tracking_system_impl.py` as shipped:
  ```python
  from parcel_tracking_system import ParcelTrackingSystem

  class ParcelTrackingSystemImpl(ParcelTrackingSystem):
      def __init__(self):
          # TODO: implement
          pass
      # TODO: implement interface methods here
  ```
- `parcel_tracking_system.py` (Level 1 part visible): `class ParcelTrackingSystem(ABC)` with docstring
  "`ParcelTrackingSystem` interface.", and for each method a docstring + `# default implementation`:
  `set_tag` → `pass`, `get_tag` → `return None`, `remove_tag` → `return False`.

## Verbatim text

> **Instructions.** Your task is to implement a simplified version of a parcel tracking system. All operations that
> should be supported by this system are described below.
>
> Solving this task consists of several levels. Subsequent levels are opened when the current level is correctly
> solved. You always have access to the data for the current and all previous levels.
>
> You are not required to provide the most efficient implementation. Any code that passes the unit tests is sufficient.
>
> You can execute a single test case by running the following command in the terminal:
> `bash run_single_test.sh "<test_case_name>"`.
>
> **Requirements.** Your task is to implement a simplified version of a parcel tracking system. Plan your design
> according to the level specifications below:
>
> - Level 1: The parcel tracking system should support basic tag operations: setting, getting, and removing string
>   tags on parcels.
> - Level 2: The parcel tracking system should support listing tags on parcels.
> - Level 3: The parcel tracking system should support timestamped tag operations with optional time-to-live (TTL) expiry.
> - Level 4: The parcel tracking system should support checkpoints for saving and restoring the state of parcels.
>
> To move to the next level, you need to pass all the tests at this level when submitting the solution.
>
> **Level 1.** The basic level of the parcel tracking system contains parcels. Each parcel is accessed with a unique
> identifier `parcel_id` of *string* type. A parcel contains several `tag` - `value` pairs, where both `tag` and
> `value` are *strings*.
>
> - `set_tag(self, parcel_id: str, tag: str, value: str) -> None` — should set or overwrite the `tag` to `value` for
>   the parcel identified by `parcel_id`.
> - `get_tag(self, parcel_id: str, tag: str) -> str | None` — should return the value of `tag` for the parcel
>   identified by `parcel_id`. If the parcel or tag does not exist, should return `None`.
> - `remove_tag(self, parcel_id: str, tag: str) -> bool` — should remove the `tag` from parcel `parcel_id`. Returns
>   `True` if the tag was removed or `False` if the tag did not exist.
>
> **Examples**
>
> | Queries | Explanations |
> |---|---|
> | `set_tag("parcel1", "status", "in-transit")` | sets tag "status" to "in-transit" |
> | `get_tag("parcel1", "status")` | returns "in-transit" |
> | `set_tag("parcel1", "status", "delivered")` | overwrites "status" to "delivered" |
> | `get_tag("parcel1", "status")` | returns "delivered" |
> | `remove_tag("parcel1", "status")` | returns True; tag removed |
> | `get_tag("parcel1", "status")` | returns None; tag no longer exists |
> | `remove_tag("parcel1", "status")` | returns False; tag already removed |

Not visible: Level 2–4 method names, signatures, return formats and examples.

## Second batch (5 more photos, supplied 2026-09-27)

- `main.sh`: `echo "> python3 -m unittest discover -s /usercode/FILESYSTEM/tests -p '*.py' 2>&1"` then runs that command.
- Every test is decorated `@timeout(0.4)` (`from timeout_decorator import timeout`): **0.4 s per test**, far stricter
  than the page's "3 seconds" execution limit.
- Test classes use `@classmethod def setUp(cls): cls.tracker = ParcelTrackingSystemImpl()`: a fresh instance per test.
- `tests/sandbox_tests.py` (editable, unscored): "The test class below can be considered as a playground - feel free to
  modify it as you need, e.g.: add your own custom tests, delete existing tests, modify test contents or expected
  output. The results of tests from this file will always be at the beginning of the report generated by clicking the
  'Run' button. The results of these tests do not affect the final score (unless the project fails to build). Do not
  reuse the name of an existing unit test. If a sandbox test has the same name as a scored test, that scored test will
  not be counted and a full score is impossible." Its `test_sample`:
  ```python
  self.tracker.set_tag('PKG-001', 'status', 'in_transit')
  self.tracker.set_tag('PKG-001', 'hub', 'east')
  self.assertEqual(self.tracker.get_tag('PKG-001', 'status'), 'in_transit')
  self.assertIsNone(self.tracker.get_tag('PKG-001', 'route'))
  self.assertTrue(self.tracker.remove_tag('PKG-001', 'status'))
  self.assertFalse(self.tracker.remove_tag('PKG-001', 'route'))
  ```
- `tests/level_1_tests.py` (locked): "The test class below includes **10 tests for Level 1**. All have the same score.
  You are not allowed to modify this file, but feel free to read the source code to better understand what is
  happening in every specific case." So Levels 2–4 share the other 15 of the 25 tests. Legible cases:
  ```python
  def test_level_1_case_01_simple_set_and_get_1(self):
      self.tracker.set_tag('parcel1', 'destination_city', 'Annapolis')
      self.tracker.set_tag('parcel2', 'tracking_number', '0123')
      self.assertEqual(self.tracker.get_tag('parcel1', 'destination_city'), 'Annapolis')

  def test_level_1_case_02_simple_set_and_get_2(self):
      self.assertIsNone(self.tracker.get_tag('parcel4', 'service'))
      self.tracker.set_tag('parcel4', 'service', 'express')
      self.assertEqual(self.tracker.get_tag('parcel4', 'service'), 'express')
      self.assertEqual(self.tracker.get_tag('parcel4', 'service'), 'express')

  def test_level_1_case_03_simple_set_get_and_delete(self):
      self.tracker.set_tag('parcel5', 'status', 'in-transit')
      self.assertEqual(self.tracker.get_tag('parcel5', 'status'), 'in-transit')
      self.assertTrue(self.tracker.remove_tag('parcel5', 'status'))
      self.assertIsNone(self.tracker.get_tag('parcel5', 'status'))

  def test_level_1_case_04_multiple_parcels_with_same_tag(self):
      self.tracker.set_tag('parcel6', 'recipient_name', 'HubA')
      self.tracker.set_tag('parcel6', 'sender_name', 'HubB')
      self.tracker.set_tag('sender_name', 'parcel6', 'error')   # arguments swapped on purpose
      self.assertEqual(self.tracker.get_tag('parcel6', 'sender_name'), 'HubB')
      self.assertEqual(self.tracker.get_tag('parcel6', 'recipient_name'), 'HubA')
      # two more assertIsNone(get_tag('parcel6', ...)) lines, cut off at the screen edge
  ```
  Cases 05–10 are below the fold and not visible.

## Third batch: Level 3 spec (2 photos, supplied 2026-09-27) — verbatim

> **Level 3.** Introduce timestamped tag operations, allowing tags to be set at a specific timestamp and optionally
> expire after a TTL. It is guaranteed that the `timestamp` argument is non-decreasing across all operations from
> Level 3 onward, and that `ttl` is never negative.
>
> - `set_tag_at(self, parcel_id: str, tag: str, value: str, timestamp: int) -> None` — should set or overwrite the
>   `tag` to `value` for parcel `parcel_id` at the given `timestamp`. A tag set with `set_tag_at` does not expire
>   unless overwritten.
> - `get_tag_at(self, parcel_id: str, tag: str, timestamp: int) -> str | None` — should return the value of `tag` for
>   parcel `parcel_id` as it was at `timestamp`. Returns `None` if the tag did not exist or had expired at `timestamp`.
> - `remove_tag_at(self, parcel_id: str, tag: str, timestamp: int) -> bool` — should remove the `tag` from parcel
>   `parcel_id` only if the tag is currently valid at `timestamp`, i.e. it exists and has not yet expired at that time
>   (using the same exclusive expiry boundary as `get_tag_at`: a tag expiring at `timestamp` is already considered
>   expired). Returns `True` if the tag was removed this way. Returns `False` if the parcel does not exist, the tag was
>   never set on it, the tag was already removed, or the tag had already expired by `timestamp`.
> - `set_tag_with_hold(self, parcel_id: str, tag: str, value: str, timestamp: int, ttl: int) -> None` — should set or
>   overwrite the `tag` to `value` for parcel `parcel_id` at `timestamp`, with a time-to-live of `ttl` milliseconds.
>   The tag expires at `timestamp + ttl`. If `ttl` is `0`, the tag does not expire.
> - `list_tags_at(self, parcel_id: str, timestamp: int) -> list[str]` — should return a list of all tag-value pairs
>   for parcel `parcel_id` that were valid at `timestamp`, sorted lexicographically by tag name. Each entry is
>   formatted as `"tag(value)"`.
> - `list_tags_by_prefix_at(self, parcel_id: str, prefix: str, timestamp: int) -> list[str]` — should return a list of
>   all tag-value pairs for parcel `parcel_id` where the tag starts with `prefix` and was valid at `timestamp`, sorted
>   lexicographically by tag name. Each entry is formatted as `"tag(value)"`.
>
> **Examples**
>
> | Queries | Explanations |
> |---|---|
> | `set_tag_with_hold("parcel1", "status", "held", 100, 50)` | sets "status" to "held" at ts=100, expires after 50 (at 150) |
> | `get_tag_at("parcel1", "status", 120)` | returns "held"; valid at 120 |
> | `get_tag_at("parcel1", "status", 150)` | returns None; expired at 150 |
> | `get_tag_at("parcel1", "status", 180)` | returns None; still expired |
>
> Example demonstrating `remove_tag_at`:
>
> | Queries | Explanations |
> |---|---|
> | `set_tag_with_hold("parcel1", "status", "held", 20, 60)` | sets "status" to "held" at ts=20, expires after 60 (at 80) |
> | `remove_tag_at("parcel1", "status", 50)` | returns True; "status" is still valid at ts=50, so it is removed |
> | `set_tag_with_hold("parcel1", "hold_reason", "customs", 20, 60)` | sets "hold_reason" to "customs" at ts=20, expires after 60 (at 80) |
> | `remove_tag_at("parcel1", "hold_reason", 80)` | returns False; "hold_reason" already expired at ts=80 (exclusive boundary, same rule as getTagAt) |
> | `remove_tag_at("parcel1", "priority", …)` | returns False; parcel "parcel1" never had a tag "priority" (timestamp cut off in the photo) |

Notes:
- The second example calls `set_tag_with_hold(..., 20, ...)` right after `remove_tag_at(..., 50)`, which breaks the
  stated "non-decreasing timestamp" guarantee. The spec contradicts its own example; a correct solution must not rely
  on monotonic timestamps at Level 3.
- Differences from our earlier reconstruction: the TTL method is `set_tag_with_hold`, not `set_tag_at_with_ttl`;
  **`ttl == 0` means never expires**; timestamps are non-decreasing, not strictly increasing. `set_tag_at`,
  `get_tag_at`, `remove_tag_at`, `list_tags_at`, `list_tags_by_prefix_at`, the `"tag(value)"` format, lexicographic
  order by tag and the exclusive expiry boundary all matched.

## Fourth batch: Chi's mock run at Level 3 (pasted text, 2026-09-27)

- Chi's own attempt in a CodeSignal mock ("39m left", score `50/75`). The pasted interface docstrings confirm the Level 2
  names: `list_tags(self, parcel_id: str) -> list[str]` — "all tag-value pairs for parcel `parcel_id`, sorted
  lexicographically by tag name. Each entry is formatted as `"tag(value)"`. Returns an empty list if the parcel does
  not exist." — and `list_tags_by_prefix(self, parcel_id: str, prefix: str) -> list[str]` — "... where the tag starts
  with `prefix` ... Returns an empty list if no matching tags exist."
- `python3 -m unittest discover` ran **31 tests** with Levels 1–3 unlocked. Real Level 2 test names seen in failures:
  `test_level_2_case_02_simple_set_get_and_scan`, `case_04_multiple_parcels_with_same_tag_1`,
  `case_05_multiple_parcels_with_same_tag_2`, `case_07_resets_and_deletes_with_same_tags`,
  `case_09_mixed_multiple_operations_1`, `case_10_mixed_multiple_operations_2`. Assertions seen:
  `list_tags_by_prefix('parcel4', 'a') == ['address(1)', 'arrival_date(2)']`,
  `list_tags_by_prefix('parcel6', 'first') == ['first_scan(HubA)']`,
  `list_tags_by_prefix('a', 'b') == ['b(c)', 'bb(cc)', 'bc(ca)']`,
  `list_tags_by_prefix('pkg3', 'lane') == ['lane_1(dock_4)', 'lane_2(dock_5)', 'lane_3(dock_6)']`,
  `list_tags_by_prefix('a', 'c') == ['c(d)']`, `list_tags_by_prefix('a', 'a') == ['a(b)']`.
- The failure: after the Level 3 refactor, `list_tags_by_prefix` still had its Level 2 body, so it formatted the whole
  `(value, expires_at)` tuple: `"address(('1', None))"`. 6 failures, all in Level 2. Fix: delegate to
  `list_tags_by_prefix_at(parcel_id, prefix, None)`.

## Fifth batch: Level 4 spec (3 photos, supplied 2026-09-27) — verbatim

> **Level 4.** Introduce checkpoints that save and restore the state of all parcels.
>
> - `checkpoint(self, timestamp: int) -> int` — should create a checkpoint of the current state of all parcels at
>   `timestamp`. Returns the number of parcels that are currently alive (have at least one valid tag) at `timestamp`.
> - `restore_checkpoint(self, timestamp: int, timestamp_to_restore: int) -> None` — should restore the state of all
>   parcels to the latest checkpoint at or before `timestamp_to_restore`. That checkpoint's own timestamp (call it
>   `checkpoint_timestamp`) may be earlier than `timestamp_to_restore` if no checkpoint was taken exactly at that
>   time; only checkpoints at or before `timestamp_to_restore` are considered. After restoring, any tags added or
>   removed after `checkpoint_timestamp` are rolled back. Every restored tag that has a finite expiration is shifted
>   forward by `timestamp - checkpoint_timestamp`, so its new expiration becomes
>   `original_expiration + (timestamp - checkpoint_timestamp)`. Tags that were set without a TTL keep no expiration.
>   If no checkpoint exists at or before `timestamp_to_restore`, the operation has no effect. It is guaranteed that
>   `timestamp_to_restore` never exceeds `timestamp`.
>
> (Some line ends are cut off at the right edge of the photos; the text above is reassembled from the two overlapping
> shots and every clause appears in at least one of them.)
>
> **Example 1** (only the start is visible): `set_tag_with_hold("parcel1", "status", "held", 100, 100)` — sets
> "status" … at ts=100, expires … (at 200); `checkpoint(120)` — returns 1; … at ts=120; the rest is cut off.
>
> **Example demonstrating that the expiration shift is based on the actual checkpoint's timestamp, not
> `timestamp_to_restore`:**
>
> | Queries | Explanations |
> |---|---|
> | `set_tag_with_hold("parcel1", "route_east", "active", 30, 70)` | sets "route_east" to "active" at ts=30, expires after 70 (at 100) |
> | `checkpoint(31)` | checkpoint taken at ts=31 with "route_east" alive |
> | `set_tag_with_hold("parcel1", "route_west", "queued", 35, 25)` | sets "route_west" to "queued" at ts=35, expires after 25 (at 60) |
> | `checkpoint(41)` | checkpoint taken at ts=41 with "route_east" and "route_west" alive |
> | `restore_checkpoint(110, 35)` | restores to the checkpoint at ts=31 (the latest one at or before 35, not 35 itself); delta = 110 - 31 = 79 |
> | `get_tag_at("parcel1", "route_west", 115)` | returns None; "route_west" did not exist yet in the ts=31 checkpoint, so it is discarded |
> | `get_tag_at("parcel1", "route_east", 115)` | returns "active"; "route_east"'s expiration shifts by delta to 100 + 79 = 179, so it is still valid at ts=115 |

Differences from our reconstruction: the restore method is `restore_checkpoint`, not `restore`. The expiry rule
`original_expiration + (timestamp - checkpoint_timestamp)` is algebraically the same as our
`timestamp + (original_expiration - checkpoint_timestamp)`. "Latest at or before", "no checkpoint = no effect" and the
return value of `checkpoint` all matched.
