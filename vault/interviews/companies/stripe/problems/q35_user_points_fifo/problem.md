# q35 · User Points — payer point spending, FIFO by timestamp

**Type:** phone screen (live coding, ~35 min) · **Stage:** Stripe phone interview · **Last asked:** 2022 (joeytor/StripeInterview, README → "Phone Interview")
**Frequency:** 1 Stripe source with verbatim prompt + repo assertions (joeytor/StripeInterview `UserPoints.java`); the same prompt is the well-known Fetch Rewards take-home · **Confidence:** medium-high

## Context
A Stripe-powered loyalty program shows each user one points balance, but finance tracks which
**payer** (partner brand) funds every point. Earning is easy to attribute. Spending is not: the
user just spends, and accounting must decide whose points were used. Two rules: the **oldest
points are spent first**, and **no payer may go negative**. Partners also post corrections as
negative transactions.

## Input (stdin)
Commands, one per line, processed in order (state accumulates; no `PART` line). Blank lines ignored.
```
ADD,<payer>,<points>,<timestamp>     payer may contain spaces; points is a signed integer;
                                     timestamp ISO-8601 (2020-11-02T14:00:00Z or 2020-11-02 14:00:00)
SPEND,<points>                       points >= 0
BALANCE
```

## Output
One line per `SPEND` / `BALANCE` (nothing for `ADD`):
- `SPEND`: `payer,-deducted;payer,-deducted;…` in **order of first consumption** (oldest entry
  first); payers with no deduction omitted; an empty line if nothing was deducted (`SPEND,0`).
- `BALANCE`: `payer,balance;…` for **every payer ever added, in first-ADD order**, including 0.
- a `SPEND` that cannot be satisfied or an `ADD` that would make a payer negative prints
  `ERROR` and leaves the state unchanged.

## Rules
### Part 1 — `add(payer, points, timestamp)` + `balances()`
Balance of a payer = sum of its transaction points. `balances()` returns every payer in first-add
order.

### Part 2 — `spend(points)` FIFO
Sort all transactions by timestamp (ties: insertion order). Walk the positive entries oldest first,
taking `min(remaining, need)` from each until `need == 0`. Each entry remembers what is left, so a
later spend continues where the previous one stopped. Return `[(payer, -deducted), …]` aggregated
per payer, ordered by first consumption.

### Part 3 — negative transactions
A negative transaction is a correction by that payer. Before the FIFO walk, each negative
transaction (in timestamp order) **cancels that payer's oldest remaining positive points**,
regardless of whether those points were earned before or after it — a payer's points, not the
user's, are reduced. An `ADD` that would make the payer's balance negative is rejected (`ERROR`).

### Part 4 — multiple spends and insufficient points (reconstructed)
`spend` is atomic: if `points` exceeds the total balance, raise `ValueError` (`ERROR` on stdout)
and change nothing. Spends may be repeated; each one continues consuming from what is left.

## Worked examples
Verbatim from the source (adds in this order, then spend 5000, then balances):
```
ADD,DANNON,1000,2020-11-02T14:00:00Z
ADD,UNILEVER,200,2020-10-31T11:00:00Z
ADD,DANNON,-200,2020-10-31T15:00:00Z
ADD,MILLER COORS,10000,2020-11-01T14:00:00Z
ADD,DANNON,300,2020-10-31T10:00:00Z
BALANCE          -> DANNON,1100;UNILEVER,200;MILLER COORS,10000
SPEND,5000       -> DANNON,-100;UNILEVER,-200;MILLER COORS,-4700
BALANCE          -> DANNON,1000;UNILEVER,0;MILLER COORS,5300
```
Why `DANNON,-100`: DANNON's 300 (10-31 10:00) is the oldest entry; the −200 (10-31 15:00)
cancels 200 of it, leaving 100; then UNILEVER 200 (10-31 11:00); then 4,700 of MILLER COORS.
```
ADD,A,100,2021-01-01T00:00:00Z
ADD,B,100,2021-01-02T00:00:00Z
SPEND,150         -> A,-100;B,-50
SPEND,100         -> ERROR            (only 50 left)
SPEND,50          -> B,-50
BALANCE           -> A,0;B,0
```
```
ADD,A,50,2021-01-01T00:00:00Z
ADD,A,-80,2021-01-03T00:00:00Z        -> ERROR   (A would be -30)
ADD,A,100,2021-01-05T00:00:00Z
ADD,A,-80,2021-01-03T00:00:00Z        (now fine: A = 70)
SPEND,70          -> A,-70            (−80 cancelled the 50 and 30 of the 100)
```

## Edge cases hidden tests are known to target
- adds arrive **out of timestamp order** (the verbatim example does)
- a negative transaction dated *before* the positive it cancels, and one whose payer has only
  later-dated positives
- `SPEND` exactly equal to the total balance (ok), one more (`ERROR`, state unchanged), `SPEND,0`
- same timestamp for two entries → insertion order
- payers with 0 balance still listed; payer names with spaces (`MILLER COORS`)
- spend output aggregated per payer even when the payer has several consumed entries

## Variants seen in the wild
- Fetch Rewards take-home: same rules exposed as an HTTP service (`/add`, `/spend`, `/balance`) with
  JSON bodies — the repo's assertion strings (`[UNILEVER: 200, MILLER COORS: 10000, DANNON: 1100]`)
  use Java `HashMap` order, i.e. no order guarantee.
- Points as `String` in the record (source typo); treat as integers.

## What this tests
skills: S02 parsing · S03 domain modeling · S08 deterministic ordering · S10 event streams · S12 timestamps · S17 ledger balances · S18 error paths

## Sources
- https://github.com/joeytor/StripeInterview `src/main/java/UserPoints.java` (README → Phone Interview; verbatim prompt and JUnit assertions)
