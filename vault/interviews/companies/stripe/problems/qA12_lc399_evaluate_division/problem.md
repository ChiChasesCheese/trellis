# qA12 · LC 399 Evaluate Division — BFS and weighted union-find, best-rate path, inconsistent rates

**Type:** LeetCode "Stripe" tag (algorithm) — the tag twin of the bespoke currency-conversion phone screen (q21) · **Stage:** phone screen · **Last asked:** tag snapshot 2026-07-12 (>6 months bucket); LC 5150083 comments (2024-05) "similar to LC 399"
**Frequency:** tag freq 76.9 (liquidslr All, 2025-06), 83.5 (liquidslr >6mo), 68.2 (shreeratn 2025-05), 87.5 all / 100.0 >6mo (snehasishroy 2026-07) · 4 tag mirrors + Hazeera65 / premjm-67 / TWINSRIRAM asked-list repos + LC 5150083 · **Confidence:** high

LC 399 · *Evaluate Division* · Medium · https://leetcode.com/problems/evaluate-division

## Context
This is the currency-conversion problem in LeetCode clothing: `a/b = 2.0` is "1 a buys 2 b", and a
query `a/c` is "what is the a→c rate through whatever quotes we have". The bespoke version — direct
quote, inverse quote, multi-hop path, payouts in cents — lives in `problems/q21_currency_conversion`
and is **not repeated here**. This problem drills the two graph techniques an interviewer expects you
to name and code (BFS with inverse edges; weighted union-find with path compression), then the two
questions Stripe's FX desk actually asks: which path gives the *best* rate when quotes disagree, and
which quotes are inconsistent with the rest.

## The problem (restated)
You are given `equations[i] = [A_i, B_i]` and `values[i]`, meaning `A_i / B_i = values[i]` (all
values positive; variables are short lowercase strings). For each `queries[j] = [C_j, D_j]` return
`C_j / D_j`, or `-1.0` if it cannot be derived (unknown variable, or no chain of equations connects
them). `x / x` is `1.0` when `x` appears in some equation and `-1.0` otherwise. Inputs are consistent
(no contradictions) and never divide by zero.
LC limits: `1 ≤ len(equations), len(queries) ≤ 20`, `0 < values[i] ≤ 20`, variable length 1..5.

## Input (stdin)
```
PART n                 # 1..4
A/B=v                  # one equation per line (v is a decimal)
...
?                      # separator
C/D                    # Parts 1–2: one query per line
SRC DST                # Part 3: exactly one line
                       # Part 4: nothing after the separator
```
Blank lines are ignored; whitespace around `/`, `=` is tolerated.

## Output
* Parts 1–2: one line per query, the value with five decimals (`6.00000`, `-1.00000`).
* Part 3: `rate path` e.g. `6.00000 a -> b -> c`, or `N/A`.
* Part 4: one line per conflicting equation, in input order: `index: A/B given=v implied=w` (five
  decimals), or a single line `consistent`.

## Rules
### Part 1 — LC signature, BFS  `calc_equation(equations, values, queries) -> list[float]`
Build an undirected weighted graph: edge `A→B` with weight `v` and `B→A` with weight `1/v` (the
inverse edge). Per query BFS from `C` accumulating the product of weights; the first time `D` is
reached, return the product (inputs are consistent, so any path gives the same value). Unknown
variable → `-1.0`; `C == D` and known → `1.0`. O(V + E) per query.

### Part 2 — weighted union-find  `calc_equation_union_find(equations, values, queries) -> list[float]`
`parent[x]` and `weight[x] = x / parent[x]`. `find(x)` compresses the path and returns
`(root, x / root)`. `union(A, B, v)`: with `(ra, wa) = find(A)`, `(rb, wb) = find(B)`, set
`parent[ra] = rb`, `weight[ra] = v · wb / wa`. Query: same root → `wa / wb`, else `-1.0`. Near-O(1)
per query after O(E α) preprocessing; results must match Part 1 to `1e-9`.

### Part 3 — best-rate path  `best_rate_path(equations, values, src, dst) -> tuple[float, list[str]] | None`
Now the quotes may disagree (real FX tables do). With the same graph (inverse edges included), return
the **maximum product over simple paths** from `src` to `dst` and the path attaining it (DFS, each
variable at most once so a bad quote cannot be looped). Ties: fewer hops first, then the
lexicographically smaller path. `src == dst` (known) → `(1.0, [src])`; unknown/disconnected → `None`.
Same rule as q21 Part 3's `best_conversion`; LC sizes (≤ 20 equations) keep the DFS cheap.

### Part 4 — inconsistent quotes  `find_conflicts(equations, values, rel_tol=1e-9) -> list[Conflict]`
Process equations in order with Part 2's union-find. When `A` and `B` are already in the same set,
the implied ratio is `wa / wb`; if `abs(implied − v) > rel_tol · v` the equation **conflicts** with the
quotes before it: record `Conflict(index, a, b, given, implied)` (NamedTuple) and **do not** apply it
(earlier quotes win). Equations that merely repeat a known ratio (within tolerance) are fine. Return the
conflicts in input order (`[]` when consistent).

