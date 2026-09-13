# od01 · Priority Task Scheduler — tie-breaks, duplicate-ID suppression, concurrency, persistence

**类型：** onsite 类设计（VO，60 min，4 part + 追问）· **最近一手：** 2026-08（1p3a 挂经 t.me/29167）
**置信度：** HIGH（见文末来源）

## 背景
Snowflake 的任务执行框架里有大量"谁先跑"的问题：后台 compaction job、metadata 刷新、用户提交的
异步查询，都要按优先级排队执行。面试官把这个现实问题简化成一个类：`add` 把任务扔进队列，
`execute` 每次挑"当前最该跑"的那个。base 版任务 id 是唯一整数；onsite 的 follow-up 版本把 id
换成可以重复的字符串——重复 id 语义不是"去重"，而是"竞态"：同一个逻辑任务可能被提交了好几次
（重试、多个 client 各交一次），只要**任意一次**跑完，其余排队中/未来还会提交的同 id 任务就永久
作废，不该再被执行第二次。这道题在本仓库里被写成一个类，让 Part1→Part4 共享同一份状态机，
而不是 base/duplicate 两个互不相干的类。

## API 契约（英文签名）
```python
class TaskScheduler:
    def __init__(self) -> None: ...
    def add(self, task_id: str, priority: int, timestamp: int) -> None: ...
    def execute(self) -> str:
        """Pop and return the id of the highest-priority eligible pending task.
        Tie-break: higher priority wins; ties -> earlier timestamp; further ties -> smaller
        task_id (lexicographic, since task_id is a str here). '' if nothing eligible."""
    def snapshot(self) -> list[str]:
        """Return the operation log (one string per add/execute call) needed to reconstruct
        current state via TaskScheduler.replay(...)."""
    @classmethod
    def replay(cls, log: list[str]) -> "TaskScheduler":
        """Rebuild a scheduler by re-applying a snapshot()'d log from scratch."""
```

**改写说明（相对来源的两个 API 版本）：** fastprep 的 base 版用整数 id、空队列返回 `-1`；duplicate
版用字符串 id、空队列返回 `""`。为了让本题的 4 个 part 共享一个类型而不是"改到 Part2 要换类"，本
题统一成**字符串 id + `""` 哨兵**（`str(int)` 也是合法字符串，Part1 的测试例继续用 `"101"` 这种
"看起来像整数"的 id 来验证 tie-break，不影响 base 版语义）。这是本题面对来源的**唯一**改写，写在
这里以免被当成没读清楚原题。

## 规则

### Part 1 — 优先队列 + tie-break
`add(task_id, priority, timestamp)` 把任务放进队列（同一个未执行的 `task_id` 不会重复出现在候选
里——重复添加同一个仍未执行的 id 时，把它当成"更新"：新的 `(priority, timestamp)` 替换旧的，因为
重复添加同一个还没跑的任务在 Part1 的语境里最合理的读法是"这次提交作废上一次"）。`execute()` 从
当前池子里选：**priority 更大者胜**；priority 相同选 **timestamp 更早者**；再相同选 **task_id 字典
序更小者**。选中后把该任务从池子移除并返回其 id；池子为空返回 `""`。

### Part 2 — 重复 ID 抑制
一旦某个 `task_id` 的**任意一次**排队被 `execute()` 选中过，这个 id 就**永久**失效：队列里还没跑
的同 id 副本、以及此后再 `add` 进来的同 id 副本，都不能再被 `execute()` 选中（`execute()` 在扫描
时跳过它们，就像它们从未存在）。注意这与 Part1 的"重复 add 替换"不冲突：Part1 的替换只发生在
"这个 id 从未被执行过"的前提下；一旦执行过，后续 add 完全是无操作（连"替换"都不做——已执行的 id
没有"当前候选"这个概念了）。

