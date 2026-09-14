# od01 · Priority Task Scheduler：优先队列类设计，练的是"惰性删除 + 原子标记"

> [!tldr]
> - **Part 4（`snapshot`/`replay` 持久化）是 (reconstructed)**：来源只把"持久化/崩溃恢复"列为 fastprep 追问列表里的一个方向，没有给出具体 API，本题的 `snapshot`/`replay` 设计是本仓库补全的
> - 这题考的是：一个任务调度器类，`add` 入队、`execute` 按 (priority desc, timestamp asc, id asc) 弹出最优任务，重复 id 一旦执行过就永久失效
> - 三步套路：先把四个方法的契约和不变量写清楚 → Part 1/2 用"堆 + 版本号惰性删除"解决"重复 add 替换"和"执行后失效" → Part 3 把"扫描+标记"锁进一个临界区 → Part 4 用操作日志重放实现持久化
> - 最值得带走的一个模式：**堆不支持 O(1) 更新/删除某个元素，用一个版本号让旧堆项自然过期**——不需要物理删除，弹出时发现版本号不匹配就跳过

## 类设计先定契约
```python
class TaskScheduler:
    def __init__(self) -> None: ...
    def add(self, task_id: str, priority: int, timestamp: int) -> None: ...
    def execute(self) -> str:
        """弹出并返回当前池子里优先级最高的可执行任务 id。
        tie-break: priority 更大者胜 -> timestamp 更早者胜 -> task_id 字典序更小者胜。
        池子为空返回 ""。"""
    def snapshot(self) -> list[str]:
        """返回从构造到现在的完整操作日志，用于 replay 重建等价实例。"""
    @classmethod
    def replay(cls, log: list[str]) -> "TaskScheduler":
        """从空状态重放日志，重建一个『未来行为等价』的新实例（不要求内部结构一致）。"""
```
**不变量（写代码前先想清楚）**：
1. 一个 `task_id` 只要还没被 `execute()` 选中过，重复 `add` 就是"替换"——新的 `(priority, timestamp)`
   覆盖旧的。
2. 一个 `task_id` 一旦被 `execute()` 选中过，就**永久**失效——队列里的残留副本、之后任何新的 `add`，
   都必须是无操作，`execute()` 也永远不会再选中它。
3. "选中并标记为已执行"必须是一个原子操作，两次并发 `execute()` 不能返回同一个已判定执行过的 id。

## 1. 题目在说什么（人话版）
`add(task_id, priority, timestamp)` 把任务扔进队列；`execute()` 从队列里挑"最该跑"的（priority 越大
越优先，同 priority 比 timestamp 越早越优先，再同则比 id 字典序）弹出并返回它的 id。重复 id 不是去重，
而是"竞态"——同一个逻辑任务被提交好几次，只要**任意一次**跑完，其余的（不管是队列里排队中的还是未来
才提交的）就永久作废。

三行小例子：
```
ADD a 1 0
ADD a 5 10   # 替换：还没执行，新值覆盖旧值 (priority=5, ts=10)
EXEC         # 选中 a，标记为已执行
ADD a 9 0    # 无操作：a 已执行，任何后续 add 都不会让它复活
EXEC         # 池子为空 -> ""
```

## 2. 读题：把文字变成模型
- **实体**：任务（`task_id`、`priority`、`timestamp`）、"已执行"状态。
- **输入长什么样**：`main()` 命令流 `ADD <id> <priority> <timestamp>` / `EXEC` / `SNAPSHOT`。
- **输出要什么**：`EXEC` 输出一行结果（id 或空行）；`ADD`/`SNAPSHOT` 无输出。
- **状态**：一个"当前候选池"（未执行、最新一次 add 的 `(priority, timestamp)`）、一个"已执行 id 集合"。
- **一句话建模**：这是一个 **带条件淘汰的优先队列**——用堆维护候选，但堆本身不支持"这个 id 已经作废"
  或"这个 id 的值被替换了"这种原地更新，需要额外一层"版本号 + 已执行集合"来处理淘汰。

