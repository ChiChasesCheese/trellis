# od05 · Cron Scheduler — schedule/pause/resume/tick, pause-vs-claim race, multi-instance lease

**类型：** 技术筛（PS，60 min，3 part + 追问）· **最近：** 2026-06
**置信度：** LOW-MED（单一聚合来源，但与 Snowflake 自家 TASK 产品强锚定，见文末）

## 背景
Snowflake 的 TASK 对象本身就是一个 cron 调度系统
（https://docs.snowflake.com/en/user-guide/tasks-intro），来源要求实现的正是这类系统的核心：
`schedule`/`pause(job_id)`/`resume(job_id)`，外加"多实例安全、不重复触发"和"crash 恢复不丢
触发"。本题把后两点合并成一道 3-part 题：先写单实例的 API 与 tick 循环，再处理
pause-与-claim 之间的竞态，最后扩展到"两个调度器实例共享同一批任务、谁都不能重复触发同一次"。

## API 契约（英文签名）
```python
class CronScheduler:
    def __init__(self, lease_store: "LeaseStore | None" = None) -> None: ...
    def schedule(self, job_id: str, cron_expr: str) -> None: ...
    def pause(self, job_id: str) -> None: ...
    def resume(self, job_id: str) -> None: ...
    def tick(self, now: int) -> list[str]: ...
        # now: 距 epoch 的分钟数（整数）；返回本次 tick 里被这个实例"认领"到的 job_id 列表

class LeaseStore:
    """模拟一个外部共享的租约存储（生产环境会是 Redis/DB 行），供多个 CronScheduler 实例共享，
    实现"同一个 (job_id, 分钟) 只能被一个实例认领一次"。"""
    def try_claim(self, job_id: str, minute: int) -> bool: ...
```
`cron_expr` 是标准 5 字段 `分 时 日 月 周` 格式的**子集**：每个字段要么是 `*`（任意）、要么是
`*/n`（能整除 n），本题**不实现**逗号列表/范围（`1,15` 或 `1-5`）——这些留作变体追问，不在测试
覆盖范围内。`now` 到日历字段的换算用 UTC：`datetime.utcfromtimestamp(now * 60)` 的
`minute/hour/day/month`，`weekday`（Monday=0…Sunday=6）用 `.weekday()`。

## 规则

### Part 1 — API 与 tick 循环
- `schedule(job_id, cron_expr)`：注册一个任务（覆盖同 id 的旧注册），初始状态为**未暂停**、
  从未触发过。
- `pause(job_id)`/`resume(job_id)`：切换任务的暂停状态；对不存在的 `job_id` 静默忽略（不抛
  异常——生产环境里"pause 一个刚被删除的任务"不应该让调用方处理异常）。
- `tick(now)`：对每个已注册、**未暂停**的任务，检查它的 cron 表达式是否匹配 `now` 对应的日历
  字段（5 个字段全部匹配才算命中），且这个任务在**这一分钟**（`(job_id, now)` 这个组合）还没
  被认领过——命中且未认领则认领（记录 `(job_id, now)` 已认领）并加入返回列表。同一个
  `(job_id, now)` 组合只能被认领一次，即使 `tick(now)` 被调用多次（例如恢复/重放场景）。

### Part 2 — pause 与 claim 的竞态
`pause(job_id)` 和 `tick(now)` 可能被不同线程并发调用。要求：一次 `tick(now)` 对某个
`job_id` 的"检查未暂停 + 认领"必须是原子的——不会出现"检查时未暂停，但认领动作发生在
`pause()` 之后却仍然算数"的中间态。可测试的定义（本题采用）：多个线程并发调用
`tick(now)`（同一个 `now`，同一批任务），最终**这一分钟**里每个命中的 `job_id` 在所有线程
返回值的并集里**恰好出现一次**——这直接检验"认领"本身的原子性，是"pause 竞态"这个说法在
单实例、多线程场景下的可测试核心。