### Part 3 — 并发下的 `add`/`execute`
多个线程可能同时调用 `add`/`execute`。要求：
- 两次 `execute()` 调用**永远不会返回同一个已经被判定"执行过"的 id**（即使这两次调用在时间上
  重叠）——已执行判定和"选中并标记"必须是一个原子操作。
- 所有被成功 `add` 过、且从未被任何线程 `execute()` 选中的 id，最终必须能被某次 `execute()` 选
  中恰好一次（不丢任务），除非池子提前耗尽（`execute()` 调用次数 < 待执行任务数）。
- 用 `threading.Lock`（或等价原语）包住"扫描候选 + 标记已执行"这一段临界区即可满足以上两条。

### Part 4 — 持久化：快照 / 重放（**重建**）
来源里"持久化/崩溃恢复"只在 fastprep 的追问列表里被提及为"下一步自然追问"，没有给出具体 API——
本 part 的 `snapshot()`/`replay()` 设计是**本仓库补全**的，用于让候选人练习"如何用操作日志而不是
序列化内部堆结构来做持久化"这个通用套路。`snapshot()` 返回从构造到调用时刻的完整操作日志（每条
`add`/`execute` 调用各占一行，格式与下面 `main()` 的输入行格式相同）；`TaskScheduler.replay(log)`
从空状态重新按顺序把这些操作跑一遍，重建出一个状态上等价的新实例（后续对新旧实例做完全相同的
`add`/`execute` 调用序列，必须产生完全相同的返回值序列——这是本题对"等价"的可测试定义，不要求
内部数据结构一致）。

## `main()` 命令流
```
ADD <task_id> <priority> <timestamp>
EXEC
SNAPSHOT
```
每行一个操作；`ADD`/`SNAPSHOT` 无输出；`EXEC` 输出一行结果（task_id 或空行表示 `""`）。`SNAPSHOT`
是 Part4 专用的测试钩子：把当前调度器替换成 `TaskScheduler.replay(当前.snapshot())` 重建出的新
实例，之后的操作全部作用在新实例上——如果 `snapshot`/`replay` 正确，替换前后的行为必须完全不可
区分（例4）。

## Worked examples

**例 1（Part1，tie-break：priority → timestamp → id 字典序）**
```
ADD 101 2 100
ADD 102 5 50
EXEC
ADD 103 5 30
EXEC
EXEC
EXEC
```
→ `["102", "103", "101", ""]`
（第一次 EXEC：102 priority=5 > 101 的 2 → 102 胜；第二次 EXEC：103 与 102 已跑完的池子里只剩
103(5,30) vs 101(2,100) → 103 胜；第三次剩 101；第四次池子空 → `""`。）

**例 2（Part2，重复 id 抑制 + Part1 的"未执行前重复 add 替换"）**
```
ADD a 1 0
ADD a 5 10
EXEC
ADD a 9 0
EXEC
```
→ `["a", ""]`
（第一次 add a(1,0) 被第二次 add a(5,10) 替换，此时池子只有一个 a；第一次 EXEC 选中 a 并标记为
已执行；第二次 `ADD a 9 0` 发生在 a 已执行之后，是无操作；第二次 EXEC 池子为空 → `""`。）

**例 3（Part2，未执行前重复 add 是"替换"，执行后重复 add 是"无操作"）**
```
ADD x 1 0
ADD y 1 1
ADD x 9 5
EXEC
ADD x 100 0
EXEC
EXEC
```
→ `["x", "y", ""]`
（`ADD x 9 5` 在 x 还没执行时替换了 x 的 `(priority, timestamp)`；第一次 EXEC 时候选是
`x(9,5)` 与 `y(1,1)`，x 胜出并被标记为已执行；`ADD x 100 0` 发生在 x 已执行之后，是无操作
（即便 priority=100 看起来"应该"很抢眼，也不会让 x 复活）；第二次 EXEC 候选只剩 `y(1,1)`，选中
y；第三次 EXEC 池子为空 → `""`。）

