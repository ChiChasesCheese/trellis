# ps06 · Receivables registration

**Type:** phone screen (technical, 4-段面试流程) · **Stage:** technical screen, 45 min · **Last asked:** 2024-10-04 (csoahelp.com, 代面服务站点转录)
**Frequency:** 1 direct transcript (csoahelp) + cross-referenced by 一亩三分地/programhelp as appearing in both Technical Screen and Integration contexts (轮次归属存在混淆，见 `loop/raw/cn_forums.md` 第 64/103 行) · **Confidence:** medium — I/O field names (`customer_id,merchant_id,payout_date,card_type,amount`) and the aggregation key (`merchant_id + card_type + payout_date`) are directly from the source; exact formatting/edge rules below are this report's reconstruction to match Stripe's usual "happy path → robustness/business rules" phone-screen shape

## Context
Stripe processes card transactions for merchants in Brazil. Brazilian regulation requires
payment processors to register upcoming payouts to merchants ("recebíveis" / receivables) with
the central bank ahead of the actual payout date, aggregated by merchant, card network, and the
date money will move. You're given a batch of individual transaction records and must produce the
aggregated registration file the central bank submission expects.

## Input (stdin, for `main()`)
First line is `PART 1` or `PART 2`. The next line is the CSV header
`customer_id,merchant_id,payout_date,card_type,amount`. Remaining lines are data rows, one
transaction per line, same field order. `amount` is a BRL value given as a **two-decimal string**
(e.g. `150.00`, `-15.50` for a refund) — not integer cents; you convert internally. `payout_date`
is `YYYY-MM-DD`. Blank lines are ignored; spaces around commas are tolerated (fields are
stripped). Part 1 never rolls dates — a Saturday `payout_date` is a Saturday group.

## Output
One line per `(merchant_id, card_type, payout_date)` group:
`merchant_id,card_type,payout_date,total` — `total` is a two-decimal string (may be negative,
e.g. `-30.00`), **no `$`/`R$` sign** (this is an internal registration file, not a customer-facing
statement). Sorted by **`merchant_id`, then `payout_date`, then `card_type`** (all plain string
order). Part 2 additionally appends one trailing line `SKIPPED n` (`n` = number of rows skipped as
malformed; `n` is always printed, even `SKIPPED 0`).

## Rules

### Part 1 — `register_receivables` happy path
Input rows are well-formed (assume valid CSV, valid date, valid two-decimal amount — no
validation needed). Group by `(merchant_id, card_type, payout_date)`, sum `amount` in **integer
cents** internally (never accumulate floats), and emit the aggregated lines as described above.
Duplicate rows for the same key (repeat customer, or the same customer transacting twice) merge
into the same group — summed, not overwritten.

### Part 2 — robustness and business rules
The same aggregation, but the input is no longer clean:
- **Skip and count** any row that is malformed: wrong number of comma-separated fields (≠ 5),
  `amount` that doesn't match `-?digits.dd` (exactly two decimal digits — `150.5`, `150`,
  `abc`, empty are all invalid), or `payout_date` that isn't a real calendar date in `YYYY-MM-DD`
  form (`2026-13-01`, `2026-02-30`, `26-08-03` are all invalid). A skipped row contributes
  nothing to any group's total.
- **Negative amounts are allowed** (refunds/chargebacks) and can make a group's total negative —
  do not clamp at zero.
- **Duplicate rows for the same key merge** (same as Part 1).
- **Weekend payout dates roll forward to the following Monday** — Saturday → +2 days, Sunday →
  +1 day — applied to each row's `payout_date` **before** it is used as part of the aggregation
  key, so a Saturday-dated and a Monday-dated row for the same merchant/card_type land in the
  *same* group once rolled.
- Append `SKIPPED n` as the last output line.

## Worked examples
```
PART 1
customer_id,merchant_id,payout_date,card_type,amount
c1,m1,2026-08-03,visa,150.00
c2,m1,2026-08-03,visa,50.00
c3,m1,2026-08-03,mastercard,20.00
c4,m2,2026-08-04,visa,100.00
->
m1,mastercard,2026-08-03,20.00
m1,visa,2026-08-03,200.00
m2,visa,2026-08-04,100.00
```
```
PART 2
customer_id,merchant_id,payout_date,card_type,amount
c1,m1,2026-08-08,visa,150.00
c2,m1,2026-08-10,visa,50.00
c3,m1,2026-08-09,visa,-30.00
c4,m2,2026-08-04,visa,BAD
c5,m2,2026-08-04
c6,m3,2026-13-01,visa,10.00
->
m1,visa,2026-08-10,170.00
SKIPPED 3
```
(2026-08-08 is a Saturday → rolls to 2026-08-10 Monday; 2026-08-09 is a Sunday → also rolls to
2026-08-10; all three land in one group: `150 + 50 - 30 = 170.00`. Row 4 has a malformed amount,
row 5 has only 4 fields, row 6 has month `13` — all three skipped, `SKIPPED 3`.)

