# qA02 LC 787 Cheapest Flights Within K Stops — report

## Summary
Bounded-hop cheapest path. The Stripe tag lists it at freq 56–89, three Stripe prep repos carry a
solution, and a 2026-04 onsite "algorithm" round (programhelp VO) asked it verbatim next to LC 465.
It is the abstract form of q22's shipping routes / q21's currency hops: the hop bound breaks Dijkstra's
greedy invariant, so the candidate must layer by hop count.

## Sources & confidence
high — liquidslr (82.0 / 88.8), shreeratn (56.4), snehasishroy (75.0 / 87.5), programhelp VO
2026-04-02, Hazeera65 / premjm-67 / TWINSRIRAM repos, github_repos.md §30.

## Approach by part
1. Bellman-Ford: `k+1` rounds, every round relaxes from a **copy** of the previous distances so one
   round = one extra flight. O((k+1)·E).
2. BFS by hops: frontier dict per layer; a city re-enters the frontier only if the new cost is
   strictly below the best ever seen (an earlier reach with ≤ cost has fewer hops and dominates).
   Same bound, typically far fewer relaxations.
3. Same layering carrying `(cost, hops, path_tuple)`; tuple comparison gives the tie-break "fewer
   flights, then lexicographic city list" for free.
4. Parse `FROM:TO:CARRIER:price`, filter by carrier (or `*`), intern city names, call Part 1.

## Pitfalls hidden tests target
- in-place relaxation (returns 4 instead of 10 on the chain-vs-direct test)
- `k=0` = direct only; `src == dst` → 0; cycles must not help; unreachable → -1
- BFS pruning against the current layer only (re-expands dominated states; wrong or slow)
- path tie-break must be independent of edge input order
- unknown city / carrier in Part 4 → -1, not KeyError

## Complexity & measured cost
Parts 1/3: O((k+1)·E) = 100 × 4950 ≈ 5·10^5 relaxations at LC max; Part 2 ≤ that. Measured: 0.15s
(all three algorithms in-process at LC max + script run); script run alone ≈ 0.1 s, ~15 MB. Budget 2 s / 256 MB.

## Test inventory
17 tests — part1: 7 (incl. 1 io, 1 perf) · part2: 4 · part3: 4 · part4: 2; edge 8 · fmt 1.

## Skills exercised
A03 bounded-hop shortest path · S03 modelling · S08 deterministic tie-break · S18 validation · S19 incremental design
