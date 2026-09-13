# q24 · Server Allocator — smallest free server number and hostname allocate/deallocate

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

## 关联知识点

- [[a15-heap-topk-least-loaded|A15 堆做 top-k / 选最闲的]]
- [[s03-small-record-modeling|S03 用小记录 + 按 id 索引的字典建模]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s11-idempotency-dedup|S11 幂等 / 去重]]
- [[s18-validation-error-paths|S18 校验与错误路径]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
- [[s21-python-stdlib-fluency|S21 语言熟练度与标准库]]
