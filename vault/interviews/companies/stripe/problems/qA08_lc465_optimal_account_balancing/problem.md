# qA08 · LC 465 Optimal Account Balancing — net balances, fewest transfers, the transfer list, dust write-off

**Type:** LeetCode "Stripe" tag (algorithm) · **Stage:** virtual-onsite "algorithm" round (programhelp VO 2026-04-02), also the follow-up to the bank-rebalancing phone/VO problem (q32) · **Last asked:** 2026-04 (programhelp VO), 2026-01 (LeetCode 7521596 "Minimum Transactions for Multi-Party Debt Settlement")
**Frequency:** tag freq 51.5 (shreeratn All, 2025-05 snapshot; absent from liquidslr 2025-06 and snehasishroy 2026-07 mirrors) · 3 dated candidate reports (programhelp H1 2026-04, programhelp H3 2026-02 "min transactions DFS", LeetCode 7521596 2026-01) + Hazeera65 `round1/465optimalaccountBalancing/` write-up · **Confidence:** high (repeatedly reported as the *follow-up*), medium as a stand-alone tag question

LC 465 · *Optimal Account Balancing* · Hard · https://leetcode.com/problems/optimal-account-balancing

## Context
Stripe Connect platforms, Treasury and the internal "move money between bank accounts" tooling all end
the day with a pile of IOUs between accounts. Every transfer costs money and reconciliation effort, so
the question interviewers keep asking (q32 Part 2, the VO write-ups above) is: after netting everybody
out, what is the **fewest** number of transfers that leaves every account at zero? LC 465 is the
minimal form of that question. The bespoke q32 keeps a minimum-balance target and named accounts; this
problem keeps just the graph of IOUs, and adds the two follow-ups an interviewer reaches for next:
*show me the transfers*, and *what if tiny balances are not worth a transfer at all* (dust write-off).

## The problem (restated)
You are given `transactions`, a list of `[from, to, amount]` records meaning "party `from` handed
`amount` to party `to`". Parties are small integers, `from != to`, amounts are positive integers.
Whoever received money owes it back. Return the **minimum number of transfers** needed so that
afterwards nobody owes anybody anything — every party's net credit (given minus received) is zero. Any party may pay any other party; the
transfers do not have to follow the original edges.
LC limits: `1 ≤ len(transactions) ≤ 8`, `0 ≤ from, to < 12`, `from != to`, `1 ≤ amount ≤ 100`.
Consequently at most 12 parties have a non-zero net balance.

## Input (stdin)
```
PART n                 # 1..3
THRESHOLD t            # Part 3 only, non-negative integer
from,to,amount         # one transaction per line
...
```
Blank lines are ignored; whitespace around `,` is tolerated.

## Output
* Part 1: one line, the minimum number of transfers.
* Part 2: first line the count, then one line per transfer `from: A, to: B, amount: X` in the order
  the solver emits them (deterministic, see Part 2).
* Part 3: the transfer lines as in Part 2 (the platform account prints as `PLATFORM`), then one line
  `written_off: p=net,p=net,...` (ascending party; `written_off: none` when nothing was written off).

## Rules
### Part 1 — LC signature  `min_transfers(transactions) -> int`
1. Net every party: `net[p] = Σ given − Σ received` (positive = is owed money, negative = owes).
   Drop parties with `net == 0`. The remaining nets sum to zero.
2. Exact search over the non-zero nets (≤ 12 of them): take the first unsettled party `i`, try to
   settle it completely against each later party `j` of the opposite sign (`net[j] += net[i]`,
   `net[i] = 0`, one transfer), recurse. Pruning that is expected: (a) skip a `j` whose current value
   equals one already tried at this level; (b) stop the loop after a `j` that exactly cancels `i`
   (`net[i] + net[j] == 0`) — an exact match is never worse; (c) abandon a branch whose count can no
   longer beat the best found.
   Justification the interviewer wants to hear: some optimal solution settles at least one party per
   transfer, so restricting each transfer to "fully settle the current party" loses nothing.