## Edge cases
- group total that nets to exactly `0.00` (still printed, a merchant/card/date with all refunds
  offsetting charges is still a real registration line)
- group total that goes negative overall (refunds exceed charges for that key)
- `payout_date` exactly on a Monday–Friday — no rolling
- Saturday **and** Sunday rows for the same merchant/card_type both rolling into the same Monday
  group
- a roll that crosses a month or year boundary (e.g. Saturday Jan 31 → Monday Feb 2)
- malformed row: wrong field count (too few or too many commas)
- malformed row: amount with one decimal digit, no decimal point, or non-numeric
- malformed row: impossible calendar date (`2026-02-30`) vs. wrong format (`2026/08/03`)
- `SKIPPED 0` still printed when nothing was skipped
- multiple merchants, multiple card types, ties in the sort key broken by the next key in order
- large batch (10^5 rows) with a bounded number of distinct groups — aggregation must stay
  near-linear, not re-scan per row

## Variants seen in the wild
- csoahelp's summary doesn't publish the weekend-rolling or bad-row rules explicitly — it
  describes the interview as **4 段**: ① clarifying questions ② solution walkthrough ③ follow-ups
  ④ behavioral. The weekend-roll rule here is written to be a plausible, commonly-asked follow-up
  direction (see follow-ups list) rather than a transcribed Part 2 — treat it as the "canonical"
  version of this drill's Part 2, and treat the follow-ups list as the actual reported shape of
  the interview's later stages.
- 中文圈 (`cn_forums.md` 第 103 行) 部分把同一题归类在 Integration 轮而非纯 Technical Screen —— 说明
  该题目在不同候选人/不同流程阶段都出现过，轮次归属本身存在混淆，练习时按 Technical Screen 的时间盒
  （45 min）来演练即可。

## What this tests
skills: S02 parsing/malformed-row handling · S04 grouping/aggregation · S06 integer money
(never float-accumulate BRL cents) · S08 deterministic multi-key sort · S09 exact formatting
(no currency symbol, signed totals) · S12 date handling (calendar validity + business-day
rolling) · S18 validation and error paths (skip + count, don't crash)

## Sources
- https://csoahelp.com/2024/10/04/stripe-api-receivables-registration-interview-.../ (csoahelp.com,
  "Stripe API Receivables Registration Interview", 2024-10-04 — Brazil receivables scenario,
  `register_receivables` function name, CSV field list, aggregation key, 4-stage interview
  structure)
- `loop/raw/cn_forums.md` 第 64 行（原文摘录）、第 103 行（"Onsite — Coding" 交叉引用，轮次归属存疑说明）

## 面试官会怎么追问
1. 如果同一批数据里同一个 `(merchant_id, card_type, payout_date)` 出现极多笔小额交易（比如某商户
   一天几十万笔），你现在的实现要扫描/存多少内存？能不能流式处理，边读边聚合不用把所有行放进内存？
   （引导到 10^5～10^7 行的流式设计：只需要保留聚合字典，不需要保留原始行）
2. 这批注册数据如果需要**重复提交**（比如任务重试、上游重发同一批文件）,你怎么保证登记到央行系统
   是**幂等**的，不会重复计入？（引导到"给每批文件一个幂等键 / 用 transaction id 去重而不是天真地
   对同一份文件重新求和"）
3. 如果 `amount` 字段本来就是巴西雷亚尔的整数分（而不是两位小数字符串），你的解析逻辑要改哪里？
   两种格式同时存在的历史数据要怎么兼容？
4. 如果交易涉及多币种（不只是 BRL），你会怎么改聚合 key 和输出格式？金额还能直接相加吗？
5. `payout_date` 目前假设和请求处理时区一致；如果客户端传的是 UTC 时间戳而央行要求巴西本地时区
   (America/Sao_Paulo, 有夏令时历史) 的日期，你的"周末顺延"规则会怎么受影响？
6. 现在的"周末顺延到下周一"没有考虑巴西法定节假日；如果要接入节假日日历，你的设计需要新增什么
   依赖/接口，且不能让这个查询变成每行一次的外部调用？
7. 如果一笔交易在提交后被发现金额登记错了，需要更正（不是简单退款），你会怎么设计"更正/冲正"记录
   而不破坏已经提交给央行的历史聚合？
