# ps06 Receivables registration — report

## Summary
A CSV-aggregation question dressed as a real Stripe Brazil compliance workflow (receivables
registered with the central bank). Part 1 is pure grouping + integer-cents summation; Part 2 is
where the interview actually differentiates candidates — malformed-row handling that skips and
*counts* (not silently drops) bad rows, signed amounts (refunds), and a date-normalization rule
(weekend payout dates roll to the next business day) that must run *before* the aggregation key is
built, not after — a common off-by-ordering bug.

## Sources & confidence
medium — csoahelp.com's 2024-10-04 transcript gives the scenario (Brazil receivables), the
function name (`register_receivables`), the exact CSV field list
(`customer_id,merchant_id,payout_date,card_type,amount`), and the aggregation key
(`merchant_id + card_type + payout_date`), plus the 4-stage interview structure (clarify → solution
walkthrough → follow-ups → behavioral). It does **not** publish exact output formatting or Part 2's
business rules — the weekend-roll rule, the specific malformed-row categories, and the `SKIPPED n`
trailer are this report's reconstruction, written to be a plausible, commonly-asked follow-up
direction rather than a verbatim transcript. Flagged explicitly in problem.md's "Variants" section.

## Approach by part
1. **Part 1**: parse `customer_id,merchant_id,payout_date,card_type,amount`, convert `amount` to
   integer cents (`_amount_to_cents`), accumulate into a `defaultdict(int)` keyed by
   `(merchant_id, card_type, payout_date)`, render sorted by `(merchant_id, payout_date,
   card_type)` — note the *output* column order (`merchant_id,card_type,payout_date,total`)
   differs from the *sort key* order, which is exactly the kind of detail hidden tests target.
2. **Part 2**: same aggregation, plus a validation gate per row (field count == 5, amount matches
   `-?\d+\.\d{2}`, date matches `YYYY-MM-DD` **and** parses as a real calendar date via
   `datetime.strptime`) that increments a skip counter on any failure; only rows that pass get
   their `payout_date` rolled forward (Saturday +2, Sunday +1) *before* being used as the group
   key, so a Saturday and a Sunday row for the same merchant/card_type correctly merge into one
   Monday group.

## Pitfalls hidden tests target
- output column order vs. sort key order are different tuples — easy to conflate
- `2026-02-30` (impossible day) vs `2026/08/03` (wrong separator) — both invalid, but for
  different reasons; a solution that only regex-checks the shape misses the calendar-validity case
- `150.5` / `150` / empty string amounts — one-decimal, no-decimal, and empty are all invalid,
  distinct from a merely negative-but-correctly-formatted `-15.50`
- rolling the date *before* keying, not after — rolling after grouping would produce two separate
  groups (pre-roll Saturday group and the original Monday group) instead of one merged group
  (`test_saturday_and_sunday_both_roll_to_same_monday` targets this directly)
  a group total that nets to exactly `0.00` must still be printed as a real registration line
