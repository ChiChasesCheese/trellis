# q10 · Payment Intent Commands — INIT / CREATE / ATTEMPT / SUCCEED state machine

**Type:** bespoke OA · **Stage:** HackerRank OA (60 min, 3–4 parts unlocked in sequence) · **Last asked:** 2025-04-21 (csoahelp), 2025 summer-intern threads on 1point3acres
**Frequency:** 5 independent sources (csoahelp ×3 write-ups, 1point3acres ×4 threads, medium @azn7u1) · **Confidence:** high

## Context
A Stripe **PaymentIntent** tracks one payment through its lifecycle: it is created in
`requires_action`, moves to `processing` when the customer's payment method is attempted, and
lands in `succeeded` when the money is captured — only then does the merchant's balance move.
A refund reverses a succeeded payment exactly once. You are given a log of API commands, one per
line, and must replay them against an in-memory ledger. **Invalid commands are silently ignored**
— that is where nearly every hidden test lives.

## Input (stdin)
Optional first line `PART n` (n ∈ 1..4). Without it, `PART 3` is assumed (Parts 1–3 share one
command language; each part only *adds* commands). Then one command per line, whitespace
separated; blank lines ignored. Amounts and balances are integers in minor units (cents).
Up to 2×10^5 lines.

Parts 1–3 commands (no timestamps):
```
INIT   <merchant_id> <balance>
CREATE <payment_id> <merchant_id> <amount>
ATTEMPT <payment_id>
SUCCEED <payment_id>
UPDATE <payment_id> <amount>          (Part 2+)
FAIL   <payment_id>                   (Part 3+)
REFUND <payment_id>                   (Part 3+)
```
Part 4 commands: every line is prefixed with an integer timestamp, and `INIT` takes an optional
`refund_limit` (see Part 4). A command that is not part of the selected part is ignored.

## Output
One line per merchant that was `INIT`ed, `merchant_id balance`, **sorted by merchant_id in plain
string order**. Merchants with balance 0 are printed. No merchants → no output.

## Rules
Payment states: `REQUIRES_ACTION → PROCESSING → COMPLETED`. Every command that does not apply
(unknown id, wrong state, bad argument count, non-integer number) is ignored without output.

### Part 1 — create / attempt / succeed
- `INIT m balance`: create merchant `m` with the given balance (may be negative or 0).
  **If `m` already exists the command is ignored** (balance not reset).
- `CREATE p m amount`: create payment `p` for merchant `m` in state `REQUIRES_ACTION`.
  Ignored if `p` already exists, `m` does not exist, or `amount < 0` (0 is allowed).
- `ATTEMPT p`: `REQUIRES_ACTION → PROCESSING`. Any other state → ignored.
- `SUCCEED p`: `PROCESSING → COMPLETED` and **balance[m] += amount** (only now).

### Part 2 — update the amount
- `UPDATE p amount`: sets the amount **only while `p` is in `REQUIRES_ACTION`**; ignored in
  `PROCESSING`/`COMPLETED`, for unknown `p`, or when `amount < 0` (0 is allowed).

### Part 3 — fail and refund
- `FAIL p`: `PROCESSING → REQUIRES_ACTION` (the payment can then be `UPDATE`d and `ATTEMPT`ed
  again). Any other state → ignored.
- `REFUND p`: only if `p` is `COMPLETED` **and has not been refunded before**:
  `balance[m] -= amount` (the amount that was credited) and `p` is marked refunded. The state
  stays `COMPLETED`; a second `REFUND` is ignored. Balances may go negative.

### Part 4 — timestamps and a refund window (version C semantics)
Every line is `<t> <command …>` with integer `t` (non-negative, normally non-decreasing;
commands are processed **in input order**, `t` is used only for the refund window).
- `t INIT m balance [refund_limit]` — `refund_limit` absent → the merchant's payments are
  **always** refundable; `0` → **never** refundable; otherwise a refund is allowed only when
  `t_refund − t_create ≤ refund_limit` (inclusive).
- `t CREATE p m amount` — in this version **the payment completes immediately**: it is created
  in `COMPLETED` and `balance[m] += amount` at once. Same ignore rules as Part 1.
- `t REFUND p` — as Part 3, plus the window check. A refused refund does not mark the payment.
- Other commands (`ATTEMPT`/`SUCCEED`/`FAIL`/`UPDATE`) are accepted syntactically but never
  apply because every payment is already `COMPLETED`.
Difference from Parts 1–3 (documented because the source samples require it): Part 4's source
sample never `SUCCEED`s the payment yet the refund moves money, so `CREATE` must credit
immediately. The solution exposes `part4(lines, immediate_credit=False)` for the variant (source
version B) in which Part 4 keeps the full Part 1–3 state machine plus timestamps; there the
window is still measured from the `CREATE` timestamp (reconstructed).

## Worked examples
Example 1 (Part 1, source sample):
```
INIT m1 0
INIT m2 10
CREATE p1 m1 50
ATTEMPT p1
SUCCEED p1
CREATE p2 m2 100
ATTEMPT p2
```
→
```
m1 50
m2 10
```
(p2 is only `PROCESSING`, so m2 keeps its initial 10.)

