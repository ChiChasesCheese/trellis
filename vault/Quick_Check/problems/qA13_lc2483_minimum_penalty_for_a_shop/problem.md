# qA13 · LC 2483 Minimum Penalty for a Shop — O(n) running penalty, one open/close window, k windows, weighted hours

**Type:** LeetCode "Stripe" tag (algorithm) — #1 on the tag; the twin of the bespoke store-closing OA/phone screen (q08) · **Stage:** phone screen part 1 / OA part 1 · **Last asked:** 2026-07 (InterviewDB "Closing Time — Phone"); tag snapshot 2026-07-12
**Frequency:** tag freq 100.0 (liquidslr All, 2025-06), 76.7 (liquidslr >6mo), 100.0 (shreeratn 2025-05), 100.0 all / 87.5 >6mo (snehasishroy 2026-07) · 4 tag mirrors + the 9 bespoke sources listed in q08 (pkafel gist, Hazeera65, TWINSRIRAM, premjm-67 `MP.java`, LC 2585038 / 3950781, …) · **Confidence:** high

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

## Edge cases hidden tests are known to target
- closing at `n` (never close) and at `0` (never open) are both valid answers
- ties → the **earliest** hour (`YNYN` → 1, not 3); strict `<` when updating the minimum
- all `'Y'`, all `'N'`, single character
- O(n²) recomputation of the penalty per hour times out at 10^5 (LC hidden test)
- Part 2: empty window when everything is `'N'`; equal scores → smallest open then smallest close
- Part 3: `k = 0`; `k` larger than the number of `'Y'`-runs; windows must be disjoint (no double-count)
- Part 4: zero weights make many hours tie → earliest again; weights up to 10^9 (int, no overflow issue)

## Variants seen in the wild
- q08 Parts 1–3 (bespoke): penalty for a given hour, best hour, `BEGIN … END` aggregate logs.
- Dublin L2 variant (LC 3950781): days and `L/R` tokens instead of hours and `Y/N`; same rule.
- "Return all hours with the minimum penalty" — collect instead of keeping the first.

## Why Stripe asks it
It is the phone-screen opener Stripe has used for years (see q08's nine sources): five minutes to
show a clean running-count loop and correct tie-breaking, then the bespoke parsing follow-ups. The
window / k-window / weighted extensions here are the *algorithmic* directions an interviewer takes
when the candidate finishes early.

## Stripe-flavored follow-ups
1. The shop chooses both opening and closing hour — maximum subarray in disguise (Part 2).
2. Split shifts: up to k windows — the O(n·k) DP (Part 3); then "return the windows" (parent pointers).
3. Weighted hours: staff cost vs. lost revenue per hour (Part 4).

## What this tests
skills: A01 prefix sums + argmin with tie-break · S05 threshold/tie semantics · S13 boundary discipline · S19 incremental design · S22 time-boxing

## Sources
- https://leetcode.com/problems/minimum-penalty-for-a-shop
- https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/5.%20All.csv (freq 100.0)
- https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/4.%20More%20Than%20Six%20Months.csv (freq 76.7)
- https://raw.githubusercontent.com/shreeratn/leetcode-company-wise-problems/main/Stripe/5.%20All.csv (freq 100.0)
- https://raw.githubusercontent.com/snehasishroy/leetcode-companywise-interview-questions/master/stripe/all.csv (freq 100.0 all / 87.5 >6mo)
- https://leetcode.com/discuss/interview-question/2585038/Stripe-or-Phone-Screen-or-Senior-SE-or-Reject + https://gist.github.com/pkafel/86470ca581350014bb89033fbffb9bb1
- https://github.com/premjm-67/stripe-interview-questions (`MP.java`) ; https://github.com/Hazeera65/stripe-interview/tree/main/round1 ; https://github.com/TWINSRIRAM/Stripe_OA_Prep (part1-3)
- catalog/raw/github_repos.md §1 and §30 (tag table, freq 100.0) ; catalog/raw/en_forums.md §8 / §A4
- problems/q08_store_closing_penalty (the bespoke twin — its BEGIN/END aggregate part is not repeated here)