3. Also expose `min_transfers_bitmask(transactions) -> int`: with `n` non-zero nets the answer is
   `n − (maximum number of disjoint zero-sum subsets the nets can be split into)`; compute the
   maximum by a DP over the `2^n` subsets (`dp[mask] = max_i dp[mask without i] + [sum(mask) == 0]`).
   Both functions must agree on every input.

### Part 2 — the transfers  `settle(transactions) -> list[Transfer]`
`Transfer(frm, to, amount)` (NamedTuple; `frm` because `from` is a keyword). Return one optimal
transfer list; `len(settle(t)) == min_transfers(t)` and applying the transfers zeroes every net.
Determinism: parties are processed in ascending id; at each level the candidates `j` are tried in
ascending id; the **first** list found with the minimal count is returned (a later list of equal
length never replaces it). Each transfer moves `|net[i]|` from the party whose *current* net is
negative (owes) to the one whose current net is positive (is owed) — in a chain the receiver may be
over-paid and forward the excess in a later transfer. Empty / fully cancelled input → `[]`.

### Part 3 — dust write-off  `settle_with_writeoff(transactions, threshold) -> Settlement`   (designed)
A transfer costs a flat fee, so a balance smaller than `threshold` is not worth moving. Rule:
every party with `0 < |net| < threshold` (**strict**: a net exactly equal to the threshold is still
settled) is **written off** — its claim is forfeited or its debt forgiven, and the platform absorbs
the difference. Concretely: remove the written-off parties, then add a virtual party `PLATFORM`
(id `-1`, sorted first) whose net is `−(sum of the remaining nets)` when that is non-zero, and run
Part 2's search on what is left. Return `Settlement(transfers, written_off)` where `written_off` is
the list of `(party, net)` pairs written off, ascending by party. `threshold = 0` reproduces Part 2
exactly.

## Worked examples
```
LC ex1  [[0,1,10],[2,0,5]]                         -> 2
        nets: 0:+5, 1:-10, 2:+5  → 1 pays 0 five, 1 pays 2 five
LC ex2  [[0,1,10],[1,0,1],[1,2,5],[2,0,5]]         -> 1
        nets: 0:+4, 1:-4, 2:0   → 1 pays 0 four
Part 1  [[0,1,5],[1,0,5]]                          -> 0   (everything cancels)
        [[0,1,6],[0,2,2],[0,3,2],[0,4,2]]          -> 4   nets 0:+12, 1:-6, 2:-2, 3:-2, 4:-2
                                                          (each of the four must pay 0 separately)
        [[0,1,5],[2,3,5],[4,5,3],[6,7,3]]          -> 4   (two independent 5-groups, two 3-groups)
        [[0,1,3],[0,2,7],[3,4,10]] nets 0:+10,1:-3,2:-7,3:+10,4:-10 -> 3   ({3,4} cancels; 1 and 2 pay 0)
Part 2  LC ex1 -> [Transfer(1,0,5), Transfer(1,2,5)]
        LC ex2 -> [Transfer(1,0,4)]
        [[0,1,3],[0,2,7],[3,4,10]] -> [Transfer(1,0,10), Transfer(2,1,7), Transfer(4,3,10)]
        (first-found: party 0 is settled fully by 1, who over-pays by 7 and is reimbursed by 2 —
         a chain of 3 is as good as the "obvious" 1→0 3, 2→0 7, 4→3 10; both are optimal)
Part 3  [[0,1,10],[2,0,5]] threshold 6  -> nets 0:+5,1:-10,2:+5 → 0 and 2 written off (5 < 6, claims
        forfeited); remaining 1:-10, PLATFORM:+10 → transfers [Transfer(1,-1,10)], written_off [(0,5),(2,5)]
        same, threshold 5 -> nothing written off (5 is not < 5) → Part 2's answer
        [[0,1,10],[1,0,1],[1,2,5],[2,0,5]] threshold 5 -> 0:+4,1:-4 both written off; remaining nets
        sum to 0 → no PLATFORM party; transfers [], written_off [(0,4),(1,-4)]
        [[0,1,3],[0,2,7]] threshold 4 -> 1's debt of 3 forgiven; PLATFORM:-3 covers it:
        [Transfer(-1,0,3), Transfer(2,0,7)], written_off [(1,-3)]
```
stdin for Part 2, LC ex1:
```
PART 2
0,1,10
2,0,5
```
→
```
2
from: 1, to: 0, amount: 5
from: 1, to: 2, amount: 5
```
stdin for Part 3 (`PART 3` / `THRESHOLD 6` / `0,1,10` / `2,0,5`) →
```
from: 1, to: PLATFORM, amount: 10
written_off: 0=5,2=5
```

