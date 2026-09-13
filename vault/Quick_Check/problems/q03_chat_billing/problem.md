# q03 · Chat Billing — monthly billing by token usage and plan switching

**Type:** bespoke OA · **Stage:** HackerRank OA (60 min) · **Last asked:** 2026-04-17 (1point3acres 题库)
**Frequency:** 4 independent mentions (1point3acres 题库 ×2 entries, 1point3acres company page, 1024bbs 10992) · **Confidence:** high

## Context
Stripe Billing bills an AI-chat product per calendar month. Every chat session is one record.
Two plans exist: `payg` (pay-as-you-go, metered) and `fixed` (subscription with an included
allowance). A user may switch plans mid-month, so the same user can have sessions on both plans.

## Input (stdin)
One session per line, `user_id,input_tokens,output_tokens,plan`. Blank lines are ignored.
`plan ∈ {payg, fixed}`; tokens are non-negative integers. Up to 10^5 lines.

## Output
One line per user, **sorted by `user_id` (plain string order)**, formatted `user_id: $x.xx`
(two decimals, `$` sign, `: ` separator). **Every user appears, including $0.00 users.**

## Rules
### Part 1 — pay-as-you-go
Tokens are billed in **blocks of 100, per session, complete blocks only**
(`floor(tokens / 100)`; remainders of different sessions are *never* pooled).
Input blocks cost **$0.03** each, output blocks **$0.04** each.

### Part 2 — fixed plan
`fixed` costs a flat **$15.00 per month** and includes **40,000 tokens** (input + output combined).
Each fixed session still rounds down to 100-blocks first (`billable = floor(tokens/100)*100`),
then billable tokens consume the allowance **in input order, input tokens before output tokens
inside a session**. Tokens beyond the allowance are charged at the pay-as-you-go block prices
(input $0.03 / output $0.04 per 100).

### Part 3 — plan switching (proration)
If a user has sessions on both plans in the month:
`r = fixed_sessions / total_sessions` (session counts, not tokens).
Prorated fee = `$15.00 × r` rounded **half-up to the cent**; prorated allowance =
`floor(40,000 × r)` tokens. `payg` sessions are billed as in Part 1 regardless of `r`.
`fixed` sessions consume the prorated allowance as in Part 2; overage at payg block prices.
`total = payg_cost + prorated_fee + fixed_overage`.

## Worked examples
```
alice,250,120,payg        -> alice: $0.10    (2 in-blocks × 0.03 + 1 out-block × 0.04)
bob,99,99,payg            -> bob: $0.00      (no complete block)
carol,30000,15000,fixed   -> carol: $17.00   (45,000 billable − 40,000 = 5,000 over →
                                              all overage is output → 50 × 0.04 = 2.00; +15)
dave,1000,1000,fixed
dave,1000,1000,payg       -> dave: $8.20     (r=1/2 → fee 7.50, allowance 20,000; fixed session
                                              2,000 tokens inside allowance; payg 10×.03+10×.04=0.70)
```
Input order for the file above yields output sorted: alice, bob, carol, dave.

## Edge cases hidden tests are known to target
- users with $0.00 must still be printed
- `x.xx5` half-up rounding of the prorated fee (e.g. r = 1/3 → 5.00; r = 1/6 → 2.50; r = 1/7 → 2.142857… → 2.14)
- allowance boundary: exactly 40,000 billable tokens → overage 0
- overage split between input and output when the allowance runs out mid-session
- remainders < 100 never accumulate across sessions
- very large token counts (10^9) — use integers, never float accumulation
- `user_id` sorting is plain string order (`B` < `a`, `user10` < `user2`)

## Variants seen in the wild
- **Separate allowances**: 40,000 input + 20,000 output (1point3acres entry f8e3ed43). Swap
  `ALLOWANCE` for two counters; everything else identical.
- Output as a returned `list[str]` from `calculate_monthly_billing(sessions)` instead of stdout.

## What this tests
skills: S02 parsing · S04 grouping · S06 integer money + rounding · S07 tiered/metered math ·
S08 deterministic sort · S09 exact formatting · S19 incremental design

## Sources
- https://www.1point3acres.com/interview/problems/59a39c1c (Chat Billing Calculation — Monthly Billing by Token Usage and Plan Switching)
- https://www.1point3acres.com/interview/problems/f8e3ed43 (Chat Billing Calculation, separate allowances)
- https://www.1point3acres.com/interview/company/stripe/chat-billing-oa (OA · Medium · last asked 2026-04-17)
- 1024bbs 10992 「Stripe 吐血面经总结」(mention)

## Clarifications (from adversarial review, 2026-08-26)
- When the prorated allowance is not a multiple of 100 (e.g. r = 1/3 → 13,333 tokens), the leftover over-allowance tokens are floored to 100-blocks again, so 67 excess tokens bill 0 blocks. This double floor is intentional and matches the per-session block rule.
