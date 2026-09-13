# q24 Server Allocator — report

## Summary
Hostname allocation for a fleet (`apibox1`, `apibox2`, `sitebox1`): hand out the lowest free
number per host type and reuse numbers when boxes are decommissioned. A classic Stripe phone
screen (two independent gists from 2016 and 2018 plus a Glassdoor entry), i.e. "first missing
positive" wrapped in a small stateful class — tests modelling, idempotent frees and choosing a
heap over an O(n) rescan.

## Sources & confidence
high — gist aranibatta (2016, unittest vectors copied verbatim), gist stealthbomber10 (2018, full
statement and examples copied verbatim), sahaia1 code1.py transcript, Glassdoor QTN_1221351
(ServerManager sequence, used as the Part 4 worked example), 1point3acres 1093485.

## Approach by part
1. `next_server_number`: `set(allocated)` then walk `n = 1, 2, …` — O(n); non-integers, zero,
   negatives and duplicates fall out of the membership test naturally.
2. `Tracker`: per type a high-water `next` counter and a min-heap of freed numbers; a `live`
   set of names makes `deallocate` idempotent and lets unknown names be ignored (or raised with
   `strict=True`). `split_hostname` splits at the trailing digit run (`apibox12` → 12) and
   rejects `apibox0` / leading zeros / no digits; host types ending in a digit are refused at
   `allocate` because they would make names ambiguous.
3. The heap gives O(log n) per operation — Part 3 is verified by a 5 000-step churn test
   against the brute-force `next_server_number` oracle and by the 10^6-command perf test.
4. `run_commands` streams `ALLOCATE`/`DEALLOCATE` lines; `main` reads `PART 1` number lists or
   streams commands line by line (keeps memory flat for 10^6 lines).

## Pitfalls hidden tests target
- `[]` → 1, `[2,3]` → 1, contiguous `1..n` → n+1; floats/zero/negatives ignored
- double deallocate creating two `apibox1`s; deallocating names never issued
- reuse in ascending order across several frees, then continuing from the high-water mark
- per-type independence; multi-digit numbers (`apibox10`)
- O(n) rescans per allocate (fails the 10^6 budget)

## Reconstructed rules / conflicts
- The "O(log n) heap" part is the reported follow-up direction, reconstructed as Part 3.
- Unknown deallocate: gists return `None` silently; a 2022 comment asks for validation — both
  supported (`deallocate -> bool`, `Tracker(strict=True)` raises `KeyError`).
- Hostname splitting at the trailing digit run and the "type may not end in a digit" rule are
  reconstructions needed to make `deallocate(name)` well defined.

## Complexity & measured cost
Part 1 O(n); Tracker O(log n) per op, O(live + freed) memory.
Measured: 0.50 s, 97 MB for 10^6 mixed commands (60 % allocate / 40 % deallocate, 4 types) — budget 2 s / 256 MB.

## Test inventory
15 tests — part1: 4 (incl. 1 io) · part2: 7 · part3: 2 · part4: 2 (1 io, 1 perf); edge 8 · io 2 · perf 1.

## Skills exercised
S03 state per type · S08 smallest-free ordering · S11 idempotent free · S18 malformed-name validation · S19 incremental design · S21 `heapq` · A15 heap selection
