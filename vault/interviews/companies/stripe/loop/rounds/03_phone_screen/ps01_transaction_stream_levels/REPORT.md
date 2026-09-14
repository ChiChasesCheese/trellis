# ps01 Transaction Stream Levels — report

## Summary
Four unlock-next-part levels over the same `user_id,amount,timestamp` stream: totals -> 60s
sliding-window threshold flag -> top-K at a point in time -> `[small,large,small]` pattern
detection. This is Stripe's real-time velocity/fraud-monitoring shape ("has this user spent too
much too fast?") reduced to interview size. The whole difficulty is nailing down *one* window
convention (closed interval) and reusing it consistently across Parts 2-4, plus getting the
tie-break rules (timestamp ties -> input order; sort ties -> user_id) explicit instead of
implicit.

## Sources & confidence
medium — single primary source (learncswithus.com, 2025-10-25) with a detailed four-level
breakdown, but only Levels 1 and 3 include concrete numeric examples; Levels 2 and 4 are
prose-only ("flag users who cross T within any 60s window", "detect [small,large,small] with a
state machine") with no numbers. The Level 3 example (`t=90, K=2 -> [2,1]`) was load-bearing: it
is the only piece of ground truth that pins the window to a **closed** interval `[t-60,t]`
rather than a half-open one — a half-open window on the same input produces `[1,2]`, the wrong
order. Levels 2 and 4's worked examples in problem.md are reconstructed by me to be internally
consistent with that same closed-interval rule, not sourced numbers.

## Approach by part
1. **Part 1**: plain `dict` accumulation, order-independent, `O(n)`.
2. **Part 2**: per-user deque of `(timestamp, amount)`; on each event (processed in
   timestamp-then-input-order), evict everything older than `ts - W`, then check the running sum
   against `T`. First crossing wins and is recorded; amortized `O(n)` overall (each transaction
   enters/leaves its deque once).
3. **Part 3**: single pass filtering to the closed window `[t-60, t]`, `dict` sum per candidate
   user, then `sorted(items, key=lambda kv: (-sum, user_id))[:K]`. `O(n + m log m)`. Documented
   the heap alternative (`O(n log K)`) as a stated trade-off rather than implementing it — not
   worth the complexity at `n<=10^5`.
4. **Part 4**: sort each user's stream once (shared `_by_user_sorted` helper, reused by Parts 2
   and 4), classify into `small`/`large` by `amount < S`, then scan every window of 3 consecutive
   (post-sort) transactions — deliberately index-based rather than a literal 3-state machine,
   though the two are equivalent; documented the state-machine framing as the "expected" mental
   model from the source, since an interviewer may ask for it explicitly.

## Pitfalls hidden tests target
- Window boundary: exactly `W` seconds old is **inside** the window (closed interval) — tested
  both directions (`W` in, `W+1` out) for Parts 2 and 3 independently, since they're separate
  code paths that happen to share the same convention.
- Part 2's "first crossing" semantics vs. "ever crossing" vs. "max window sum ever seen" — three
  different, easily-conflated definitions; the reference solution + tests commit to "first
  crossing, report that window's sum."