**例 4（Part4，`SNAPSHOT` 前后行为不可区分）**
```
ADD a 1 0
ADD b 5 0
EXEC
SNAPSHOT
ADD c 9 0
EXEC
EXEC
```
→ `["b", "c", "a"]`
（`SNAPSHOT` 发生在 b 已执行、a 仍待执行之后；重建出的新实例必须"记得" b 已经执行过（哪怕后面
再 `ADD b ...` 也不会复活）、a 仍待执行；`ADD c 9 0` 和两次 `EXEC` 在新实例上跑，结果必须和"从未
发生过 SNAPSHOT、所有操作在同一个实例上连续执行"完全一致。）

## 边界清单
- 空池子 `execute()` → `""`；构造后立刻 `execute()` 不抛异常
- 单任务；priority 全部相同（纯 timestamp 排序）；timestamp 也相同（纯 id 字典序）
- 同一 id 在未执行前被 `add` 多次（替换语义）；同一 id 在执行后再 `add`（无操作，`execute()` 永
  远不会再选中它）
- id 是数字样式的字符串（`"9"` vs `"10"`）时按**字典序**而非数值比较（`"10" < "9"`）——这是刻意
  的陷阱，problem.md 与测试都显式验证
- 负 priority、负 timestamp 合法且参与比较
- `replay([])` 得到一个空调度器；`replay(log)` 之后立即 `execute()` 与原实例在同一时刻 `execute()`
  的结果一致
- 10^5 次 `add`/`execute` 混合调用在 2s 预算内完成（堆结构，不能用线性扫描）

## 并发追问
1. "两个线程同时 `execute()`，会不会都选中同一个任务？" —— 期望候选人指出"选中"必须和"标记已
   执行"在同一把锁内完成，否则会有 check-then-act 竞态；本题 Part3 的测试直接用多线程验证"不会
   返回同一个已判定执行过的 id"。
2. "能不能用无锁结构（比如 `heapq` + CAS）替代全局锁来提升吞吐？" —— 期望候选人讨论"标记已执行"
   这一步天然需要互斥，无锁堆本身不难，但"弹出即视为已执行"这个语义要求弹出和标记必须原子，纯
   无锁实现需要类似 `compare_and_pop`，Python 里没有原生支持，通常还是退回到锁。
3. "持久化的 `replay` 在并发场景下怎么保证日志顺序与实际执行顺序一致？" —— 期望候选人提出"日志
   写入也要在同一把锁内，按临界区顺序追加"，否则重放出来的调度器可能和原实例分叉。

## 变体
- base 版（整数 id，空池返回 `-1`）与 duplicate 版（字符串 id，空池返回 `""`）在来源里是同一道
  onsite 题的两个 part，本题按"字符串 id 统一"的方式合并（见上方"改写说明"）。
- 一处一手报告把这道题和 cron scheduler（od05）的持久化追问放在同一次面试的延伸讨论里，说明
  "调度器 + 持久化"是 Snowflake 面试官偏好的组合追问，不是巧合。

## 来源与置信度
- https://www.fastprep.io/problems/snowflake-priority-task-manager （Snowflake, Full-time Onsite,
  Medium；base 版 `add`/`execute`，tie-break：priority → timestamp → 最小 id）
- https://www.fastprep.io/problems/snowflake-priority-task-execution-duplicate-ids （同上，
  duplicate-ID 版，"once any occurrence of an id executes, all other occurrences become
  permanently ineligible"）
- 1point3acres 一手挂经 t.me/s/usinterview/29167（架构与 API 形状交叉印证，见
  `catalog/raw/ood.md` #1、`catalog/CATALOG.md` Table B od01 行）
- 置信度 **HIGH**：两个 fastprep 页面 + 一手挂经三方交叉；Part4 持久化标注**重建**，不算入置信度。

## 考什么
S09 类设计先定 API 契约再讲状态与不变量 · S10 并发正确性（原子 claim、锁粒度）· S11 持久化与恢复
（操作日志 replay）· S08 确定性 tie-break · S19 增量设计（Part1→4 依次加一个能力）· S20 自测试