### Part 3 — 多实例租约，两个调度器不重复触发
两个（或更多）`CronScheduler` 实例可能分别跑在不同进程/机器上，各自独立 `schedule` 了**相同**
的任务集合，各自的 `tick(now)` 几乎同时被调用。要求：给它们传入**同一个** `LeaseStore` 实例
（构造函数的 `lease_store` 参数），`tick` 内部对每个候选任务改用
`lease_store.try_claim(job_id, now)` 做认领判断——`try_claim` 对同一个 `(job_id, minute)`
只有第一次调用返回 `True`，之后（无论是同一个实例还是另一个实例调用）都返回 `False`。这样，
即使两个调度器实例的 `tick(now)` 真的在同一时刻被不同线程调用，命中的每个任务也只会被**恰好
一个**实例认领到。

## Worked examples

**例 1（Part1，`*/n` 与固定分钟字段，`now` 是"分钟数since epoch"）**
```
schedule("a", "*/15 * * * *")   -- 每当分钟字段能被 15 整除时触发（00/15/30/45 分）
schedule("b", "30 9 * * *")     -- 每天 UTC 09:30 触发（分钟字段固定=30，小时字段固定=9）
tick(now=0)      -- 1970-01-01 00:00 UTC：分钟=0，小时=0
tick(now=15)     -- 1970-01-01 00:15 UTC：分钟=15，小时=0
tick(now=570)    -- 570 分钟 = 9 小时 30 分 -> 1970-01-01 09:30 UTC：分钟=30，小时=9
tick(now=571)    -- 1970-01-01 09:31 UTC：分钟=31，小时=9
```
→
```
["a"]
["a"]
["a", "b"]
[]
```
（`now=570` 时分钟字段是 30，`30 % 15 == 0` 对 a 命中，`分钟=30 且 小时=9` 也让 b 命中——两个
任务在同一个 tick 里都触发，输出按字典序排序为 `["a", "b"]`；`now=571` 时分钟字段是 31，两个
表达式都不再匹配。）

**例 2（Part2，并发 tick 认领恰好一次）**
20 个线程对同一个 `CronScheduler`（已 `schedule` 一个每分钟触发的任务 `"*/1 * * * *"`）在
`now=100` 并发调用 `tick(100)`；所有线程返回值拼起来，`"job"` 这个 id 总共只出现一次。

**例 3（Part3，两个实例共享 LeaseStore 不重复触发）**
两个 `CronScheduler(lease_store=shared)` 实例都 `schedule("job", "*/1 * * * *")`；分别用两个
线程在 `now=200` 同时调用各自的 `tick(200)`；两次调用返回值的并集里 `"job"` 只出现一次（不是
两次——如果两个实例各自独立认领，`"job"` 会出现两次，这正是本 part 要防止的 bug）。

## `main()` 命令流
```
SCHEDULE <job_id> <cron_expr...>   -- cron_expr 是本行剩余部分（5 个字段，空格分隔）
PAUSE <job_id>
RESUME <job_id>
TICK <now>
```
`SCHEDULE`/`PAUSE`/`RESUME` 无输出。`TICK` 输出一行 `repr(sorted(fired_job_ids))`（Python list
字面量，按字典序排序以保证输出确定性——`tick()` 本身返回的顺序不保证，`main()` 层负责排序）。

## 边界清单
- `pause`/`resume` 一个不存在的 `job_id`：静默忽略，不抛异常
- 已暂停的任务即使 cron 匹配也不会出现在 `tick` 的返回里；`resume` 之后、且尚未被认领过的
  那一分钟里再次匹配才会触发
- 同一个 `(job_id, now)` 只能被认领一次：连续两次 `tick(相同的 now)` 第二次不会重复返回同一个
  刚触发过的 job（即使它一直保持未暂停）
