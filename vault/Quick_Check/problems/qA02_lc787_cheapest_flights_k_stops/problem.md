# qA02 · LC 787 Cheapest Flights Within K Stops — Bellman-Ford by rounds, BFS by hops, path, carriers

**Type:** LeetCode "Stripe" tag (algorithm) · **Stage:** onsite "algorithm" round (programhelp VO 2026-04-02), phone screen · **Last asked:** 2026-04 (programhelp VO write-up)
**Frequency:** tag freq 82.0 (liquidslr All), 88.8 (liquidslr >6mo), 56.4 (shreeratn 2025-05), 75.0 all / 87.5 >6mo (snehasishroy 2026-07); 3 GitHub prep repos carry a solution (Hazeera65, premjm-67, TWINSRIRAM); 1 dated VO report · **Confidence:** high

LC 787 · *Cheapest Flights Within K Stops* · Medium · https://leetcode.com/problems/cheapest-flights-within-k-stops

## Context
Stripe's routing problems — "UK:US:FedEx:4" shipping routes with *direct / one transfer / cheapest path*
(q22), currency conversion with a hop limit (q21), payout rails with at most one intermediary bank — are
all "cheapest path with a bounded number of hops". LC 787 is the canonical version and it was asked
verbatim in a 2026-04 Stripe onsite algorithm round together with LC 465. The hop bound is what makes
plain Dijkstra wrong: a cheaper route with too many stops must lose to a pricier direct one.

## The problem (restated)
There are `n` cities `0..n-1` and a list of one-way flights `[from, to, price]`. Given `src`, `dst` and an
integer `k`, return the cheapest total price of an itinerary from `src` to `dst` using **at most `k`
intermediate stops** (so at most `k+1` flights). Return `-1` when no such itinerary exists.
LC limits: `1 ≤ n ≤ 100`, `0 ≤ flights ≤ n(n-1)/2`, no duplicate `(from,to)` pairs, `1 ≤ price ≤ 10^4`,
`0 ≤ k < n`, `src ≠ dst`.

## Input (stdin)
```
PART n                    # 1..4
n src dst k               # Parts 1-3 (integers)
from to price             # one flight per line
...
```
Part 4 uses q22-style named routes:
```
PART 4
src dst k carrier         # carrier name, or * for "any mix of carriers"
FROM:TO:CARRIER:price     # one route per line
```
Blank lines ignored.

## Output
* Parts 1, 2, 4: one integer line (`-1` if unreachable).
* Part 3: `src -> a -> b -> dst (price)` or `-1`.

## Rules
### Part 1 — Bellman-Ford, k+1 rounds  `find_cheapest_price(n, flights, src, dst, k) -> int`
Run exactly `k+1` relaxation rounds over **all** edges; each round reads the **previous round's**
distances (copy the array), so a round adds at most one flight to every itinerary. Answer `dist[dst]`
after the last round, `-1` if still infinite. `src == dst` → 0.

### Part 2 — BFS by hops  `find_cheapest_price_bfs(n, flights, src, dst, k) -> int`
Same answer by a frontier expansion: layer 0 = `{src: 0}`; layer `h+1` = every out-neighbour of layer `h`
whose new cost is **strictly lower** than the best cost ever recorded for that city (a city reached
earlier with ≤ cost dominates: fewer hops *and* cheaper). Stop after `k+1` layers or when the frontier
empties. Must equal Part 1 on every input.

### Part 3 — return the itinerary  `cheapest_path(n, flights, src, dst, k) -> list[int] | None`
The cities of a cheapest itinerary, `src` first. Tie-break among equal-price itineraries: **fewer
flights first, then the lexicographically smaller list of city ids**. `None` if unreachable;
`[src]` when `src == dst`.

### Part 4 — carriers (q22 link)  `cheapest_with_carrier(routes, src, dst, k, carrier="*") -> int`
Routes are strings `FROM:TO:CARRIER:price` with city and carrier names. With a named carrier only that
carrier's routes may be flown; with `"*"` any mix is allowed. Otherwise Part 1 semantics (`≤ k` stops).
Unknown city → `-1`.

