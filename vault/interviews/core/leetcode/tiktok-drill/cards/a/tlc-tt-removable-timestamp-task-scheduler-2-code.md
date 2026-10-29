---
id: tlc-tt-removable-timestamp-task-scheduler-2-code
node: a.tt-removable-timestamp-task-scheduler
type: qa
step: 2
---
## Q
**可删除任务的时间戳调度器（popTask）**｜写出 Python 实现

用类实现：`addTask(taskId, timestamp)` 加入任务（同一 `taskId` 再次加入视为更新时间戳）；`removeTask(taskId)` 删除尚未取走的任务并返回是否成功；`popTask(num)` 返回时间戳最早的 `num` 个任务（不足则全部），时间戳相同按 `taskId` 字典序，并把它们移除。`taskId` 为字符串，`timestamp` 为整数，操作总数不超过 `10^5`。

## A
**思路。** 堆里放 `(timestamp, taskId)`，字典 `_alive` 记录每个任务当前有效的时间戳。删除和更新都只改字典；弹出堆顶时，条目的时间戳与字典不符就丢弃，相符才算取走并从字典里删掉。

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

运行：`(a,5)`、`(b,3)`、`(c,3)` 后 `popTask(2)` → `['b', 'c']`，再 `popTask(2)` → `['a']`，再 `popTask(2)` → `[]`；加入 `a@5, b@3, c@3, d@9` 后，`removeTask("b")` → `True`，`removeTask("zzz")` → `False`，`popTask(2)` → `['c', 'a']`，`popTask(5)` → `['d']`，`popTask(1)` → `[]`。

**复杂度。** `addTask` `O(log n)`；`removeTask` `O(1)`；`popTask` 摊还 `O(log n)` 每个返回的任务；空间 `O(n)`，含尚未清理的旧条目。

**写法要点。** `dict.pop(key, None) is not None` 一行完成「存在则删除并返回是否成功」，注意不能写成 `if dict.pop(...)`，因为时间戳可能是 `0`；元组比较让时间戳相同时自然按 `task_id` 排序；`alive.get(id) != timestamp` 同时处理「已删除」（得到 `None`）和「已被更新」（得到另一个时间戳）两种失效；类型注解里堆元素是 `tuple[int, str]`，保证比较时两个字段都可比。
