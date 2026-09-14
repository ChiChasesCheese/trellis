# ps13 · Incident Monitor

**Type:** phone screen（technical）· **Stage:** technical screen, ~45 min ·
**Last asked:** 2026-01-15（候选人原始报告日期，见下）
**Frequency:** 1 名候选人第一人称报告（语义高度吻合但标题不同的疑似同源题）· **Confidence:** low-medium
（见下方警示块与 Sources）

> ⚠️ **部分重建题**：Part 1 的规则来自一份真实候选人报告（PracHub「Detect Trigger and Resolve Events」，
> 2026-01-15，第一人称、非 AI 生成），但**该报告的标题与 catalog 记录的「Incident Monitor」不同，
> 无法确认是同一道题**；候选人本人也说"二三部分有点忘了"。因此 **Part 2 及以后的规则、
> 全部的输入输出格式、part 划分，都是本仓库自拟的**。
> 练它是为了覆盖 S04 · S05 · S10 · S12 · S16，**不要把这里的输出格式当成真题格式**去背。

## Context
Stripe's error-rate monitoring watches transaction logs for each `(merchant_id, status_code)`
pair independently. When a pair's error count over a trailing time window climbs to a threshold,
an on-call alert fires (`TRIGGER`); when the same pair's error count later falls back below that
threshold, the alert clears (`RESOLVE`). This problem builds that monitor up from a single global
rule (Part 1 — the part with real candidate-report provenance) through out-of-order log arrival,
per-merchant rule overrides, and a two-severity-level escalation ladder (Parts 2-4, this suite's
own design).

## Input (stdin, for `main()`)
```
PART n
<params line(s) -- see each part below>
timestamp,merchant_id,status_code,count
timestamp,merchant_id,status_code,count
...
```
* `timestamp` and `count` are non-negative integers (`0 <= timestamp <= 10^9`,
  `1 <= count <= 10^9`). `merchant_id` and `status_code` are opaque strings/tokens — never
  reformatted, just grouped on. Fields are comma-separated, exactly 4 per log line; surrounding
  whitespace is stripped.
* `0 <= number of log lines <= 200000`.
* Blank lines are ignored.

## Rules

### Part 1 — single global rule, sorted input (real candidate-report provenance)
Params line: `WINDOW=<int> THRESHOLD=<int>` (`1 <= WINDOW <= 10^9`, `1 <= THRESHOLD <= 10^12`).
Logs for this part are **already sorted by non-decreasing timestamp** (equal timestamps: process
in the order they appear in the input).

For each log record at time `t`, its `(merchant_id, status_code)` pair's **rolling count** is the
sum of `count` from every record for that same pair whose `timestamp` falls in the **inclusive
range `[t - WINDOW + 1, t]`**. Process records one at a time, in order; after folding a record
into its pair's rolling count, check that pair's state:
* Emit `TRIGGER` the moment a pair's rolling count goes from **strictly less than** `THRESHOLD` to
  **greater than or equal to** `THRESHOLD`.
* Emit `RESOLVE` the moment a pair's rolling count goes from **greater than or equal to**
  `THRESHOLD` back to **strictly less than** `THRESHOLD`.
* Never emit two consecutive events of the same type for the same pair (a state only changes once
  per crossing — this falls out naturally from tracking "am I currently above or below
  `THRESHOLD`" per pair, rather than re-checking the raw sum against the threshold independently
  at every step).

Output one line per emitted event, `timestamp,merchant_id,status_code,event_type`
(`event_type` is `TRIGGER` or `RESOLVE`), in the chronological order the events were generated
(which — because input is sorted and events are emitted while processing in order — is simply
processing order).

### Part 2 — logs may arrive out of order
Same params (`WINDOW=<int> THRESHOLD=<int>`) and same rule as Part 1, but log lines are **not**
guaranteed sorted by timestamp. Sort by `(timestamp, original input position)` before applying
Part 1's rule (stable tie-break: two logs at the same timestamp are processed in the order they
appeared in the input, not re-sorted by `merchant_id` or anything else). Output events remain in
chronological order (post-sort processing order).

### Part 3 — per-merchant rule overrides
Params line: `DEFAULT_WINDOW=<int> DEFAULT_THRESHOLD=<int> RULES=<k>`, followed immediately by
exactly `k` override-rule lines `merchant_id,window,threshold` (`k` may be `0`, in which case there
are zero override lines and every merchant uses the default rule), followed by the log lines
(logs for this part are sorted, as in Part 1 — Part 2's out-of-order handling and Part 3's
per-merchant rules are independent axes, not combined).

