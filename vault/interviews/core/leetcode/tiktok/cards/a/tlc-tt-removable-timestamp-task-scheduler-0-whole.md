---
id: tlc-tt-removable-timestamp-task-scheduler-0-whole
node: a.tt-removable-timestamp-task-scheduler
type: qa
---
## Q
**可删除任务的时间戳调度器（popTask）**｜Medium · 近一年被问：美国 1 次、国内 0 次 · 最近 2026-08-20（面试记录）

实现一个任务调度器：`addTask(taskId, timestamp)` 加入任务；`removeTask(taskId)` 删除一个尚未被取走的任务；`popTask(num)` 返回时间戳最早的 `num` 个任务，并把它们从调度器中移除。时间戳相同的任务按 `taskId` 的字典序排先后（确定性）。约定：`popTask` 在任务不足 `num` 个时返回全部剩余任务；对已存在的 `taskId` 再次 `addTask` 视为更新它的时间戳；`removeTask` 返回是否真的删除了任务。`taskId` 是字符串，`timestamp` 是整数，操作总数不超过 `10^5`。例：依次加入 `(a,5)`、`(b,3)`、`(c,3)`，`popTask(2)` → `['b','c']`，再 `popTask(2)` → `['a']`，再 `popTask(2)` → `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 最小堆 `(timestamp, taskId)` 加一个字典 `alive`（任务 → 当前时间戳）做懒删除（lazy deletion）：`removeTask` 只改字典；`popTask` 弹出堆顶时，条目与字典不符就丢弃，相符就取走并从字典删除。每个条目最多进出堆一次，摊还 `O(log n)`。

**识别。** 「总是取最早的」是优先队列；「还能删除中间的任务」是堆的弱点，堆不支持按值删除；「并列要确定」说明比较键里要带 `taskId`。堆加懒删除是最小改动，需要严格删除时再换有序集合。

**推导。** 暴力：任务放列表，每次 `popTask` 排序取前 `num` 个，`O(n log n)` 一次；堆加真删除要先线性找到位置，`O(n)` → 浪费：删除并不需要立刻让堆「干净」，只要弹出时不返回已删除的任务就行 → 洞察：把删除推迟到弹出：`alive[taskId] = timestamp` 记录「这个任务当前有效的时间戳」，堆里条目 `(ts, id)` 有效当且仅当 `alive.get(id) == ts`；更新时间戳时旧条目的 `ts` 不再匹配，自动失效。

```python
import heapq


class TaskScheduler:
    def __init__(self) -> None:
        self._heap: list[tuple[int, str]] = []      # (timestamp, task_id)：时间戳小者在前，相同时按 task_id 字典序
        self._alive: dict[str, int] = {}            # 仍在调度器里的任务 -> 它当前的时间戳

    def addTask(self, task_id: str, timestamp: int) -> None:
        self._alive[task_id] = timestamp            # 同一个 id 重复加入视为改时间戳
        heapq.heappush(self._heap, (timestamp, task_id))

    def removeTask(self, task_id: str) -> bool:
        return self._alive.pop(task_id, None) is not None   # 只改字典，堆里的旧条目等弹出时再丢（懒删除）

    def popTask(self, num: int) -> list[str]:
        out: list[str] = []
        while self._heap and len(out) < num:
            timestamp, task_id = heapq.heappop(self._heap)
            if self._alive.get(task_id) != timestamp:   # 已被删除或已被改过时间戳的旧条目：跳过
                continue
            del self._alive[task_id]                    # popTask 取走即移除
            out.append(task_id)
        return out
```

运行：`(a,5)`、`(b,3)`、`(c,3)` 后 `popTask(2)` → `['b', 'c']`，`popTask(2)` → `['a']`，`popTask(2)` → `[]`；加入 `a,b,c,d(9)`，`removeTask("b")` → `True`，`removeTask("zzz")` → `False`，`popTask(2)` → `['c', 'a']`，`popTask(5)` → `['d']`，`popTask(1)` → `[]`；`x@1` 加入再删除，再以 `x@7`、`y@4` 加入，`popTask(2)` → `['y', 'x']`。

**复杂度。** `addTask` 为 `O(log n)`；`removeTask` 为 `O(1)`；`popTask(k)` 摊还 `O((k + 被丢弃的旧条目数) * log n)`，每个条目只会被丢弃一次，总成本不超过 `O(操作数 * log n)`；空间 `O(n)`，包含尚未被清理的旧条目。

**易错点。**
- `popTask` 只查看不移除：`(a,5)`、`(b,3)`、`(c,3)` 连续两次 `popTask(2)` 都得到 `['b','c']`，正确第二次是 `['a']`。
- 用「已删除 id 集合」做懒删除：`x@1` 加入、删除，再以 `x@7` 加入，`popTask(1)` 会因为 `x` 在已删除集合里而返回 `[]`，正确是 `['x']`。要校验的是「条目的时间戳等于当前有效时间戳」，不是 id 是否出现过。
- 并列不确定：只按时间戳排序时，相同时间戳的先后取决于插入顺序；元组 `(timestamp, task_id)` 的比较天然把 `task_id` 当第二关键字。

**追问。**
- 堆里积压很多已失效的条目：当堆长度超过存活任务数的两倍时，用 `alive` 重建并 `heapify`，让内存回到 `O(存活任务数)`。
- 要求 `removeTask` 严格 `O(log n)` 且不留残余：用有序集合（平衡树、跳表）；标准库没有，常用第三方 `sortedcontainers.SortedList`。
- 增加 `peekTask()` 或 `size()`：`size` 就是 `len(alive)`，`peek` 要先弹掉堆顶的失效条目再查看。

**同模式。** LC 1834 单线程 CPU、LC 2336 无限集中的最小数字、LC 703 数据流中的第 K 大元素、LC 355 设计推特。
