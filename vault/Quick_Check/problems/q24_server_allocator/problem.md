# q24 · Server Allocator — smallest free server number and hostname allocate/deallocate

**Type:** bespoke · **Stage:** phone screen (classic; still listed on Glassdoor as "server id allocation") · **Last asked:** 1point3acres 1093485 (2024–25 摘要); Glassdoor QTN_1221351; gists 2016 / 2018
**Frequency:** 5 independent sources (gist aranibatta 2016 with unittest vectors, gist stealthbomber10 2018 with full statement, Glassdoor QTN_1221351 "ServerManager allocate/deallocate", 1point3acres 1093485, sahaia1/Stripe_Pyhton_libraries code1.py) · **Confidence:** high

## Context
Stripe's infrastructure names hosts by role plus a sequence number — `apibox1`, `apibox2`,
`sitebox1`. When a box "explodes" (is decommissioned) its number goes back into the pool and
the next box of that type takes the **lowest free number**, so the fleet never has gaps for long.
Part 1 is the pure function ("first missing positive"); Part 2 wraps it in a `Tracker` with
per-type counters; Part 3 asks for `O(log n)` per operation (a heap of freed numbers per type);
Part 4 drives it from a command stream.

## Input (stdin)
```
PART 1
5 3 1                 one query per line: the allocated numbers (space or comma separated; may be empty)
[]                    (an empty line or "[]" is the empty list)

PART 2 | PART 3 | PART 4
ALLOCATE apibox       commands, one per line
DEALLOCATE apibox1
```
Parts 2–4 share one program (Part 3 is the complexity requirement, Part 4 the driver);
`PART 2`, `PART 3` and `PART 4` all run the command interpreter. Up to 10^6 commands.

## Output
* Part 1: one integer per query line.
* Parts 2–4: the hostname returned by each `ALLOCATE`, in order. `DEALLOCATE` prints nothing
  (an unknown hostname is ignored silently).

## Rules
### Part 1 — `next_server_number(allocated) -> int`
Return the smallest **positive integer** not present in `allocated`. Duplicates, zero,
negatives and non-integers (the 2018 gist passes `1.5, 2.5, …`) are ignored: they can never be
the answer and never block one. `[]` → 1. O(n) time with a set.

### Part 2 — `Tracker().allocate(host_type) -> str`, `deallocate(hostname) -> bool`
A hostname is `host_type + number`. Each host type has its own pool starting at 1:
`allocate("apibox")` → `apibox1`, `apibox2`, …; `allocate("sitebox")` → `sitebox1`.
`deallocate("apibox1")` releases the number; the next `allocate("apibox")` **reuses the smallest
free number** (`apibox1`), not the next counter value. `deallocate` returns `True` if the name
was allocated, `False` if it is unknown (never allocated, already freed, malformed, or number 0)
— unknown names are ignored, not raised (the 2022 gist follow-up asks for this validation).
`hostname` is split at its **trailing digit run**: `apibox12` → (`apibox`, 12). Host types must
therefore not end in a digit (`allocate("box2")` → `ValueError`) and must be non-empty.
Deallocating a name whose number has leading zeros (`apibox01`) is unknown.

### Part 3 — O(log n) per operation (reconstructed as the performance part)
Per type keep `next` (the largest number ever handed out + 1) and a **min-heap of freed
numbers**; `allocate` pops the heap if non-empty else uses `next`; `deallocate` pushes onto the
heap only if the name is currently allocated (a set of live names guards double frees). Every
operation is O(log n); 10^6 commands must run in < 2 s.

### Part 4 — command stream
`ALLOCATE <type>` prints the name; `DEALLOCATE <name>` prints nothing. Commands are
case-sensitive keywords; blank lines are ignored.

## Worked examples
```
next_server_number([5, 3, 1]) == 2        next_server_number([]) == 1
next_server_number([3, 2, 1]) == 4        next_server_number([5, 4, 1, 2]) == 3
next_server_number([1, 2, 3, 4, 5]) == 6  next_server_number([5, 4, 3, 2]) == 1
next_server_number([1, 2, 3, 4, 6]) == 5  next_server_number([2, 3]) == 1
next_server_number([1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 5.5]) == 6
```
```
tracker.allocate("apibox")    -> "apibox1"
tracker.allocate("apibox")    -> "apibox2"
tracker.deallocate("apibox1") -> True
tracker.allocate("apibox")    -> "apibox1"     (reuses the freed number)
tracker.allocate("sitebox")   -> "sitebox1"    (separate counter)
```
Glassdoor sequence (stdin):
```
PART 4                     output
ALLOCATE apibox            apibox1
ALLOCATE apibox            apibox2
ALLOCATE sitebox           sitebox1
ALLOCATE apibox            apibox3
DEALLOCATE apibox2
ALLOCATE apibox            apibox2
```

## Edge cases hidden tests are known to target
- empty list → 1; list without 1 → 1; contiguous 1..n → n+1
- duplicates / zero / negatives / floats in the list
- deallocating an unknown, already-freed or malformed name (`apibox`, `apibox0`, `sitebox9`) is a no-op
- double deallocate must not make the number available twice (two `apibox1` live at once)
- freeing several numbers: allocation order is ascending (`free 3, free 1` → next is 1 then 3)
- once the freed pool is empty the counter continues from the high-water mark, not from `len(live)+1`
- types are independent: `apibox2` freed does not affect `sitebox`
- hostnames with multi-digit numbers (`apibox10` → 10, not `apibox1` + `0`)
- 10^6 commands in < 2 s (no O(n) scan per allocate)

## Variants seen in the wild
- `ServerManager` class name (Glassdoor) instead of `Tracker`; `deallocate` returning `None`.
- Part 1 as LC "first missing positive" (O(1) extra space, in-place) — the algorithmic cousin
  noted in the same repo.
- Validation follow-up: raise instead of ignore on unknown deallocate — `Tracker(strict=True)`
  raises `KeyError`.

## What this tests
S03 modelling (state per type) · S08 deterministic smallest-free ordering · S11 idempotency (double free) · S18 validation of malformed names · S19 incremental design · S21 stdlib (`heapq`) · A15 heap-based selection

## Sources
- https://gist.github.com/stealthbomber10/d85d44776ad58ba66d84ff76fd5be736 (2018-10-10, full statement + examples)
- https://gist.github.com/aranibatta/ffa87e94d117a86fc05b6940e626ee56 (2016-09-01, "Interview Code Written for Stripe", unittest vectors)
- https://github.com/sahaia1/Stripe_Pyhton_libraries/blob/main/code1.py (usage transcript)
- Glassdoor QTN_1221351 ("Create a ServerManager class with allocate(string) and deallocate(string)…")
- 1point3acres 1093485 (摘要: allocate/deallocate 电面)
