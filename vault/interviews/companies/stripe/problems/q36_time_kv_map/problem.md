# q36 · Time-based Key-Value Map (MultiTimeMap) — versioned get, history, TTL

**Type:** phone screen / coding-challenge repo (LC 981 twin, Stripe tag) · **Stage:** phone screen · **Last asked:** 2023-01 (SogAniMic/Stripe_coding_challenge)
**Frequency:** 3 sources (SogAniMic notebook with verbatim statement, Murillo2380 `medium-stripe-timestamp-cache`, LeetCode Stripe tag "Time Based Key-Value Store") · **Confidence:** medium-high

## Context
Stripe objects are versioned: a customer's default payment method, a price, a Radar rule — each
has a value *as of* a point in time, and reports must answer "what was the value at time t?"
without rewriting history. This is the smallest possible model of that: a map whose every
write is stamped with a time, and whose reads are as-of a time.

## Input (stdin)
First line `PART n` (n ∈ 1..4). Blank lines ignored.
- Parts 1–3: one command per line, processed in order:
  `SET key value time [ttl]` · `GET key time` · `GETALL key time`. Keys and values are
  strings without spaces; `time`/`ttl` are non-negative integers.
- Part 4: one line of space-separated integers (may be empty).

## Output
- `GET` → the value, or `null`. `GETALL` → the values separated by single spaces (empty line if
  none). `SET` prints nothing.
- Part 4 → one integer.

## Rules
### Part 1 — `set(key, value, time)` / `get(key, time)`
`get` returns the value written with the **largest time ≤ `time`**; `None`/`null` if the key has
no write at or before `time`. Writes may arrive in any time order. A second `set` with the **same
key and the same time overwrites** the earlier value.

### Part 2 — `get_all(key, time)`
All versions of `key` with write time ≤ `time`, as values ordered by write time ascending
(one value per distinct time, because equal-time writes overwrite). Empty list if none.

### Part 3 — TTL (reconstructed)
`set(key, value, time, ttl)`: the version is valid for `t ∈ [time, time + ttl)` — **`time + ttl`
itself is expired**. `get(key, t)` still picks the version with the largest write time ≤ `t`; if
that version has expired at `t` the result is `None` (an expired version does **not** fall back
to an older one — the newer write superseded it). `ttl=None` never expires. `get_all` lists
versions with write time ≤ `t` that are not expired at `t`.

### Part 4 — `first_missing_positive(nums)` (bonus from the same source repo)
Smallest positive integer not in the list; duplicates and negatives allowed; `[]` → `1`.
Linear time (a set, or in-place index marking).

## Worked examples
Verbatim from the source — **three separate fresh maps** (see Variants):
```
PART 1
SET 1 1 0
SET 1 2 2
GET 1 1            -> 1
GET 1 3            -> 2
```
```
SET 1 1 5
GET 1 0            -> null
GET 1 10           -> 1
```
```
SET 1 1 0
SET 1 2 0
GET 1 0            -> 2
```
```
PART 2
SET k a 1
SET k c 3
SET k b 2
GETALL k 2         -> a b
GETALL k 0         ->              (empty line)
GETALL k 3         -> a b c
PART 3
SET s x 10 5
GET s 14           -> x
GET s 15           -> null
SET s y 20
GET s 100          -> y
PART 4
3 4 -1 1           -> 2
1 2 0              -> 3
```

## Edge cases hidden tests are known to target
- `get` before the first write → `null`; `get` exactly at a write time → that value (≤, not <)
- equal-time overwrite (the last verbatim block); out-of-order writes
- TTL boundary: `time + ttl - 1` alive, `time + ttl` expired; `ttl = 0` never readable
- expired newer version hides the older one (no fallback)
- unknown key; `GETALL` with nothing ≤ t → empty line, not `null`
- Part 4: `[]` → 1, `[1]` → 2, duplicates `[1,1,2,2]` → 3, all negative → 1, `[2]` → 1

## Variants seen in the wild
- The notebook pastes Daily Coding Problem #97's three example blocks as one sequence; read as a
  single map the second block (`get(1,0) → null` after `set(1,1,0)`) is contradictory, so the
  primary reading is three fresh maps (matches DCP #97 and LC 981).
- LC 981 guarantees strictly increasing timestamps per key (append + `bisect_right`); here writes
  may be out of order (`insort`), which is what the reference does.
- Murillo2380's "timestamp cache" variant adds eviction/expiry — modelled as Part 3.

## What this tests
skills: S03 domain modeling · S12 time handling · S13 inclusive/exclusive boundaries · S18 error paths · S19 incremental design

## Sources
- https://github.com/SogAniMic/Stripe_coding_challenge/blob/main/MultiTimeMap.ipynb (verbatim statement + examples; repo "Stripe_coding_challenge", 2023-01-27)
- https://github.com/SogAniMic/Stripe_coding_challenge (`first_missing_positive.ipynb`, Part 4 statement)
- https://github.com/Murillo2380/interview-coding-solutions `medium-stripe-timestamp-cache`
