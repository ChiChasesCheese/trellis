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
