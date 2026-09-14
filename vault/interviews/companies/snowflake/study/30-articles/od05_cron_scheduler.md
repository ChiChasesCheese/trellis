# od05 · Cron Scheduler：schedule/pause/tick，练的是"认领必须原子、且要跨实例"

> [!tldr]
> - 这题考的是：一个 cron 调度器——注册任务、暂停/恢复、`tick(now)` 判定哪些任务命中并"认领"；单实例内的 pause-vs-claim 竞态、以及多实例共享租约不重复触发
> - 三步套路：先写单实例的 cron 匹配 + tick 循环 → Part 2 把"检查未暂停 + 认领"锁进一个原子操作 → Part 3 把认领判断委托给一个跨实例共享的 `LeaseStore`
> - 最值得带走的一个模式：**"认领"这个动作要么用本地锁保证原子，要么委托给一个外部共享存储的"第一个写入者赢"操作**——两者是同一个思路（compare-and-set）在单机/分布式两种场景下的不同载体

## 类设计先定契约
```python
class CronScheduler:
    def __init__(self, lease_store: "LeaseStore | None" = None) -> None: ...
    def schedule(self, job_id: str, cron_expr: str) -> None: ...   # 覆盖同 id 旧注册，初始未暂停
    def pause(self, job_id: str) -> None: ...                       # 不存在的 id 静默忽略
    def resume(self, job_id: str) -> None: ...                      # 同上
    def tick(self, now: int) -> list[str]: ...                      # 返回本次认领到的 job_id 列表

class LeaseStore:
    def try_claim(self, job_id: str, minute: int) -> bool: ...      # 同一 (job_id,minute) 只有第一次调用返回 True
```
**不变量（写代码前先想清楚）**：
1. `pause`/`resume` 对不存在的 `job_id` 静默忽略，不抛异常。
2. `tick(now)` 只处理未暂停的任务；一个任务 cron 匹配 `now` 且这一分钟 `(job_id, now)` 还没被认领过，
   才算命中并认领。
3. 同一个 `(job_id, now)` 组合无论 `tick` 被调用多少次，只能被认领**一次**。
4. "检查未暂停 + 认领"必须是一个原子操作——不能出现"检查时未暂停，但认领发生在 `pause()` 之后却
   仍然算数"的中间态。
5. 多实例共享同一个 `LeaseStore` 时，`try_claim` 保证同一个 `(job_id, minute)` 全局只被认领一次，
   不管是哪个实例调用的。

## 1. 题目在说什么（人话版）
`schedule(job_id, cron_expr)` 注册一个任务；`pause`/`resume` 切换暂停状态；`tick(now)` 检查所有未
暂停任务的 cron 表达式是否匹配 `now`（换算成 UTC 日历字段后逐字段比较），命中且这一分钟没认领过就
"认领"它并返回。Part 2 要求单实例内多线程并发 `tick`/`pause` 时认领是原子的；Part 3 要求两个调度器
实例共享同一批任务时，谁都不会重复触发同一次。

三行小例子：
```
schedule("a", "*/15 * * * *")   # 每15分钟(00/15/30/45)
tick(now=15)  -> ["a"]           # 分钟=15，15%15==0 命中
tick(now=15)  -> []               # 同一分钟已认领过，不会再触发
```

## 2. 读题：把文字变成模型
- **实体**：任务（`job_id`、`cron_expr`、是否暂停）、认领记录（`(job_id, minute)` 集合）。
- **输入长什么样**：`main()` 命令流 `SCHEDULE/PAUSE/RESUME/TICK`。
- **输出要什么**：`TICK` 输出这次命中并认领到的 job id 列表（`main()` 层排序保证输出确定性）。
- **状态**：任务注册表、暂停集合、认领记录（单实例本地维护，或委托给共享的 `LeaseStore`）。
- **一句话建模**：这是一个 **cron 表达式匹配 + 幂等认领** 的问题——匹配逻辑是纯函数（换算日历字段
  逐个比较），真正的难点在"认领"这个动作的原子性,以及它要不要跨实例共享。

