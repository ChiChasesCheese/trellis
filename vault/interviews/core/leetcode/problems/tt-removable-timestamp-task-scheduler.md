---
slug: tt-removable-timestamp-task-scheduler
---
## Q
**可删除任务的时间戳调度器（popTask）**｜Medium

实现调度器：`addTask(taskId, timestamp)` 加入任务（已存在则更新时间戳），`removeTask(taskId)` 删除未被取走的任务并返回是否删除成功，`popTask(num)` 取走并返回时间戳最早的 `num` 个任务（同时间戳按 `taskId` 字典序，不足则返回全部）。

## A
**一句话。** 最小堆 `(timestamp, taskId)` 加字典 `alive` 做懒删除：`removeTask` 只改字典，`popTask` 弹出时与字典对不上的旧条目直接丢弃。

```python
class TaskScheduler:
    def __init__(self):
        self.heap = []      # (timestamp, task_id)
        self.alive = {}     # 存活任务 -> 当前时间戳

    def addTask(self, task_id, timestamp):
        self.alive[task_id] = timestamp   # 重复加入即改时间戳
        heapq.heappush(self.heap, (timestamp, task_id))

    def removeTask(self, task_id):
        return self.alive.pop(task_id, None) is not None

    def popTask(self, num):
        out = []
        while self.heap and len(out) < num:
            ts, tid = heapq.heappop(self.heap)
            if self.alive.get(tid) != ts:   # 旧条目：跳过
                continue
            del self.alive[tid]
            out.append(tid)
        return out
```

**复杂度。** 时间 `addTask` 为 `O(log n)`、`removeTask` 为 `O(1)`、`popTask` 摊还 `O(log n)` 每个，空间 `O(n)`。

**易错点。**
- `popTask` 只查看不移除：连续两次 `popTask(2)` 得到相同结果。
- 用「已删除 id 集合」做懒删除：`x@1` 加入、删除，再以 `x@7` 加入，`popTask(1)` 返回 `[]`，应为 `['x']`；要校验时间戳是否等于当前有效值。

**追问。**
- 堆里积压很多失效条目？：堆长超过存活数两倍时用 `alive` 重建并 `heapify`。
- 要求 `removeTask` 严格 `O(log n)` 且不留残余？：用有序集合（平衡树、`SortedList`）。

**同模式。** LC 1834 单线程 CPU、LC 703 数据流中的第 K 大元素、LC 355 设计推特
