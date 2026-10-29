---
id: uth-compose-indexed-heap-5-removable-scheduler
node: compose.indexed-heap
type: qa
step: 5
---
## Q
**借到面试题：可删除任务的调度器**｜Java ScheduledThreadPoolExecutor · JDK 21

面试要你实现 `addTask`、`removeTask`、`popTask(num)`：按时间戳取最早的任务，还要能删除任务。怎样用同一个骨架做？

## A
**结构。** 同一个骨架：堆存 `(时间戳, taskId)`，再配一张字典。字典里存什么，决定两种做法：

- 存「任务 → 当前时间戳」（懒删除）：`removeTask` 只改字典，弹出堆顶时和字典对不上的旧条目直接丢。删除 O(1)，弹出摊还 O(log n)，堆里暂留垃圾。
- 存「任务 → 堆下标」（带下标）：`removeTask` 真正从堆里摘掉，O(log n)，没有垃圾；代价是要手写堆，每次交换都更新下标。

**为什么。** 面试里先写懒删除：`heapq` 现成，改动最小。追问「要严格删除、不留残余」时，再换成带下标的堆。

**坑。** 懒删除只记「已删除的 id」会出错：同一个 id 删除后又重新加入，旧条目会被误认成新的。要比对的是「条目的时间戳等于当前有效时间戳」。

**例题：** 可删除任务的时间戳调度器（`popTask`）

`addTask(taskId, timestamp)` 加入任务（已存在则更新时间戳）；`removeTask(taskId)` 删除未被取走的任务，返回是否删除成功；`popTask(num)` 返回时间戳最早的 `num` 个任务并移除，时间戳相同按 `taskId` 字典序。例：加入 `(a,5)`、`(b,3)`、`(c,3)`，`popTask(2)` → `['b','c']`，再 `popTask(2)` → `['a']`。

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