Every `(merchant_id, status_code)` pair uses **its merchant's** rule: the override rule for that
`merchant_id` if one was given, else `(DEFAULT_WINDOW, DEFAULT_THRESHOLD)`. A merchant's rule is
fixed for the whole run (it does not change mid-stream). Apply Part 1's TRIGGER/RESOLVE logic
per pair using that pair's merchant's `(window, threshold)`; merge all pairs' events into one
chronologically-ordered output list exactly as in Part 1/2.

### Part 4 — two-severity escalation ladder
Params line: `WARN=<int> CRIT=<int> WINDOW=<int>` (`CRIT > WARN`, both `>= 1`). Logs are sorted, as
in Part 1. Each pair's rolling count (same `[t - WINDOW + 1, t]` window as before) now has three
possible **levels**: `0` (`count < WARN`), `1` (`WARN <= count < CRIT`), `2` (`count >= CRIT`).
Every time a pair's level changes (checked after folding each record into the rolling count, same
as before), emit one event **per threshold boundary crossed**, in the direction of travel:
* Crossing **up** through the `WARN` boundary (level `0 -> 1`): `TRIGGER`.
* Crossing **up** through the `CRIT` boundary (level `1 -> 2`): `ESCALATE`.
* Crossing **down** through the `CRIT` boundary (level `2 -> 1`): `DEESCALATE`.
* Crossing **down** through the `WARN` boundary (level `1 -> 0`): `RESOLVE`.

A single record can move a pair's level by more than one step (e.g. a huge `count` jumps a pair
straight from level `0` to level `2`, or the window sliding forward drops enough old volume to
fall straight from level `2` to level `0`). In that case emit **every** boundary event the
transition crosses, in traversal order, all timestamped at that same record's `timestamp` — e.g.
`0 -> 2` emits `TRIGGER` then `ESCALATE` (in that order); `2 -> 0` emits `DEESCALATE` then
`RESOLVE` (in that order). Output format and chronological ordering are unchanged from Part 1
(`timestamp,merchant_id,status_code,event_type`).

