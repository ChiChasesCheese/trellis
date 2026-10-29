---
id: uth-compose-k8s-workqueue-5-interview
node: compose.k8s-workqueue
type: qa
step: 5
---
## Q
**借到面试题：可撤销的任务调度器**｜队列 + 去重集合

任务可以随时撤销、改时间，怎样用"顺序结构 + 一张记真相的表"设计这个调度器？

## A
**背景。** workqueue 里 `queue` 只管顺序，`dirty` 才是真相：谁该处理，以集合为准。"可删除、可改时间的任务调度器"是同一个套路：堆只管顺序，一张字典记每个任务当前有效的时间戳。

| workqueue | 调度器 |
|---|---|
| `dirty`：谁还欠一次处理 | `alive`：任务 → 当前有效的时间戳 |
| `queue`：先后顺序 | 最小堆 `(时间戳, 任务 id)` |
| 重复 `Add` 合并成一份 | 同一 id 再次 `addTask`，旧堆项自动失效 |
| `Get` 时取出 | `popTask` 弹出时与 `alive` 对账，对不上就丢弃 |

**为什么。** 不去堆里找出来删（要 O(n)），只改字典这本账，弹出时再对账，每个条目至多被丢弃一次，摊还 O(log n)。

**坑。** 用"已删除 id 集合"对账会出错：任务 `x` 删除后又以新时间加入，会被误当成已删除。该比较的是堆项的时间戳是否等于字典里的有效值，而不是 id 出没出现过。

**例题：** 可删除任务的时间戳调度器（popTask）

`addTask(taskId, timestamp)` 加入任务（已存在则更新时间戳），`removeTask(taskId)` 删除尚未取走的任务并返回是否删除成功，`popTask(num)` 返回并移除时间戳最早的 `num` 个任务（时间戳相同按 `taskId` 字典序）。例：加入 `(a,5)`、`(b,3)`、`(c,3)`，`popTask(2)` → `['b','c']`，再 `popTask(2)` → `['a']`。

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
