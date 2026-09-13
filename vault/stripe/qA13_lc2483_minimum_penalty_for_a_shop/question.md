# qA13 · LC 2483 Minimum Penalty for a Shop — O(n) running penalty, one open/close window, k windows, weighted hours

LC 2483 · *Minimum Penalty for a Shop* · Medium · https://leetcode.com/problems/minimum-penalty-for-a-shop

## Context
The single most-attested Stripe question. The bespoke version — penalty for a given closing hour,
best closing hour, `BEGIN … END` aggregate logs with garbage — is `problems/q08_store_closing_penalty`
and is **not repeated here**. This directory drills the LeetCode form (one pass, earliest hour on a
tie) and pushes in the direction the bespoke follow-ups do *not* go: a shop that also chooses when to
**open** (one window), up to **k** opening windows per day (a Stripe Terminal merchant with split
shifts), and hours with different **weights** (staff cost vs. lost revenue), which is the penalty a
Capital/Terminal analytics report would actually compute.

## The problem (restated)
`customers` is a string of `'Y'`/`'N'`; character `i` says whether any customer showed up during hour
`i`. The shop can close at any hour `j` in `0..n` (closing at `j` means it is open during hours `0..j−1`
and closed during `j..n−1`). Penalty of closing at `j` = number of open hours with no customer (`'N'`
before `j`) + number of closed hours with a customer (`'Y'` at or after `j`). Return the **earliest**
`j` with the minimum penalty. LC limits: `1 ≤ n ≤ 10^5`.

## Input (stdin)
```
PART n                 # 1..4
customers              # the Y/N string (spaces inside are ignored, so "Y Y N Y" also works)
K k                    # Part 3 only
w1 w2 ... wn           # Part 4 only: one non-negative integer weight per hour
```
Blank lines are ignored.

## Output
* Parts 1 and 4: one line, the closing hour.
* Part 2: one line `open close penalty`.
* Part 3: one line, the minimum penalty.

## Rules
### Part 1 — LC signature  `best_closing_time(customers) -> int`
Start with `penalty(0) = count('Y')`; moving the closing hour from `j` to `j+1` subtracts 1 if
`customers[j] == 'Y'` (that hour is now served) and adds 1 if it is `'N'` (now an idle open hour).
Keep the minimum with a **strict `<`** so the earliest hour wins ties. One pass, O(n), O(1) extra.
Also expose `penalty(customers, j) -> int` for a given closing hour (O(n) is fine).

### Part 2 — choose open *and* close  `best_open_close(customers) -> Window`
The shop is open during `[open, close)` (half-open, `0 ≤ open ≤ close ≤ n`; `open == close` = never
opens). Penalty = idle open hours (`'N'` inside) + missed customers (`'Y'` outside). Return
`Window(open, close, penalty)` (NamedTuple). Equivalent to: score each hour `+1` for `'Y'`, `−1` for
`'N'`; penalty = `count('Y') − (score of the window)`; so maximise the window score (maximum subarray
with the empty window allowed at score 0). Ties: smallest `open`, then smallest `close`. O(n) with
prefix sums: for each `close`, the best `open` is the earliest index with the minimum prefix.

### Part 3 — up to k windows  `min_penalty_k_windows(customers, k) -> int`
Split shifts: at most `k` disjoint open windows. Minimum penalty = `count('Y') − (max total score of
≤ k disjoint sub-arrays)`. DP over the prefix, O(n·k) time and O(n) memory:
`g = max(g, f_prev[i−1]) + s[i−1]` (best with the j-th window ending exactly at hour `i−1`) and
`f[i] = max(f[i−1], g)`. `k = 0` → `count('Y')`; `k = 1` → Part 2's penalty; `k ≥` number of
`'Y'`-runs → 0. Returning the windows themselves is a discussion point (parent pointers), not required.

### Part 4 — weighted hours  `best_closing_time_weighted(customers, weights) -> int`
`weights[i] ≥ 0` is the cost of hour `i` being "wrong" (idle-open `'N'` or missed `'Y'`). Penalty of
closing at `j` = `Σ weights[i]` over `i < j` with `'N'` + `Σ weights[i]` over `i ≥ j` with `'Y'`.
Earliest `j` on ties; same running pass as Part 1 with `±weights[j]`. Part 1 is Part 4 with all
weights 1.

## Worked examples
```
LC ex1  "YYNY"   -> 2   penalties by hour: 3, 2, 1, 2, 1 → earliest minimum is hour 2
LC ex2  "NNNNN"  -> 0   penalties: 0, 1, 2, 3, 4, 5
LC ex3  "YYYY"   -> 4   penalties: 4, 3, 2, 1, 0
Part 1  "N" -> 0 ; "Y" -> 1 ; "YNYN" -> 1 (penalties 2,1,2,1,2 → earliest 1)
Part 2  "YYNY"      -> Window(0, 2, 1)   ([0,2) scores 2; [0,4) also scores 2 → smaller close wins)
        "NNYYNNYN"  -> Window(2, 4, 1)   (3 Y total; window [2,4) scores 2 → penalty 1)
        "NNNNN"     -> Window(0, 0, 0)   (never open)
        "YYYY"      -> Window(0, 4, 0)
        "NYN"       -> Window(1, 2, 0)
Part 3  "NNYYNNYN" k=1 -> 1 ; k=2 -> 0 ([2,4) and [6,7)) ; k=0 -> 3 ; k=5 -> 0
        "YNYNY"     k=1 -> 2 (window [0,5) scores 1 → 3−1) ; k=2 -> 1 ; k=3 -> 0
Part 4  "YYNY" weights [1,1,5,1]  -> 2   (penalties 3, 2, 1, 6, 5)
        "YYNY" weights [1,1,1,10] -> 4   (penalties 12, 11, 10, 11, 1)
        "YYNY" weights [1,1,1,1]  -> 2   (= Part 1)
```
stdin for Part 2:
```
PART 2
NNYYNNYN
```
→ `2 4 1`
stdin for Part 3 (`PART 3` / `NNYYNNYN` / `K 2`) → `0` ; Part 4 (`PART 4` / `YYNY` / `1 1 5 1`) → `2`

## 关联知识点

- [[a01-prefix-sum-argmin|A01 前缀和 + 带 tie-break 的 argmin]]
- [[s05-threshold-semantics|S05 阈值语义：严格 vs 非严格、计数 vs 比例、最小量门槛]]
- [[s13-closed-intervals-offbyone|S13 闭区间、补齐空隙、off-by-one 纪律]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
- [[s22-timeboxing|S22 时间盒]]
