# ps02 Shipping Cost Pricing — report

## Summary
Three unlock-next-part levels over a rate table + order list: flat per-unit price -> quantity
tiers (single matched-band rate) -> mixed billing where each tier band is explicitly typed
`incremental` (graduated, tax-bracket style) or `fixed` (whole quantity at the matched band's
rate). This mirrors Stripe Billing's own `graduated` vs `tiered`(volume) pricing distinction, and
two independent sources (CN + EN) confirm the identical three-step shape and the exact
`incremental`/`fixed` terminology for Part 3.

## Sources & confidence
high — learncswithus.com (2025-10-20, primary, detailed level-by-level write-up including the
grading note "no automated test cases, logic + structure graded, boundaries not enforced") cross
-confirmed by 1point3acres.com/interview/post/7100079's TOC (`Simple Fixed Price -> Volume
Discounts -> Mixed Pricing Types`, word-for-word the same progression) and independently by
`en_forums.md` line 151 (linkjob.ai P9, English side, naming `incremental`/`fixed-pricing`
explicitly for Part 3). Neither source gives concrete numeric examples or nails down interval
open/closed-ness or an exact error-message format — those are reconstructed decisions, called
out explicitly in problem.md's Rules section (closed interval `[min_qty,max_qty]`; three pinned
error strings) rather than presented as sourced facts.

## Approach by part
1. **Part 1**: `dict[(country,product)] -> unit_cost_cents`, `O(1)` lookup per order.
2. **Part 2**: `dict[(country,product)] -> [bands]`, bands sorted by `min_qty` once at parse
   time (rate table order is explicitly untrusted — the worked example lists the top band
   first on purpose, and a test pins this). Per-order: linear scan to find the containing band
   (bands-per-product is small in practice; documented `bisect` as a follow-up, not implemented
   up front — avoids over-engineering a ~3-band-per-product table).
3. **Part 3**: reuses Part 2's exact band-matching lookup unchanged; only the matched band's
   `type` branches the pricing: `fixed` calls the identical `qty * cost` as Part 2, `incremental`
   walks every band from `min_qty=1` up through the matched band, summing each band's own rate
   for the units inside it, with an explicit contiguity check (`incremental gap` error) that
   only fires when an order's quantity actually needs to walk through the hole — verified with a
   dedicated worked example showing the *same* rate table producing both a clean price (qty=5,
   never reaches the gap) and an error (qty=20, must cross it).

## Pitfalls hidden tests target
- Rate table rows out of order in the file (must sort by `min_qty` before lookup, not assume
  file order).
- Band boundaries: `min_qty` and `max_qty` both inclusive, tested on both edges of the *same*
  band (`qty=10` and `qty=11` on a `1-10`/`11-20` split must give different, correct answers).
- Three distinct, verbatim-matched error strings — `unknown product`, `no tier`, `incremental
  gap` — deliberately different failure modes that must not be conflated (e.g. a gap in the
  matched-band lookup itself is `no tier`, not `incremental gap`; the latter only fires once the
  matched band is found but the walk *to* it hits a hole).
- `fixed` vs `incremental` on the identical quantity must diverge ($67.50 vs $72.50 for qty=15
  on the same-shaped ladder) — the one test most likely to catch a candidate who implements
  `incremental` but silently ignores the `type` field per band (i.e., always sums cumulatively).
- Money parsing: `"5"`, `"5.5"`, `"5.50"` must all mean the same 5.50 — a common bug is treating
  a bare `.5` as 5 cents instead of 50 cents (right-padding, not left-padding, the fraction).
- `quantity = 0` must price at `$0.00` without touching the tier lookup at all, but still
  requires the product to exist (a zero-quantity order for an unknown product still errors).
- Output is **input order**, not sorted by `order_id` (unlike ps01/q03's per-user grouping) —
  each order is an independent query, not an aggregation key.

## Complexity & measured cost
`O(n)` for Part 1; `O(n * b)` for Parts 2-3 where `b` = bands for that order's `(country,
product)` (small, bounded by the rate table size, ~200 rows total in the stated scale).
Perf test: 100k orders across a 15-row rate table (5 countries x 3 products) through Part 1 ran
in ~0.07s during ad-hoc development timing, well under the 2s / 256MB budget (measured live via
the `run_script` fixture at test time).

## Test inventory
21 tests — part1: 8 · part2: 6 · part3: 7; edge: 9 · fmt: 1 · io: 3 · perf: 1.

## Skills exercised
S02 parsing (fixed vs variable-width CSV rows, `RATES`/`ORDERS` section markers) · S06 integer
money (cents, decimal-string parsing, never floats) · S07 tiered/metered pricing math
(closed-interval band lookup, graduated vs flat billing) · S09 exact formatting (money + verbatim
error strings) · S10 defined error handling (three distinct, pinned error message formats) · S19
incremental design (Part 2's lookup reused unmodified as Part 3's `fixed` branch)

## 电面话术：边写边说什么
1. **读题时**：先复述协议再动手——"RATES 到 ORDERS 之间是费率行,ORDERS 之后每行是一个独立订单,
   输出按订单出现的顺序,不做分组/排序"——避免默认套用 ps01/q03 那种"按 key 排序输出"的肌肉记忆。
2. **写 Part 1 前**：说明货币解析策略——"金额一律解析成整数分,`5`、`5.5`、`5.50` 都当 5.50 处理,
   全程不出现浮点数"。
3. **写 Part 2 前**：主动提出区间开闭问题——"题面没直接给,我按闭区间 `[min_qty,max_qty]` 实现,
   也就是边界值精确落在某一档就算那一档;如果你们的定义不同,这里只需要改一个比较符号"。
4. **写 Part 2 时**：提醒自己费率表可能乱序——"我先把每个 (country,product) 的档位按 min_qty
   排序,再做查找,不假设输入文件本身有序"——这是原始面经里明确提到的"最容易踩的坑"。
5. **写 Part 3 前**：讲清楚"哪个 type 说了算"——"我只看命中的那一档的 type,而不是要求整条费率
   链条的 type 都一致;如果面试官问'如果不同档 type 不一样怎么办',这个设计天然就是良定义的"。
6. **写 incremental 分支时**：现场画一下"缺口"场景——"如果链条从 1 开始不连续,只有订单数量真的
   需要穿过那个缺口时才报错;数量在缺口前面就命中的订单不受影响"——用 worked example 里 qty=5 vs
   qty=20 的对比现场证明。
7. **收尾**：主动提"如果一个订单要买多个 product,现在的单行 order protocol 怎么扩展"——展示对
   协议可扩展性的思考,呼应面经里"没有自动测例,面试官看代码结构"的评分导向。

## Review（Fable 5.1，2026-09-01）
**改了什么**
- `solution.py` 重构为范本（`part1/2/3` 与 `main` 签名不变）：`Band` 由 4 元组改为 NamedTuple 并带 `contains(qty)`
  （闭区间只写一次）；定价函数改为"返回整数分，算不出就 `raise PricingError`"，取代原来贯穿各层的 `(cost, err)`
  tuple；三种错误文案只在 `_price_orders` 的 `try/except` 一处变成 `ERROR ...` 字符串。`_price_tiered` 30 行拆为
  "找档位 + fixed"与 `_price_incremental`；`_split_sections` 的 `assert` 改为 `ValueError`；`parse_money_to_cents`
  去掉题面未定义的负数分支并用 `partition` 简化；`TIER_TYPES` 常量。
- `test_ps02.py` 新增 2 个：`part1 edge` 零数量 + 未知商品仍报错（题面明文，原未测）；`part3 edge` incremental 走到
  `inf` 顶档（`$215.00`，原来 `inf` 分支只在报错路径被触及）。现在 23 tests：part1 9 · part2 6 · part3 8；
  edge 11 · fmt 1 · io 3 · perf 1。`IMPL=starter` 22 failed / 1 passed。
- black 格式化（4 文件），`loop/lint.sh` 通过。
**为什么**：无 F 级 bug；全部是 S 级可读性/复用/错误处理约定。4 组 worked examples 已用 `python3 solution.py` 逐字核对。
**遗留**：无。`bisect` 版档位查找仍作为追问讨论不实现。