## Worked examples
```
# Part 1 -- this is the confirmed real example (window=3, threshold=4)
WINDOW=3 THRESHOLD=4
1,m1,500,2
2,m1,500,2
5,m1,500,1
6,m1,500,1
->
2,m1,500,TRIGGER
5,m1,500,RESOLVE
# window [t-2,t]. t=2: window [0,2] sums the t=1 and t=2 records -> 2+2=4 >= 4 -> TRIGGER.
# t=5: window [3,5] only the t=5 record is in range -> 1 < 4 -> RESOLVE. t=6: window [4,6] sums
# t=5,t=6 -> 1+1=2, still < 4, no new event (already resolved).

# Part 1 -- second confirmed example: two independent pairs, same threshold, window=3
WINDOW=3 THRESHOLD=3
1,A,404,2
1,A,404,1
2,B,500,3
3,A,404,1
4,B,500,1
->
1,A,404,TRIGGER
2,B,500,TRIGGER
# Two records share timestamp 1, both for (A,404): processed in input order. After the first
# (count=2) the window [-1,1] sums to 2 < 3, no event. After the second (count=1) the window
# sums to 2+1=3 >= 3 -> TRIGGER at t=1. (B,500)'s single record at t=2 sums to 3 >= 3 -> TRIGGER
# at t=2. Later records for both pairs keep them above threshold, so no RESOLVE follows.

# Part 2 -- same logs as the first Part 1 example, but shuffled in the input
WINDOW=3 THRESHOLD=4
6,m1,500,1
1,m1,500,2
5,m1,500,1
2,m1,500,2
->
2,m1,500,TRIGGER
5,m1,500,RESOLVE
# identical output to the sorted version -- Part 2 sorts by timestamp first, so input order of
# the *file* doesn't matter, only each record's own timestamp does.

# Part 2 -- tie-break demonstration: two different pairs share a timestamp; whichever one
# appears FIRST in the input is emitted first in the output, even though this is not
# merchant_id-alphabetical order
WINDOW=5 THRESHOLD=5
1,B,500,5
1,A,404,5
->
1,B,500,TRIGGER
1,A,404,TRIGGER
# B comes first in the input at the same timestamp, so B's TRIGGER is emitted first --
# swap the two input lines and the output order swaps too (not sorted by merchant_id).

# Part 3 -- default rule (window=3, threshold=4) plus one merchant override (m2: window=2, threshold=3)
DEFAULT_WINDOW=3 DEFAULT_THRESHOLD=4 RULES=1
m2,2,3
1,m1,500,2
2,m1,500,2
5,m1,500,1
6,m1,500,1
1,m2,404,3
2,m2,404,1
->
1,m2,404,TRIGGER
2,m1,500,TRIGGER
5,m1,500,RESOLVE
# m1 has no override -> uses the default rule -> same two events as the first Part 1 example.
# m2 uses its own rule (window=2 -> [t-1,t], threshold=3): at t=1, window [0,1] sums to 3 -> TRIGGER
# at t=1. At t=2, window [1,2] sums 3+1=4, still >= 3, no new event. Merged chronologically: m2's
# TRIGGER at t=1 comes before m1's TRIGGER at t=2.

# Part 4 -- full escalation/de-escalation cycle (warn=3, crit=6, window=3)
WARN=3 CRIT=6 WINDOW=3
1,m1,500,2
2,m1,500,2
3,m1,500,3
5,m1,500,1
7,m1,500,1
->
2,m1,500,TRIGGER
3,m1,500,ESCALATE
5,m1,500,DEESCALATE
7,m1,500,RESOLVE
# t=1: window[-1,1] sum=2 < WARN(3) -> level 0, no event.
# t=2: window[0,2] sum=2+2=4 -> WARN<=4<CRIT -> level 1 (0->1): TRIGGER.
# t=3: window[1,3] sum=2+2+3=7 -> >=CRIT(6) -> level 2 (1->2): ESCALATE.
# t=5: window[3,5] sum=3+1=4 (t=1,2 expired) -> level 1 (2->1): DEESCALATE.
# t=7: window[5,7] sum=1+1=2 -> level 0 (1->0): RESOLVE.

# Part 4 -- a single record jumps two levels at once (both directions)
WARN=3 CRIT=10 WINDOW=2
1,m1,500,1
2,m1,500,20
10,m1,500,1
->
2,m1,500,TRIGGER
2,m1,500,ESCALATE
10,m1,500,DEESCALATE
10,m1,500,RESOLVE
# t=1: window[0,1] sum=1 < WARN -> level 0.
# t=2: window[1,2] sum=1+20=21 -> jumps straight to level 2 (0->2): emits TRIGGER then ESCALATE,
# both timestamped 2, in that order (crossing WARN before CRIT on the way up).
# t=10: window[9,10] sum=1 (t=1,2 long expired) -> jumps straight to level 0 (2->0): emits
# DEESCALATE then RESOLVE, both timestamped 10 (crossing CRIT before WARN on the way down).

# Zero log lines, any part (the params line is still present -- see Input format above)
part1(["WINDOW=1 THRESHOLD=1"]) == []
part4(["WARN=1 CRIT=2 WINDOW=1"]) == []
```

## Edge cases hidden tests are known to target
- Part 1: window boundary exactly `t - WINDOW + 1` (included) vs one second earlier (excluded);
  a pair that is flagged once and never resolves (only a `TRIGGER` line, input ends while still
  above threshold); a pair that never crosses the threshold at all (zero events, not `RESOLVE`
  with no prior `TRIGGER`); `count` exactly equal to `THRESHOLD` counts as `>=` (triggers).
- Part 2: fully reverse-sorted input still produces the sorted-order output; two different pairs
  sharing an exact timestamp preserve **input order**, not `merchant_id` order, in the output
  (both directions must be tested — swap the two lines and the output order swaps too).
- Part 3: `RULES=0` (every merchant uses the default, no override lines follow the params line);
  a merchant with an override whose `window`/`threshold` differ from the default in both
  directions (looser and stricter); two different merchants' events interleaving correctly in the
  merged chronological output even though their windows are different sizes.
- Part 4: a level-0-to-level-2 jump in one record (emits `TRIGGER` then `ESCALATE`, same
  timestamp, that order); a level-2-to-level-0 jump (emits `DEESCALATE` then `RESOLVE`, that
  order); `count` landing exactly on `WARN` (level 1, not 0) and exactly on `CRIT` (level 2, not
  1) — the non-strict `>=` boundary is symmetric at both thresholds; a pair that reaches level 1
  and drops back to 0 without ever reaching level 2 (only `TRIGGER`/`RESOLVE`, never
  `ESCALATE`/`DEESCALATE`).