- `*/1` 等价于 `*`（每个单位都匹配）；`*/60` 的分钟字段只在分钟为 0 时匹配
- `*/n` 的判断对象永远是**日历字段本身**（分钟 0–59、小时 0–23、日 1–31、月 1–12），不是
  `now`（分钟数 since epoch）直接对 n 取模——两者在分钟字段上恰好等价（因为分钟字段本身就是
  `now % 60`），但小时/日/月字段绝不能直接用 `now` 取模，必须先换算成日历字段再判断
- 崩溃恢复（来源要求 "no lost triggers"）：本题不实现持久化存储，约定"认领记录"只要在进程
  存活期间不丢即可，重启后的恢复策略作为并发追问的开放讨论，不写测试

## 并发追问
1. "`pause` 和 `tick` 的竞态，如果不是靠一把全局锁，而是想要更细粒度的锁，应该锁什么？" ——
   期望候选人指出锁的粒度应该是**每个 job_id**（认领判断只需要跟这一个任务的暂停状态和认领
   记录互斥），而不是所有任务共享一把大锁,同时讨论"认领记录"这个 map 本身的并发访问也需要保护。
2. "`LeaseStore.try_claim` 在真实生产环境里会怎么实现？" —— 期望候选人提出 Redis 的
   `SET key value NX` 或数据库的"唯一约束 + INSERT ... ON CONFLICT DO NOTHING"，都是"第一个
   写入者赢"的原子操作，与本题 in-memory 版的 `dict.setdefault`/锁实现是同一个思路的不同载体。
3. "crash 恢复：某个实例认领了一个任务但在真正执行前就崩溃了，这个触发算不算丢失？" —— 期望
   候选人讨论"认领"与"执行完成"要分两步确认（类似消息队列的 ack），认领只是获得"这次尝试执行"
   的权利，真正的 exactly-once/at-least-once 语义需要执行完成后再标记，本题的 `tick`/
   `try_claim` 只解决"不重复认领"，不解决"认领后执行失败怎么办"——这是留给 od09（queue→service）
   的问题，两题在追问里经常被连起来问。

## 变体
- 来源要求的完整 cron 语法（逗号列表、范围 `1-5`）本题不实现，作为"如果要支持完整 cron 语法，
  这个 matcher 要怎么改"的口头追问方向。
- 一处来源把这道题和持久化/WAL 放在一起问（"crash recovery and reliability with no lost
  triggers"），与 od01 的持久化 part、od02 的 WAL 追问是同一个主题在不同题里反复出现，说明
  "调度 + 持久化"是 Snowflake 面试官偏好的组合追问。

## 来源与置信度
- https://prachub.com/interview-questions/design-a-cron-job-scheduler （Medium, Technical
  Screen）；要求原文（转述）："(a) Public API (b) Data model (c) Core scheduler loop (d)
  Correct pause/resume semantics, including race conditions (e) Multi-instance safety without
  double-firing (f) Crash recovery"
- Snowflake 官方文档 https://docs.snowflake.com/en/user-guide/tasks-intro 与
  https://docs.snowflake.com/en/sql-reference/sql/create-task（不是面试题来源，但独立确认
  Snowflake 自家产品就是这类 cron/TASK 系统，是这道题被反复问到的领域锚点）
- `catalog/raw/ood.md` #5、`catalog/CATALOG.md` Table B od05 行；置信度 **LOW-MED**：单一聚合站
  （PracHub）来源，但与 Snowflake 自家产品高度吻合，不是凭空编造的题型。

## 考什么
S09 类设计先定 API 契约（`pause`/`resume` 对不存在 id 静默忽略 vs 抛异常的取舍）· S10 并发正确性
（认领的原子性、锁粒度、跨实例的分布式租约）· S11 持久化与恢复（追问层面，"认领"与"执行完成"
分两步确认）· D03（系统设计侧的调度器：幂等、lease、失败隔离，与 sd02 同族）