Example 2 (Part 2):
```
PART 2
INIT m1 100
CREATE p1 m1 50
UPDATE p1 80
ATTEMPT p1
UPDATE p1 999
SUCCEED p1
UPDATE p1 -5
```
→ `m1 180` (the `UPDATE` to 80 applies in `REQUIRES_ACTION`; the later ones are ignored).

Example 3 (Part 3):
```
PART 3
INIT m1 0
INIT m1 500
CREATE p1 m1 40
ATTEMPT p1
FAIL p1
UPDATE p1 60
ATTEMPT p1
SUCCEED p1
REFUND p1
REFUND p1
CREATE p2 m1 25
REFUND p2
```
→ `m1 0` (second INIT ignored; FAIL re-opens p1 so UPDATE 60 applies; balance 60 then refunded
to 0; second refund and the refund of the never-succeeded p2 are ignored).

Example 4 (Part 4, source sample):
```
PART 4
1 INIT m1 1000 10
2 CREATE p1 m1 200
5 REFUND p1
15 REFUND p1
```
→ `m1 1000` (CREATE credits → 1200; refund at t=5: 5−2=3 ≤ 10 → 1000; t=15 already refunded).

Example 5 (Part 4, window boundaries):
```
PART 4
1 INIT a 0 5
1 INIT b 0 0
1 INIT c 0
2 CREATE pa a 100
2 CREATE pb b 100
2 CREATE pc c 100
7 REFUND pa
7 REFUND pb
99 REFUND pc
```
→
```
a 0
b 100
c 0
```
(7−2 = 5 ≤ 5 → refunded; b has limit 0 → never; c has no limit → always.)

## Edge cases hidden tests are known to target
- second `INIT` of the same merchant must not reset the balance
- `CREATE` with a duplicate payment id, an unknown merchant, or a negative amount → ignored;
  amount `0` is valid
- `SUCCEED` without a prior `ATTEMPT`, `SUCCEED` twice, `ATTEMPT` on a `COMPLETED` payment → all ignored
- `UPDATE` after `ATTEMPT` is ignored — but after `FAIL` it applies again; `SUCCEED` credits the
  *updated* amount
- `REFUND` twice, `REFUND` of a `PROCESSING`/`REQUIRES_ACTION` payment, refund of an updated
  amount uses the credited amount
- merchants with balance 0 are still printed; output sorted as strings (`m10` < `m2`)
- Part 4 window: `t_refund − t_create == refund_limit` is allowed, `+1` is refused;
  `refund_limit 0` never refunds; absent limit always refunds; a refused refund can be retried
- Part 4: `CREATE` credits immediately — no `SUCCEED` needed
- unknown command words / wrong argument counts / non-integer numbers are ignored, never crash

## Variants seen in the wild
- **Version B (2024-12-09 "Transaction Intent Management System")**: same machine renamed —
  states PENDING/IN_PROGRESS/DONE, commands START/NEW/PROCESS/COMPLETE/MODIFY/CANCEL/RETURN,
  every command timestamped, START carries `refund_limit`. `part4(lines, immediate_credit=False)`
  covers its semantics; rename the command table for the words.
- **Version C (2025-04-21)**: P1 `INIT`/`CREATE` only (CREATE credits immediately, `{"m1":1500}`),
  P2 `REFUND`, P4 timestamps + window — this is the Part 4 mode above.
- Output as a returned `list[str]` / dict `{"m1": 1500}` instead of stdout.

## What this tests
skills: S02 parsing · S03 modelling with records + dicts keyed by id · S10 state machines with
reversals · S11 idempotency (duplicate INIT/CREATE/REFUND) · S12 time windows · S18 validation
& error paths · S19 incremental design

## Sources
- csoahelp.com 2024-12-15 「[Stripe] 2025 Start – 14 Dec OA」(3 parts, version A — primary)
- csoahelp.com 2024-12-11 「[STRIPE] OA Transaction Intent Management System 2025 – 09 Dec」(version B)
- csoahelp.com 2025-04-22 「[Stripe] HackerRank OA 2025 start – 21 Apr」(version C, REFUND + window, 4 parts)
- 1point3acres thread-1091979「Stripe OA 2025 summer intern」; thread-1101931「STRIPE OA，支付系统」; thread-1085478 (16/19); thread-1099687「OA Stripe Interview.」(4 parts, 60 min)
- medium @azn7u1 「Stripe Intern OA + VO」(INIT/CREATE sample)
- https://docs.stripe.com/refunds (refund once, only succeeded payments)

## Clarifications (from adversarial review, 2026-08-26)
- Command arity is checked per part: in Parts 1–3 `INIT` takes exactly `merchant balance`; a third argument makes the line invalid (ignored). Only Part 4 accepts the optional `refund_limit`. (Bug found and fixed by adversarial review 2026-08-26.)