- All parts: `0` log lines (empty output, regardless of params); a single log line; multiple
  independent `(merchant_id, status_code)` pairs whose windows never overlap in a way that would
  cause cross-contamination (a bug that accumulates one shared running sum across all pairs
  instead of one per pair is a classic S04 failure this targets).

## Variants seen in the wild
- The only known primary source (PracHub id 7608, see Sources) explicitly frames this as
  "needs a queue" (候选人原文：*"应该是要用queue的"*) — consistent with the sliding-window-with-
  deque implementation this problem's reference solution uses, though the candidate did not
  elaborate further.
- PracHub's own auto-generated structured shell around that same report (also in Sources) exposes
  a single function `detect_events(logs, window_size, threshold)` taking tuples, not the
  `PART n` / line-based I/O this suite's problems use, and its own worked examples use `>=` at
  both the `TRIGGER` and `RESOLVE` boundary directions exactly as this problem.md states — that
  structured shell's *rule* (Part 1 here) is corroborated across two independently-generated
  presentations of the same underlying report; its *I/O format* is not carried over here (this
  suite's `part1(lines) -> list[str]` convention is used instead, per `CONVENTIONS.md`).

## What this tests
skills: S04 (group by `(merchant_id, status_code)`, apply the rule once per group, never share
state across pairs) · S05 (threshold semantics — `TRIGGER` is `< threshold` becoming
`>= threshold`, `RESOLVE` is the exact mirror image; Part 4 doubles this with two independent
boundaries that must not be conflated) · S10 (event stream + state reversal — `TRIGGER`/`RESOLVE`
is a textbook two-state reversal, Part 4 extends it to a three-level ladder) · S12 (time-bucketed
rolling window arithmetic, closed-interval boundary discipline) · S16 (sliding-window / rate-limit
style counters via a per-key deque, evicting expired volume as the window slides).

## Sources
- https://prachub.com/coding-questions/detect-trigger-and-resolve-events （PracHub, id 7608，`curl`
  抓取，2026-09-03 access，本 session 独立复抓核实，与 `catalog/discovery/2026-09/C_batchB.md`
  `## C9` 一节记录一致）— 候选人第一人称原始报告（`content` 字段，`created_at: "2026-01-15T00:00:00"`,
  `interview_round: "Technical Screen"`, `is_ai_assisted: false`）逐字摘录：*"Hackerrank Screening
  轮遇到了一道新题，有一组 transaction logs，每一条 log 包含：timestamp, merchant_id, status_code,
  count。第一部分是需要根据日志数据，针对每个 (merchant_id, status_code) 统计错误情况，当某个错误状态
  在最近一段时间内累计达到一定次数时生成一个 TRIGGER 事件，当之后错误次数下降到阈值以下时生成一个
  RESOLVE 事件，然后输出。应该是要用queue的。二三部分有点忘了。求加米！！谢谢"*
- 同页面 PracHub 结构化题面（同一 `curl` 抓取）—— 滚动窗口公式（`[t - window_size + 1, t]` 闭区间）、
  `TRIGGER`/`RESOLVE` 的 `< threshold` ⇄ `>= threshold` 双向语义、"不发连续同类型重复事件"、两个完整
  数值样例（`window_size=3, threshold=4` 与 `window_size=3, threshold=3` 两组，均在本 problem.md 的
  worked examples 里逐字复用并换算成本题的行式 I/O），本 session 独立复抓与
  `catalog/discovery/2026-09/C_batchB.md` `## C9` 一节记录逐字一致。
- **本 problem.md 未能确认这就是 catalog 记录的「Incident Monitor」这道题**——PracHub 标题
  「Detect Trigger and Resolve Events」与 catalog 的标题不同，且候选人本人说"二三部分有点忘了"，
  没有任何来源描述过 Part 2/3（如果这道题真的有多个 part 的话）。因此 Part 2-4 的规则、全部输入输出
  格式、以及"分几个 part"这个决定本身，都是本仓库为覆盖 S04/S05/S10/S12/S16 而自拟的训练设计，不代表
  任何已知的真实面试题面。
- `catalog/discovery/2026-09/C_batchB.md` `## C9` 一节（本轮排查记录，含失败检索式、interviewdb.io
  与 GitHub `divyavenn/coding_problems` 两处交叉验证"未发现同名题"的证伪证据）。

## 与 q41 的区别
`problems/q41_observability_metrics`（OA 阶段，纯重建题，指标聚合 → 时间窗 → 告警规则）与本题
`ps13_incident_monitor`（电面阶段，Part 1 规则来自真实候选人报告 + 本仓库自拟扩展）主题相邻，
都属于"可观测性/监控告警"这个知识域（S24），但规则集是两回事，练习时不要混着背：
- **来源与置信度不同**：q41 目前是本仓库纯粹按 OA 阶段常见题型自拟重建的（没有任何候选人报告作为
  锚点）；ps13 的 Part 1 有真实候选人报告 + PracHub 结构化题面的双重印证（虽然标题对不上，置信度按
  "部分线索"处理，见上方警示块），Part 2-4 才是纯自拟。两题的"重建程度"不是同一量级。
- **分组维度可能不同**：ps13 严格按 `(merchant_id, status_code)` 二元组分组；q41 是"指标聚合"，通常
  按单一 metric 名或 metric+维度标签分组——不要假设两题的分组 key 结构一样。
- **规则语义的落点不同**：ps13 的核心是 TRIGGER/RESOLVE（以及 Part 4 的 ESCALATE/DEESCALATE）严格镜像
  的阈值方向语义，配合逐条 log 增量式重新评估状态；q41 是"指标聚合 → 时间窗 → 告警规则"这个更通用的
  三段管线，具体的窗口聚合方式（sum/avg/max?）、告警规则形状（单阈值/多档/滞回?）都可能与 ps13 不同，
  **不要把 ps13 这里 `[t - window_size + 1, t]` 闭区间累加求和的具体公式当成 q41 的公式去套**。
- **事件命名不同**：ps13 用 `TRIGGER`/`RESOLVE`/`ESCALATE`/`DEESCALATE`；q41 的事件命名（如果有）应以
  q41 自己的 problem.md 为准，两套字符串不能混用。
- 本节写作时 `problems/q41_observability_metrics` 尚未在本仓库落地（由另一位代理并行建设中），因此以
  上是基于任务描述做的"预防性区分"，而非逐条核对过 q41 最终题面——**q41 落地后应回来核对本节是否需要
  更新**，参照 `loop/rounds/06_coding_onsite/cd01_subscription_email_scheduler/problem.md` 里对
  `q07_subscription_notifications` 的处理方式（同一手法：先声明"故意用不同字段/事件名/输出格式"，
  避免两题被当成同一套规则背诵）。

## 面试官会怎么追问
1. "如果同一个 `(merchant_id, status_code)` 的两条 log 时间戳完全相同，谁先处理由什么决定？" ——
   检验"稳定排序、按输入顺序 tie-break"这条隐含契约是否真的写进了代码，而不是随手 `sorted(key=ts)`
   丢失原始顺序。
2. "`WINDOW` 如果非常大（比如 10^9），你的滑动窗口 deque 实现还成立吗？内存会不会爆？" —— 期望候选人
   指出 deque 里只存"当前还在窗口内"的记录，数量受限于该 pair 的 log 条数而非 WINDOW 的数值本身，
   `WINDOW` 的大小不影响内存占用。
3. "Part 4 如果不是两档（WARN/CRIT），而是任意 N 档阈值，你的实现要改多少？" —— 检验是否用了"硬编码两
   个 if"还是"按阈值列表排序后算 level + 遍历跨越的边界"这种可扩展设计。
4. "如果 `count` 可能是负数（比如一条'撤销'记录），滚动窗口求和还成立吗？TRIGGER/RESOLVE 的方向性会
   不会反过来？" —— 纯边界假设检验，答案应该是"求和逻辑本身不变，但如果允许负数，同一个窗口内可能
   出现和忽高忽低的抖动，需要重新考虑'不发连续同类型事件'这条去重规则是否还够用"。
5. "这道题如果要处理实时流（logs 不是一次性给你，而是一条条到达且未来还有更多），Part 1 的实现要怎么
   改？" —— 期望候选人意识到当前"先读完整个 stdin 再处理"只是训练场景的简化，核心的"per-pair
   deque + running sum"逻辑本来就是流式的，只是被 I/O 边界掩盖了。
