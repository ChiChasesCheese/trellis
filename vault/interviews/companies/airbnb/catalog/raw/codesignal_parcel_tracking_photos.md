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
