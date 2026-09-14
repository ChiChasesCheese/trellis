# od05 Cron Scheduler — report

## Summary
一个 minute-granularity cron 子集（`*`/`*/n`/固定字段）的调度器：单实例的 `schedule`/`pause`/
`resume`/`tick` → pause 与 claim 之间的竞态 → 多实例共享租约、两个调度器不重复触发。与 Snowflake
自家 TASK 对象（cron 驱动的调度产品）在形状上高度吻合，是"分布式系统/调度器"这条 D03 系统设计
主题的编码版投影。

## Sources & confidence
LOW-MED——单一聚合来源（PracHub, Medium, Technical Screen），但要求原文明确列出六个设计维度
（API/数据模型/调度循环/pause-resume 竞态/多实例安全/崩溃恢复），且与 Snowflake 官方文档
（`docs.snowflake.com/en/user-guide/tasks-intro`）描述的 TASK 产品高度吻合——不是凭空编造的题型,
但没有一手候选人挂经交叉，故置信度停在 LOW-MED。完整 cron 语法（逗号列表/范围）来源要求提及但
本题不实现，作为口头追问方向。

## Approach by part
1. `_matches(cron_expr, now)` 把 `now`（分钟数 since epoch）换算成 UTC 日历字段
   （`datetime.fromtimestamp(now*60, tz=utc)`），5 个字段各自用 `_field_match` 独立判断
   （`*`/`*/n`/固定整数），全部匹配才算命中。`tick` 对每个未暂停且命中的任务尝试"认领"
   `(job_id, now)`。
2. "认领"抽成 `_claim`：单实例场景下，先在锁内重新确认任务仍未暂停（收紧 pause 与 claim 之间的
   竞态窗口），再检查/写入本地的 `_local_claims` 集合，整个过程在同一把锁内完成，保证并发
   `tick()` 调用不会让同一个 `(job_id, minute)` 被认领两次。
3. 多实例场景（Part3）把认领判断整体委托给共享的 `LeaseStore.try_claim`——它自己内部持锁，
   保证"同一个 `(job_id, minute)`，不管来自哪个调度器实例调用，只有第一次返回 `True`"，从而让
   两个各自独立 `schedule` 了相同任务的调度器实例永远不会同时触发同一次。

## Pitfalls hidden tests target
- `*/n` 的判断对象是日历字段本身（分钟 0–59 等），不是 `now` 原始值直接取模——小时/日/月字段
  尤其容易写错
- `pause`/`resume` 对不存在的 job_id 静默忽略，不抛异常
- 同一个 `(job_id, minute)` 只能被认领一次，即使反复 `tick(同一个 now)` 或被多个线程并发调用
- 重新 `schedule` 同一个 id 会重置暂停状态（问题陈述里"初始状态为未暂停"对重新注册同样成立）
- 并发 `tick`：同一分钟内，一个命中的 job 在所有并发调用的返回值并集里恰好出现一次
- 多实例：两个独立调度器各自 `schedule` 了相同任务、共享一个 `LeaseStore`，并发 `tick` 同一个
  `now` 时该任务只被其中一个实例认领到一次——不给它们共享 `LeaseStore` 就会重复触发（这正是
  Part3 要防止的 bug，测试里刻意验证"给共享 store 前后行为不同"隐含的这条底线）
- `pause` 是每个调度器实例自己的状态，不通过共享的 `LeaseStore` 传播——在一个实例上 `pause`
  不妨碍另一个仍然未暂停的实例去认领同一个任务

## Complexity & measured cost
`tick(now)` 是 O(已注册任务数)（线性扫描 + 逐个日历字段匹配）；`_claim` 是 O(1) 均摊。2000 个
任务、200 次 `tick` 的 perf 测试通过 `run_script` 实测 well under 2s / 256MB。

## Test inventory
16 tests — part1: 11（含 1 io、1 fmt、1 perf）· part2: 2（并发）· part3: 3（多实例）；edge 9 ·
fmt 1 · io 2 · perf 1。

## Skills exercised
S09 类设计先定 API 契约（`pause`/`resume` 对未知 id 静默忽略的取舍）· S10 并发正确性（认领原子
性、pause-vs-claim 竞态窗口、跨实例租约）· S11（间接，追问层面讨论"认领"与"执行完成"分两步确认，
呼应 od09 的 ack 语义）· D03 调度器：幂等、lease、失败隔离（与 sd02 同族）