## Worked examples
```
LC ex1  equations=[[a,b],[b,c]] values=[2.0,3.0]
        queries=[[a,c],[b,a],[a,e],[a,a],[x,x]]          -> [6.0, 0.5, -1.0, 1.0, -1.0]
LC ex2  equations=[[a,b],[b,c],[bc,cd]] values=[1.5,2.5,5.0]
        queries=[[a,c],[c,b],[bc,cd],[cd,bc]]            -> [3.75, 0.4, 5.0, 0.2]
LC ex3  equations=[[a,b]] values=[0.5]
        queries=[[a,b],[b,a],[a,c],[x,y]]                -> [0.5, 2.0, -1.0, -1.0]
Part 2  same answers for all three (union-find)
Part 3  equations a/b=2, b/c=3, a/c=7 (inconsistent):
        best a→c -> (7.0, [a, c])   direct 7 beats 2×3 = 6
        best c→a -> (1/6 ≈ 0.16667, [c, b, a])   inverse chain beats 1/7
        best b→b -> (1.0, [b]) ; best a→z -> None
        ex1 a→c -> (6.0, [a, b, c])
Part 4  a/b=2, b/c=3, a/c=7          -> [Conflict(2, a, c, 7.0, 6.0)]
        a/b=2, b/c=3, a/c=6          -> []   (consistent)
        a/b=2, b/a=0.5, a/b=2.0000000001 -> []  (within 1e-9 relative)
        a/b=2, a/b=2.1, b/c=3, a/c=6.3 -> [Conflict(1, a, b, 2.1, 2.0), Conflict(3, a, c, 6.3, 6.0)]
        (the rejected 2.1 is not applied, so a/c is still implied 6.0)
```
stdin for Part 1 ex1:
```
PART 1
a/b=2.0
b/c=3.0
?
a/c
b/a
a/e
a/a
x/x
```
→ `6.00000 / 0.50000 / -1.00000 / 1.00000 / -1.00000` (one per line)
stdin for Part 3 (`PART 3` / `a/b=2` / `b/c=3` / `a/c=7` / `?` / `c a`) → `0.16667 c -> b -> a`
stdin for Part 4 (`PART 4` / `a/b=2` / `b/c=3` / `a/c=7` / `?`) → `2: a/c given=7.00000 implied=6.00000`

## Edge cases hidden tests are known to target
- `x/x` for a variable that never appears → `-1.0` (not `1.0`); for a known one → `1.0`
- queries in the inverse direction of the only equation (`b/a` → `1/v`)
- disconnected components; an unknown variable on one side only
- a 20-equation chain: BFS product `2^20` and its inverse — no overflow, but float drift ~1e-12 is fine
- union-find: forgetting to recompute the weight during path compression (the classic bug)
- Part 3: the best path is not the shortest; a cycle must not be traversed twice
- Part 4: the tolerance is *relative*; a rejected equation must not be applied

## Variants seen in the wild
- q21 (phone screen): string rate table, direct / inverse / multi-hop / payouts in cents.
- LC 1st variant "return the path too" — Part 3 restricted to consistent inputs.
- "Detect arbitrage" — a cycle whose product exceeds 1 (Bellman-Ford on −log weights).

## Why Stripe asks it
It is the currency-conversion phone screen with the ambiguity removed, so the interviewer can hear the
candidate name BFS vs union-find and reason about inverse edges; the follow-ups (best rate across
inconsistent quotes, spotting a bad quote) are what Stripe's FX rate service does before every payout.

## Stripe-flavored follow-ups
1. Both techniques on demand (Part 1 BFS, Part 2 union-find) and when each wins (many queries → UF).
2. Quotes disagree: best rate path (Part 3) — then discuss arbitrage cycles.
3. Flag inconsistent quotes with a tolerance (Part 4) — then "which single quote to drop" (discussion).

## What this tests
skills: A02 weighted graph path product · A16 union-find · S08 deterministic tie-breaks · S19 incremental design · S21 stdlib fluency (deque, dict)

## Sources
- https://leetcode.com/problems/evaluate-division
- https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/5.%20All.csv (freq 76.9)
- https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/4.%20More%20Than%20Six%20Months.csv (freq 83.5)
- https://raw.githubusercontent.com/shreeratn/leetcode-company-wise-problems/main/Stripe/5.%20All.csv (freq 68.2)
- https://raw.githubusercontent.com/snehasishroy/leetcode-companywise-interview-questions/master/stripe/all.csv (freq 87.5 all / 100.0 >6mo)
- https://leetcode.com/discuss/post/5150083/ (2024-05 comments: currency problem "similar to LC 399")
- https://github.com/Hazeera65/stripe-interview/tree/main/round1 ; https://github.com/premjm-67/stripe-interview-questions (`ED.java`) ; https://github.com/TWINSRIRAM/Stripe_OA_Prep (evaluatedivision)
- catalog/raw/github_repos.md §30 (tag table, freq 76.9)
- problems/q21_currency_conversion (the bespoke twin — direct/inverse/multi-hop/payouts live there)