> [!note] 为什么选这个数据结构
> Python 的 `heapq` 只支持插入和弹出最小值，不支持"删除某个特定元素"或"更新某个元素的排序 key"。
> 直接为每次 `add` 都物理修改堆会退化成 O(n)。解法是**惰性删除**：给每个 `task_id` 维护一个版本号，
> 每次重复 `add` 就递增版本号并 push 一个新堆项；`execute()` 弹出堆顶时，检查这个堆项的版本号是否还是
> "当前最新"，或者这个 id 是否已经在 `_executed` 集合里——只要有一条不满足就说明这个堆项是"过期垃圾"，
> 丢弃继续弹下一个，不需要真的从堆里删除它。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **接口先行**：先把 `__init__` 要存的字段列出来（不写 body）：堆、版本号字典、已执行集合、操作日志、
   一把锁。再把四个方法的签名和 docstring 过一遍。
2. **Part 1 最小可用**：`add` 往堆里 push `(-priority, timestamp, task_id, version)`；`execute` 弹堆顶
   直接返回。先不管重复 id 和已执行判断，用官方样例 1 验证 tie-break 顺序对不对（注意 `-priority`
   让"越大越优先"变成堆的"越小越优先"）。
3. **Part 2 叠加**：`add` 里先查 `task_id in self._executed`，是就直接跳过（无操作）；否则递增版本号
   再 push。`execute` 弹出堆顶后检查"是否已执行"或"版本号是否过期"，不满足就继续弹下一个，直到找到
   一个有效的或堆空。
4. **Part 3 叠加**：把 `add`/`execute` 各自的核心逻辑包进同一把 `threading.Lock`，保证"扫描候选 + 标记
   已执行"是一个原子操作。
5. **Part 4 叠加**：`add`/`execute` 每次调用都往一个 `_log` 列表追加一行（格式与 `main()` 的输入行
   一致）；`snapshot()` 返回这份日志；`replay(log)` 从空实例开始重新跑一遍日志里的每个操作。

## 4. 代码怎么组织
```
TaskScheduler.__init__          # 堆、版本号字典、已执行集合、操作日志、锁
add(task_id, priority, timestamp)   # 锁内：已执行则跳过，否则递增版本号 push 堆
execute() -> str                     # 锁内：弹堆顶，版本号/已执行校验，无效则继续弹
snapshot() -> list[str]              # 锁内：返回操作日志副本
replay(log) -> TaskScheduler         # classmethod：从空实例重放日志
main(stdin, stdout)                   # 解析 ADD/EXEC/SNAPSHOT 命令流，分发
```
所有对内部状态的读写都收敛到 `add`/`execute` 两个方法内部，`snapshot`/`replay` 不直接碰堆或版本号
——它们只操作"操作日志"这个更高层的表示，这样持久化逻辑和核心调度逻辑完全解耦。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
class TaskScheduler:
    def __init__(self):
        self._heap = []              # (-priority, ts, task_id, version)
        self._versions = {}          # task_id -> 最新版本号
        self._executed = set()       # 已永久执行过的 task_id
        self._log = []               # 操作日志，用于 snapshot/replay
        self._lock = threading.Lock()

    def add(self, task_id, priority, timestamp):
        with self._lock:
            self._log.append(f"ADD {task_id} {priority} {timestamp}")
            if task_id in self._executed:
                return                            # 已执行，永久无操作
            version = self._versions.get(task_id, 0) + 1
            self._versions[task_id] = version      # 递增版本号，旧堆项自然过期
            heapq.heappush(self._heap, (-priority, timestamp, task_id, version))

    def execute(self):
        with self._lock:
            while self._heap:
                neg_p, ts, task_id, version = heapq.heappop(self._heap)
                if task_id in self._executed or self._versions.get(task_id) != version:
                    continue                        # 过期堆项：已执行 或 被更新的 add 取代
                self._executed.add(task_id)          # 选中并标记，原子完成
                self._log.append("EXEC")
                return task_id
            self._log.append("EXEC")
            return ""

    def snapshot(self):
        with self._lock:
            return list(self._log)

    @classmethod
    def replay(cls, log):
        sched = cls()
        for line in log:
            if line == "EXEC":
                sched.execute()
            else:
                _, tid, p, t = line.split()
                sched.add(tid, int(p), int(t))
        return sched