> [!note] 为什么选这个数据结构
> `*/n` 的判断必须针对**日历字段本身**（分钟 0-59、小时 0-23……），不能直接对 `now`（分钟数 since
> epoch）取模——两者只在分钟字段上恰好等价，小时/日/月字段绝不能这样简化,必须先用
> `datetime.fromtimestamp(now*60, tz=utc)` 换算出真实的日历字段再逐个比较。认领记录用一个
> `(job_id, minute)` 的集合（或委托给外部 `LeaseStore`），因为"是否已认领"只需要 O(1) 查询,不需要
> 排序或范围查询。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **接口先行**：先写 `CronScheduler`/`LeaseStore` 的方法签名，明确 `tick` 的返回值语义（这次
   **新认领**到的，不是"所有匹配的"）。
2. **Part 1 最小可用**：写 `_field_match(field, value)`（`*`/`*/n`/固定值三种情况）和 `_matches`
   （换算日历字段后 5 个字段全部匹配才算命中）；`tick` 遍历未暂停任务，命中且未认领就加入结果并
   记录认领。
3. **Part 2 叠加**：把"检查未暂停 + 认领"收进同一把锁的临界区——`tick` 先在锁外拿一份"未暂停任务"
   的快照做 cron 匹配（这一步不改变状态,可以并发），真正认领那一刻（`_claim`）里**再检查一次**
   是否已暂停、是否已认领，这一步必须在锁内完成。
4. **Part 3 叠加**：`_claim` 改成优先调用 `lease_store.try_claim(job_id, minute)`（如果构造时传入了
   共享的 `LeaseStore`），否则退回本地的认领集合。`LeaseStore.try_claim` 自己也要加锁保证跨实例
   调用的原子性。
5. **收尾**：用官方例子验证 `*/15`、固定字段的匹配；`pause` 不存在的 id 静默忽略；同一 `(job_id, now)`
   重复 `tick` 不重复触发。

## 4. 代码怎么组织
```
_field_match(field, value) -> bool           # 单字段匹配：* / */n / 固定值
_matches(cron_expr, now) -> bool             # 换算日历字段后 5 字段全匹配
LeaseStore.try_claim(job_id, minute) -> bool  # 跨实例共享的"第一个写入者赢"
CronScheduler.schedule/pause/resume(...)      # 锁内维护注册表和暂停集合
CronScheduler.tick(now) -> list[str]           # 锁外算候选，_claim 锁内做原子认领
main(stdin, stdout)                            # 解析命令流，分发，排序输出
```
`tick` 故意把"算哪些任务命中"（不改状态，可以放锁外）和"认领"（改状态,必须原子）分成两步——这是
面试官想看到的关键设计：不要为了"简单"而把整个 `tick` 都锁起来,那样会让暂停状态查询也被不必要地
串行化。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
def _field_match(field, value):
    if field == "*":
        return True
    if field.startswith("*/"):
        return value % int(field[2:]) == 0
    return int(field) == value

def _matches(cron_expr, now):                 # now 是分钟数 since epoch，必须先换算日历字段
    minute_f, hour_f, day_f, month_f, weekday_f = cron_expr.split()
    dt = datetime.fromtimestamp(now * 60, tz=timezone.utc)
    return (_field_match(minute_f, dt.minute) and _field_match(hour_f, dt.hour)
            and _field_match(day_f, dt.day) and _field_match(month_f, dt.month)
            and _field_match(weekday_f, dt.weekday()))

class LeaseStore:                             # Part3: 跨实例共享的认领存储
    def __init__(self):
        self._claimed, self._lock = set(), threading.Lock()
    def try_claim(self, job_id, minute):
        with self._lock:
            key = (job_id, minute)
            if key in self._claimed:
                return False
            self._claimed.add(key)
            return True