- Part 3: users with zero activity in the window are never candidates (no zero-padding); ties in
  `sum` broken by `user_id` ascending, not left as sort-implementation-defined; output stays in
  **ranked** order, not re-sorted by `user_id` (easy bug: reusing Part 1's user_id-sort habit).
- Part 4: overlapping matches both count (`s,l,s,l,s` -> 2 matches, not 1); `amount == S` is
  `large`, not `small` (strict `<` for small only); users with `< 3` transactions produce zero
  matches, not an error.
- Out-of-order input lines (file order != timestamp order) must not change any output.

## Complexity & measured cost
All four parts are `O(n)` to `O(n + m log m)` (`m` = distinct users). Perf test: 100k lines /
~3000 users through Part 2 (deque-heavy path) ran in ~0.09s during ad-hoc development timing,
well under the 2s / 256MB budget (measured live via the `run_script` fixture at test time).

## Test inventory
27 tests — part1: 8 · part2: 6 · part3: 7 · part4: 6; edge: 10 · fmt: 3 · io: 3 · perf: 1.

## Skills exercised
S02 parsing (params-line vs data-line disambiguation by comma-count) · S03 out-of-order stream
processing · S04 per-user grouping · S05 sliding window (deque, closed-interval boundary) · S08
deterministic sort/tie-break · S09 exact formatting · S19 incremental design (state/helpers
shared across levels 2 and 4)

## 电面话术：边写边说什么
1. **读题时**：先大声确认输入协议——"PART 行后面,如果紧跟的一行没有逗号但有等号,我把它当参数行
   读;否则直接当第一条交易处理" ——把这个隐含契约说出来,而不是默默假设。
2. **写 Part 1 前**：一句话说明分组策略——"用 dict 按 user_id 累加,金额只用 int,不引入浮点"。
3. **写 Part 2 前**：明确追问或声明窗口边界——"我按闭区间 `[ts-W, ts]` 处理,也就是恰好 W 秒前的
   交易仍然算在窗口内;如果你们的定义是开区间我现在就能改一行" ——主动暴露这个歧义点,而不是等面试官发现。
4. **写 Part 3 前**：说明为什么用 `dict + sorted` 而不是堆——"当前数据量下 `sorted` 足够快,如果
   面试官后续问'如果 K 远小于用户数怎么优化',我会换成 size-K 的最小堆"。
5. **写 Part 4 前**：先讲清楚"重叠匹配"的语义——"我把每一个起点都独立检查,`s,l,s,l,s` 会报两次
   匹配,而不是贪心地跳过已经用过的交易"——这是本题最容易被面试官抓到的隐藏歧义。
6. **测试阶段**：至少现场跑一遍"输入乱序"的用例,证明代码对"可能乱序输入"这条题面要求是真的处理了,
   而不是恰好数据本来就有序。
7. **收尾**：主动提一句"如果这是无限流,Part 1/Part 2 已经很接近流式处理了,只是被'先读完整个
   stdin'这个 I/O 边界挡住"——展示对生产场景的思考,呼应 Stripe 真实的实时风控场景。

## Review（Fable 5.1，2026-09-01）
**改了什么**
- `test_ps01.py`：`test_window_boundary_closed_inclusive` 在 part2 与 part3 各定义一次（flake8 F811），
  后者覆盖前者，Part 2 的窗口边界测试实际上从未运行。重命名为 `test_p2_…` / `test_p3_…`，两个都跑且通过。
  新增 1 个 `part4 io` 测试（参数行 + 逗号连接格式走完整脚本）。现在 29 tests：part1 8 · part2 7 ·
  part3 7 · part4 7；edge 11 · fmt 3 · io 4 · perf 1。`IMPL=starter` 21 failed / 8 passed。
- `solution.py` 重构为范本（公共 API 不变）：`Tx` NamedTuple 取代 4 元组；`_split_params` 把"去空行 +
  弹参数行"收拢到一处（原来 4 个 part 各重复一遍 strip）；规则层拆成 `_totals` / `_first_crossing` /
  `_pattern_starts`，每个只面对一个用户的排好序 list；Part 3 复用 Part 1 的 `_totals`；Part 4 的模式改为
  常量 `PATTERN`（对应追问 5"模式可配置"）；`DEFAULT_W` 常量。每个 `partN` ≤ 8 行：解析 → 规则 → 格式化。
- black 格式化（docstring 后空行、注释对齐），`loop/lint.sh` 通过。
**为什么**：F811 是真 bug（测试被吞）；其余是 S 项可读性/复用。题面语义、worked examples 逐字输出均未变
（4 个样例已用 `python3 solution.py` 逐个核对）。
**遗留**：无。堆版 top-K 仍只在 problem.md 作为追问讨论，不实现。