## Worked examples
```
LC ex1  n=4 flights=[[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]] src=0 dst=3 k=1 -> 700
        (0-1-2-3 costs 400 but needs 2 stops; 0-1-3 = 700)
LC ex2  n=3 flights=[[0,1,100],[1,2,100],[0,2,500]] src=0 dst=2 k=1 -> 200
LC ex3  same, k=0 -> 500
Part 3  ex1 k=1 -> [0, 1, 3] ; ex1 k=2 -> [0, 1, 2, 3] ; ex2 k=0 -> [0, 2]
        flights=[[0,1,5],[1,3,5],[0,2,5],[2,3,5],[0,3,10]] k=1 src=0 dst=3 -> [0, 3]   (10 either way:
        1 flight beats 2 flights); with [0,3,10] removed -> [0, 1, 3]  (lexicographic beats [0,2,3])
Part 4  routes=["US:UK:FedEx:5","UK:CA:FedEx:5","US:CA:UPS:7","US:UK:UPS:3","UK:CA:UPS:9"]
        (US, CA, k=1, FedEx) -> 10 ; (US, CA, k=1, UPS) -> 7 ; (US, CA, k=1, *) -> 7 ; (US, CA, k=0, FedEx) -> -1
        (US, CA, k=1, DHL) -> -1 ; (US, MX, 1, *) -> -1
```
stdin Part 1 ex1:
```
PART 1
4 0 3 1
0 1 100
1 2 100
2 0 100
1 3 600
2 3 200
```
→ `700`

## Edge cases hidden tests are known to target
- relaxing in place inside a round (lets one round add several flights) → wrong answer on ex1
- `k = 0` = direct flights only; `k = n-1` = unrestricted
- `src == dst` → 0 / `[src]`; no flights at all → -1; `dst` unreachable even without the hop limit
- cheaper route needs more stops than allowed (ex1); cycles (`2 -> 0`) must not help
- Part 2 pruning must be against the best cost *ever* seen, not just the current layer
- Part 3 tie-break: fewer flights, then lexicographic city ids

## Variants seen in the wild
- q22 Part 1–3 (direct / exactly one transfer / cheapest path) — the string-route form of this problem
  with method filtering (Part 4 here).
- Dijkstra on state `(city, stops_used)` — accepted alternative; heap key `(cost, stops)`.
- "Fewest hops, then cheapest" (currency conversion, q21) — BFS first, price as tie-break.

## Why Stripe asks it
Payouts, shipping and FX routing all bound the number of intermediaries; the candidate must notice that
the hop bound breaks Dijkstra's greedy invariant and pick a layered algorithm.

## Stripe-flavored follow-ups
1. Two algorithms and prove they agree (Parts 1–2).
2. Return the itinerary with a deterministic tie-break (Part 3) — what the customer sees.
3. Carrier / rail restrictions on string routes (Part 4) — links to q22 shipping routes.

## What this tests
skills: A03 bounded-hop shortest path · S03 modelling · S08 deterministic tie-break · S18 validation · S19 incremental design

## Sources
- https://leetcode.com/problems/cheapest-flights-within-k-stops
- https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/5.%20All.csv (82.0)
- https://raw.githubusercontent.com/liquidslr/leetcode-company-wise-problems/main/Stripe/4.%20More%20Than%20Six%20Months.csv (88.8)
- https://raw.githubusercontent.com/shreeratn/leetcode-company-wise-problems/main/Stripe/5.%20All.csv (56.4)
- https://raw.githubusercontent.com/snehasishroy/leetcode-companywise-interview-questions/master/stripe/all.csv (75.0 / 87.5)
- https://programhelp.net/en/vo/stripe-vo-interview-questions-and-solutions/ (2026-04-02 VO: "cheapest flight within k stops")
- https://github.com/Hazeera65/stripe-interview/tree/main/round1 ; https://github.com/premjm-67/stripe-interview-questions (`CF.java`) ; https://github.com/TWINSRIRAM/Stripe_OA_Prep (`cheapest_flight`)
- techprep.app/companies/stripe ; codinginterview.com (list mentions)