- `SKIPPED 0` must still be the last line when nothing was skipped (no "print SKIPPED only when
  n > 0" shortcut)
- a weekend roll that crosses a month/year boundary (`2026-01-31` Saturday -> `2026-02-02` Monday)

## Complexity & measured cost
O(n) parse + aggregate, O(g log g) sort where `g` = number of distinct groups (g << n for any
realistic batch). Measured: 100,000 rows (with malformed rows sprinkled in at a 1-in-5000 rate)
end-to-end via stdin -> stdout in well under 2 s, comfortably inside the 256 MB budget — see
`test_perf_100k_rows`.

## Test inventory
21 tests — part1: 6 (incl. 1 io) . part2: 12 (incl. 1 io, 1 perf); edge 11 . fmt 1 . io 3 . perf 1.

## Skills exercised
S02 parsing/malformed-row handling . S04 grouping/aggregation . S06 integer money (BRL cents,
never float-accumulate) . S08 deterministic multi-key sort . S09 exact formatting (no currency
symbol, signed totals) . S12 date handling (calendar validity + business-day rolling) . S18
validation and error paths (skip + count, never crash on bad input)

## 电面话术：边写边说什么
1. **澄清阶段** (面试第①段)：主动问三件事——`amount` 到底是分还是两位小数字符串（本题定死两位小数，
   但真实面试里这是第一个该问的问题）；输出要不要带货币符号（登记到央行的内部文件通常不带）；聚合
   总额如果是负数（退款超过消费）该怎么办，是报错还是照实输出。不要默认，直接问。
2. **写 Part 1 时**：边写边强调"金额我用整数分累加，绝不用 float"，并且提前说明输出列顺序
   (`merchant_id,card_type,payout_date,total`) 和排序 key 顺序
   (`merchant_id,payout_date,card_type`) 是两回事——这是本题最容易在口头描述里被自己绕晕的地方，主动
   讲清楚等于提前排掉一个追问。
3. **过渡到 Part 2 时** (面试第②段思路讨论)：先列出"哪些行是坏行"的分类（字段数、金额格式、日期格式/
   日期合法性），再决定"skip + count"而不是"skip 但不计数"或"直接抛异常"——说明这个选择是因为央行提交
   场景下，静默丢弃数据是不可接受的，必须有审计痕迹（`SKIPPED n`）。
4. **写周末顺延规则时**：显式说"我要在这行数据进入聚合字典**之前**做日期归一化，不然周六和周一的同一
   商户流水会被分成两组"——这是本题唯一真正容易挖坑的地方，主动指出比等面试官问出来更加分。
5. **追问阶段** (面试第③段)：参考 problem.md 末尾"面试官会怎么追问"列表——幂等重复提交、10^7 行流式处理、
   多币种、时区/夏令时、节假日日历接入、更正/冲正记录设计，任选 2-3 条主动展开讨论，展示系统设计视角
   而不仅仅是把题做对。
6. **收尾**：跑一遍 worked examples 手算核对，再补一句"如果给我历史提交批次的哈希/幂等键，我可以把
   `SKIPPED` 之外再加一个 `DUPLICATE` 计数，防止重试导致重复登记"——呼应第④段行为面试常问的"你怎么考虑
   生产环境的鲁棒性"。

## Open points
- csoahelp 的转录没有公开 Part 2 的具体业务规则（本 REPORT 已在 problem.md 的 Variants 一节明确标注：
  周末顺延、坏行分类、`SKIPPED n` 尾行都是本套件按 Stripe 电面惯用"happy path -> robustness/business
  rules"模板做的合理重建，不是逐字转录）；如果后续拿到更精确的原题转录（尤其是官方 Part 2 措辞），应
  回来核对本文件的规则定义是否需要调整。
- 未确认真实面试是否要求处理带引号/嵌入逗号的 CSV 字段（本题假设简单 split(",") 足够，字段本身不含
  逗号），如果拿到反例应补充 RFC4180 引号解析。

## Review（Fable 5.1，2026-09-01）
**改了什么**
- `solution.py` 重构为同一条流水线 `_data_lines → 解析成 Row → _aggregate → _render`：Part 1 用
  `_parse_row_trusted`，Part 2 用 `_parse_row_checked`（返回 `None` 即坏行）+ `_roll_weekend(row)`，两个
  part 共用 `_aggregate/_render`，不再各自维护一份聚合循环（原来 Part 2 是 Part 1 的复制粘贴版）。
- 规则集中为常量：`FIELD_COUNT`、`AMOUNT_RE`、`DATE_RE`、`ROLL_FORWARD_DAYS = {SAT: 2, SUN: 1}`；`Row`
  用 `NamedTuple` 命名字段；日期合法性改用 `date.fromisoformat`（正则先定形状）；`AMOUNT_RE.match` →
  `fullmatch`；`main` 用 `PARTS` 表分发（starter_template/starter 同步）。
- problem.md 补两句定死：字段两侧空格容忍（实现一直如此，题面没写）；Part 1 不做周末顺延。
- 测试 +2：Part 1 周六日期不顺延（区分两个 part）；格式化 `1234567.89` 无千分位、`-0.05` 保留前导 0。
  21 → 23。lint：black 110 + flake8 通过（此前 4 个文件 black 未格式化）。

**为什么**：checklist S 项"后 part 复用前 part / 规则用表不用散 if / 解析-逻辑-格式化分离"；原实现
Part 2 里"归一化在入 key 之前"这条关键规则埋在 12 行循环中间，现在是 `rows.append(_roll_weekend(row))`
一行加注释，面试官 60 秒能看到。

**遗留**：Part 2 规则仍是重建（见 Open points）；带引号/嵌入逗号的 CSV 未处理（题面明确假设简单 split）。
