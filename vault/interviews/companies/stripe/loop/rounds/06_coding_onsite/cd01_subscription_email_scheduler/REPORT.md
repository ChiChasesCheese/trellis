# cd01 Subscription email scheduler — report

## Summary
An onsite "Programming Exercise" build of the subscription-lifecycle-email family that recurs
across Stripe's coding round (see also `problems/q07_subscription_notifications`). This version
uses calendar dates and a single mutable per-user state machine instead of q07's day-offsets and
explicit `[Changed]`/`[Renewed]` announcement lines — the two are siblings drawn from the same
theme, not duplicates, and are cross-referenced in both problem.md files so a reader doesn't
confuse them. The core difficulty is nailing one rule ("discard pending emails strictly after the
event date, then reschedule") and applying it uniformly to four different event types.

## Sources & confidence
medium. Corroborated by four independent write-ups (`loop/raw/en_forums.md` §6.2 C1: linkjob
intern 2025, linkjob "2026 Java NG VO" 2025-12-08, Simplify 2026; `loop/raw/cn_forums.md` line 99:
1point3acres 「Subscription Email Scheduler」TOC) on the 3-part shape (basics -> plan changes ->
renewals) and the domain. None publishes exact field names, output format, or the proration
formula -- those are this problem.md's own concrete, internally-consistent reconstruction, explicitly
flagged in the "Variants" section. The follow-up list at `cn_forums.md` line 264 (「Email
Notification Scheduler」, dedup/rate-limit/ordering/out-of-order/cancel) is real and is folded
directly into "面试官会怎么追问" rather than treated as base requirements -- the source itself frames
them as discussion follow-ups, not implemented rules.

## Approach by part
1. **Part 1**: pure schedule generation. `expire = date + period_days(plan)`
   (`monthly=30, annual=365`); emit `welcome@date`, `expiring@(expire-7)`, `expiring@(expire-1)`,
   `expired@expire`.
2. **Part 2**: one rule, applied once, reused everywhere in Part 3 too -- at event date `d`, drop
   every pending email dated *strictly after* `d` (not `>=`; same-day emails are already
   "committed"), then reschedule from the new state. `change`'s proration is integer floor:
   `remaining_new = remaining_old * period_days(new) // period_days(old)`.
3. **Part 3**: `renew` either extends the term from the *old* expiry (still active) or -- if the
   term already lapsed -- becomes a fresh `subscribe` (welcome, not renewed). `cancel` applies the
   discard rule with nothing new to reschedule, and is idempotent.

## Pitfalls hidden tests target
- **same-day, not-revoked emails**: a `change`/`renew`/`cancel` landing on the exact date of an
  already-scheduled `expiring` does not revoke it (`> d`, not `>= d`) -- produces two lines dated
  the same day, one from the old schedule and one from the new. This is the single most subtle
  rule in the problem and is exercised directly by
  `test_change_causing_immediate_expiry_keeps_same_day_old_emails`.
- output order is a **fixed type priority** (`welcome<expiring<expired<renewed<canceled`), not
  event-processing order -- `test_same_day_cancel_then_resubscribe_orders_by_type_not_event_order`
  shows a `canceled` printing *after* a same-day `welcome` even though cancel was processed first.
- `change` exactly on the expiry day, or for an unknown/canceled user, is silently ignored (not an
  error, not a crash).
- integer floor division in proration, never rounding -- verified against a `remaining_old ==
  period_days(old)` case where the floor loses nothing (exact), contrasted with the immediate-expiry
  case where it floors all the way to 0.
- duplicate `subscribe` lines are deliberately **not** deduplicated by the base solution (that's a
  named follow-up, not a bug) -- `test_duplicate_subscribe_lines_are_not_deduplicated` pins this
  down so a candidate doesn't "fix" it away from the documented contract.
- events out of chronological order in the input file must still resolve in date order.

## Complexity & measured cost
O(n log n) for the event sort; O(1) amortized per event for the discard/reschedule step since a
user's pending list never holds more than ~3 entries. 100k events across 20k users, shuffled input
order: well under the 2 s / 256 MB perf budget (see `test_perf_100k_events`).

## Test inventory
23 tests -- part1: 7 . part2: 6 . part3: 10 (incl. 1 io, 1 perf); edge 11 . fmt 2 . io 2 . perf 1.

## Skills exercised
S01 reading a multi-part spec . S02 line parsing with an optional trailing field . S03 per-user
mutable state . S08 deterministic multi-key sort with a fixed tie-break . S09 exact formatting .
S10 event streams that retroactively change earlier decisions . S12 calendar-date arithmetic .
S19 incremental design

## 边写边说什么
1. **拿到题面先问**：`renew`/`cancel` 事件里没有 `plan` 字段，说明 renew 永远续同一个 plan——这个假
   设要不要跟面试官确认？如果 renew 也能顺便换 plan，规则会变成 `change`+`renew` 的组合。
2. **写 Part 1 时**：先把 `period_days` 定死成一个查表函数，说明"到期前 7 天/1 天"是从 `expire`
   往回算而不是从 `start` 往前数——这样以后无论是 `change` 还是 `renew` 改了 `expire`，公式都不用
   改，只要重新调用同一个"生成排程"的小函数。这是本题唯一值得刻意抽出来复用的地方。
3. **过渡到 Part 2 时**：提前说清楚"丢弃-重排"这一条规则要在 `change`、`renew`、`cancel` 之间完全
   复用，不要三个事件各写一套——面试官通常会在 Part 3 追问"你这段逻辑是不是可以和 Part 2 共享"，主
   动说出来能提前拿分。
4. **写比例重算时**：显式说"我用整数向下取整，不四舍五入"，并举一个"正好整除"和一个"取整到 0"的例
   子（`test_change_causing_immediate_expiry_keeps_same_day_old_emails`)，证明自己想清楚了边界。
