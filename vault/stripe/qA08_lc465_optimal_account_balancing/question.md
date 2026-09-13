# qA08 · LC 465 Optimal Account Balancing — net balances, fewest transfers, the transfer list, dust write-off

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

## 关联知识点

- [[a10-min-transfers-settle-debts|A10 最少转账次数结清债务]]
- [[s03-small-record-modeling|S03 用小记录 + 按 id 索引的字典建模]]
- [[s17-ledger-balance-tracking|S17 台账式余额跟踪]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
- [[s21-python-stdlib-fluency|S21 语言熟练度与标准库]]