class CronScheduler:
    def __init__(self, lease_store=None):
        self._jobs, self._paused = {}, set()
        self._lease_store = lease_store
        self._local_claims, self._lock = set(), threading.Lock()

    def tick(self, now):
        with self._lock:                       # 只锁"拿快照"这一步
            snapshot = [(j, e) for j, e in self._jobs.items() if j not in self._paused]
        fired = []
        for job_id, expr in snapshot:           # cron 匹配是纯函数，锁外算
            if _matches(expr, now) and self._claim(job_id, now):
                fired.append(job_id)
        return fired

    def _claim(self, job_id, minute):           # 认领必须原子
        if self._lease_store is not None:
            return self._lease_store.try_claim(job_id, minute)   # 委托给跨实例共享存储
        with self._lock:
            if job_id in self._paused:           # 认领前再检查一次未暂停，缩小竞态窗口
                return False
            key = (job_id, minute)
            if key in self._local_claims:
                return False
            self._local_claims.add(key)
            return True
```

## 6. 并发追问怎么答
- **锁的粒度应该是什么**：理想上是"每个 job_id 一把锁"（认领判断只需要跟这一个任务的暂停状态和
  认领记录互斥），不需要所有任务共享一把大锁；本题的参考实现为了简单用了一把全局锁,但要能口头讲清楚
  更细粒度的方向。
- **`LeaseStore.try_claim` 在真实生产环境怎么实现**：Redis 的 `SET key value NX`，或数据库的
  "唯一约束 + INSERT ... ON CONFLICT DO NOTHING"——都是"第一个写入者赢"的原子操作,和本题内存版的
  `dict`+锁是同一个思路的不同载体。
- **认领了但执行前崩溃算不算丢失**：认领只是获得"这次尝试执行"的权利，真正的 exactly-once/
  at-least-once 语义需要"执行完成"再单独确认（类似消息队列的 ack）；本题的 `tick`/`try_claim` 只
  解决"不重复认领"，不解决"认领后执行失败怎么办"——这个开放问题留给 `od09`（queue→service）。

## 7. 常见跑偏（方法层面，3 条）
- **`*/n` 直接对 `now`（分钟数 since epoch）取模**：只在分钟字段上恰好等价（因为分钟字段本身就是
  `now % 60`），小时/日/月字段这样算完全错误——必须先换算成真实日历字段。
- **把整个 `tick` 方法都锁起来**：虽然"正确"，但会让 cron 匹配这种纯计算也被串行化，锁的粒度应该
  只覆盖"认领"这一步（检查暂停状态 + 检查/写入认领记录）。
- **忘记"认领前再检查一次暂停状态"**：如果 `tick` 先拿快照判断"未暂停"，中途 `pause()` 发生，
  认领那一刻不重新检查暂停状态，会让一个刚被暂停的任务仍然触发——这正是 pause-vs-claim 竞态的
  核心，必须在真正认领的临界区内重新确认。

## 自测清单
- `pause`/`resume` 不存在的 `job_id` 静默忽略。
- 已暂停任务即使 cron 匹配也不出现在 `tick` 返回里；`resume` 后未被认领过的匹配分钟才会触发。
- 同一 `(job_id, now)` 连续两次 `tick` 第二次不重复触发。
- `*/1` 等价于 `*`；`*/60` 分钟字段只在 0 分匹配。
- 20 线程并发 `tick` 同一分钟,命中的 job 在所有返回值并集里恰好出现一次。
- 两个共享 `LeaseStore` 的实例并发 `tick` 同一分钟,同一任务只被恰好一个实例认领到。

## 相关题与 skills id
- skills: **S09**（类设计先定契约，`pause`/`resume` 静默忽略的取舍）· **S10**（并发正确性：认领
  原子性、锁粒度、跨实例租约）· **S11**（持久化追问：认领与执行完成分两步确认）· D03（系统设计侧
  调度器：幂等、lease、失败隔离，与 sd02 同族）。
- 同族：`od01_priority_task_scheduler` 的"snapshot/replay"持久化和本题的"认领后崩溃怎么办"经常被
  面试官在同一场面试里连起来问；`od09_queue_to_service` 接续讨论"认领后执行失败"的问题。
- 练习命令：`python3 loop/mock.py start od05`