5. **Part 3 renew 的两条分支**：讲清楚"到期前 renew = 续期"和"到期后 renew = 新订阅"是两种完全不同
   的邮件（`renewed` vs `welcome`），并且解释为什么用 `date >= expire` 而不是 `>` 做分界——因为
   `expired` 邮件本身就是在 `expire` 这一天发的，所以那一天已经算"过期状态"。
6. **收尾追问**：参考 problem.md 末尾"面试官会怎么追问"，挑 2-3 条主动展开（去重/幂等设计、流式处
   理下"决定不可撤销"假设失效、时区/DST），展示系统设计视角。

## Open points
- The proration formula (`remaining_old * period_new // period_old`) and the "same-day emails are
  never revoked" rule are this suite's own design choices, made to be simple, deterministic, and
  hand-verifiable -- not verified against an actual Stripe rubric (no source publishes exact
  grading criteria for this problem). If a more precise transcript of this problem surfaces later,
  re-check these two rules first.
- `renew`/`cancel` lines carry no `plan` field by design (renew always keeps the current plan);
  flagged as an open question in "边写边说什么" #1 for a candidate to raise proactively.

## Review（2026-09-02）
**改了什么**
- `solution.py`：`_run` 原本是一个 ~56 行的大函数（四个事件类型的逻辑全部内联），超出 checklist 的
  "函数 ≤ 40 行" 建议，可读性也差（陌生人要通读整个函数才能看清一个事件类型的规则）。拆成
  `_discard_future`（"丢弃-重排"公共规则单独一个函数，供四个 handler 共用）+ `_apply_subscribe` /
  `_apply_change` / `_apply_renew` / `_apply_cancel`（每个 handler 对应 problem.md 里的一条规则，
  10 行左右）+ `_render`（过滤窗口 + 排序 + 格式化）。`_run` 现在只剩一个 10 行的分发循环，60 秒内能
  从 `main` 追到任意一个 Part 的核心规则。新增 `State`/`Emails` 类型别名和函数级 docstring
  （每个 handler 一句话说清"什么时候生效、做什么"）；`_parse` 补了返回类型标注和 docstring。公共 API
  （`part1/2/3`、`main`）未变，`starter_template.py`/`starter.py`/`test_cd01.py` 无需同步签名改动。
- `test_cd01.py`：修了 3 处 flake8 `E741`（循环变量名 `l` 与数字 `1` 易混淆），改名为 `line`；其余是
  `black -l 110` 的自动换行（长断言列表拆成多行、`import datetime` 前补空行），无语义变化。
- 三个 worked examples 逐字喂给 `python3 solution.py`，输出与 problem.md 完全一致（未改动）。
**为什么**：`_run` 超长是 S 项（可读性/函数拆分），按 checklist "S 函数 ≤ 40 行；一个函数一件事" 修；
拆分后每个 handler 直接对应题面里 `change`/`renew`/`cancel` 各自的小节，面试官对照 problem.md 读代码
更快。`E741` 是 flake8 会拦的裸红线（虽不属于 F 类，但 `loop/lint.sh` 不区分类别，全量 flake8 通过才算
过）。题面语义、排序 key、边界规则（同日邮件不撤销、`change` 恰好到期日是 no-op、幂等 cancel）均未变。
**遗留**：无。`solution.py` 已是可复用的规则表结构；problem.md"面试官会怎么追问"里的幂等去重/流式重构/
时区等追问均未实现（按设计，仅口头讨论，见 REPORT 原有"边写边说什么" #6）。
