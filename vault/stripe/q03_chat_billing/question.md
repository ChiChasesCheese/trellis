# q03 · Chat Billing — monthly billing by token usage and plan switching

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

## 关联知识点

- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]]
- [[s04-group-then-aggregate|S04 分组聚合，规则每组一次而不是每行一次]]
- [[s06-money-integer-cents|S06 金额用整数最小单位；显式舍入；两位小数格式]]
- [[s07-tiered-metered-proration|S07 阶梯 / 计量 / 按比例分摊]]
- [[s08-deterministic-sort-tiebreak|S08 确定性排序与完整 tie-break]]
- [[s09-byte-exact-output-format|S09 字节级精确的输出格式]]
- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]]