```

## 6. 并发追问怎么答
- **哪把锁、锁什么粒度**：一把锁包住 `add`/`execute` 各自的整个临界区（"检查已执行 + 更新版本号 +
  push 堆"是一段，"弹堆顶 + 校验 + 标记已执行"是另一段），不是细粒度地只锁堆或只锁集合——因为这两步
  必须作为一个整体，否则会有 check-then-act 竞态。
- **哪个操作必须是原子的**：`execute()` 里"判断这个堆项有效"和"把它标记为已执行"必须在同一把锁内，
  否则两个线程可能同时读到"还没执行"，都把同一个 id 标记出去。
- **测试怎么证明原子性**：起多个线程并发调 `add`/`execute`，收集所有 `execute()` 的返回值，断言
  ①非空返回值里没有重复（同一个 id 不会被选中两次）；②所有成功 `add` 且从未被选中的 id，最终必须在
  某次 `execute()` 里出现恰好一次（不丢任务，除非调用次数不够）。
- **能不能用无锁结构**：`heapq` 本身可以无锁并发 push（Python GIL 让单个 `heappush` 原子），但
  "弹出即视为已执行"这个语义要求弹出和标记是一体的，需要类似 `compare_and_pop` 的原语，Python 没有
  原生支持，通常还是退回到锁，这一点可以在追问里直接讲清楚而不用假装能设计出无锁方案。

## 7. 常见跑偏（方法层面，3 条）
- **重复 add 时直接从堆里物理删除旧项**：堆不支持 O(1) 定位任意元素，物理删除需要线性扫描，退化成
  O(n)。用版本号惰性标记过期，让 `execute()` 弹出时自然跳过，才能维持 O(log n)。
- **把"已执行"判断放在 `add` 之外、`execute` 单独维护一份"跳过列表"**：容易和 `_executed` 集合的
  语义脱节，导致 `add` 里的"已执行则无操作"和 `execute` 里的"已执行则跳过"用了两套不一致的判断源。
  统一用同一个 `_executed` 集合。
- **id 是数字字符串时按数值比较**：`"9" < "10"` 是数值直觉，但 `task_id` 是字符串，题目明确要求
  按字典序比较（`"10" < "9"`），这是刻意设置的陷阱，写 tie-break 时要用字符串比较而不是先转 int。

## 自测清单
- 空池子 `execute()` 返回 `""`，不抛异常。
- priority 全部相同（纯 timestamp 排序）、timestamp 也全部相同（纯 id 字典序）。
- 同一 id 执行前重复 add（替换）vs 执行后重复 add（无操作）分别验证。
- id 是 `"9"` vs `"10"` 这种数字样式字符串，验证按字典序而非数值比较。
- `replay([])` 得到空调度器；`replay(log)` 后立即 `execute()` 与原实例同一时刻 `execute()` 结果一致。
- 多线程并发 `add`/`execute`，验证无重复选中、无丢任务。
- 1e5 次 `add`/`execute` 混合调用在 2s 内完成（验证用的是堆而不是线性扫描）。

## 相关题与 skills id
- skills: **S09**（类设计先定 API 契约）· **S10**（并发正确性：原子 claim、锁粒度）· **S11**
  （持久化与恢复：操作日志 replay）· S08（确定性 tie-break）。
- 同族：`od05_cron_scheduler` 也是"调度器 + 持久化"组合追问，一处一手报告把两题的持久化追问放在
  同一次面试里讨论过。
- 练习命令：`python3 loop/mock.py start od01`