## Edge cases hidden tests are known to target
- sign convention: `[a,b,x]` = a handed x to b, so **b owes a** — reversed nets give reversed transfers
- everything nets to zero → 0 transfers, empty list
- a single transaction → 1; a party that appears only as a pass-through (net 0) must be dropped
- zero-sum subsets: `n − #subsets`, not `n − 1` (the naive "everyone pays one hub" answer)
- one debtor owing k creditors (or one creditor) → exactly k transfers, whatever the amounts
- duplicate nets (several parties with the same balance) — the duplicate-skip pruning must not change
  the answer, only the speed
- the largest LC input: 12 non-zero nets with few zero-sum subsets — a DFS without pruning is
  ~11! branches; with the three prunings it is milliseconds
- Part 3: `|net| == threshold` is settled, `|net| == threshold − 1` is written off; when the written-off
  nets cancel each other exactly the platform party must not appear

## Variants seen in the wild
- q32 Part 2: the same search, but with a minimum-balance target per named account and a greedy
  fallback above 12 non-zero accounts (the VO follow-up "scale to hundreds of people" — LC 7521596).
- "Return any settlement, not the optimum" (q32 Part 1 / A3): a two-pointer greedy over sorted nets.
- Debt records given as names/strings (`"alice,bob,10"`) instead of ints.
- "Minimum number of transactions" phrased as splitting a dinner bill (Splitwise) — identical.

## Why Stripe asks it
It is the algorithm behind "move money so that every account is where it should be with as few
transfers as possible" — payouts, Connect platform sweeps, Treasury rebalancing. The interviewer
listens for: netting first, the zero-sum-subset insight, why "settle one party per transfer" is safe,
and honest pruning arguments rather than a claimed polynomial algorithm (the problem is NP-hard).

## Stripe-flavored follow-ups
1. Return the transfers, not just the count — Part 2 (the payout instructions).
2. Small balances are not worth a transfer (fees) — Part 3's write-off with the platform absorbing the
   residual; compare q32 Part 4 where the fee is deducted from the sender instead.
3. Hundreds of accounts: keep the exact search for the ≤ 12 non-zero accounts within each connected
   group, fall back to the sorted two-pointer greedy otherwise (q32 Part 2's fallback).

## What this tests
skills: A10 min transactions to settle debts · S03 domain records · S17 ledger-style balances · S19 incremental design · S21 stdlib fluency (recursion, bitmask DP)

## Sources
- https://leetcode.com/problems/optimal-account-balancing
- https://raw.githubusercontent.com/shreeratn/leetcode-company-wise-problems/main/Stripe/5.%20All.csv (freq 51.5)
- https://programhelp.net/en/vo/stripe-vo-interview-questions-and-solutions/ (2026-04-02 VO: "min transactions to settle group debts")
- https://programhelp.net/en/vo/stripe-sde-interview-vo-5-round-interview-experience/ (2026-02-27 VO: min transactions DFS + audit)
- https://leetcode.com/discuss/post/7521596/ (2026-01-24 VO: "Minimum Transactions for Multi-Party Debt Settlement")
- https://github.com/Hazeera65/stripe-interview/tree/main/round1 (465optimalaccountBalancing folder)
- catalog/raw/github_repos.md §30 (corroborating repos), catalog/raw/en_forums.md §A3 / §A12
- problems/q32_money_transfer_rebalancing (the bespoke twin; Part 2 = this search with a target balance)
