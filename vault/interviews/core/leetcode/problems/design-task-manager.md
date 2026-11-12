---
slug: design-task-manager
---
## Q
**LC 3408 设计任务管理器**｜Medium

设计 `TaskManager`：`add`、`edit`（改优先级）、`rmv`、`execTop`（执行并删除优先级最高、并列取 `taskId` 最大的任务，返回其 `userId`，无任务返回 `-1`）。

## A
**一句话。** 大根堆加字典（真实状态）：`edit`、`rmv` 只改字典，弹出时丢弃过期条目（懒删除）。

```python
class TaskManager:
    def __init__(self, tasks):
        self.info = {}    # taskId -> (userId, 当前优先级)
        self.heap = []    # (-优先级, -taskId)
        for u, t, p in tasks:
            self.add(u, t, p)

    def add(self, userId, taskId, priority):
        self.info[taskId] = (userId, priority)
        heappush(self.heap, (-priority, -taskId))

    def edit(self, taskId, newPriority):
        u, _ = self.info[taskId]
        self.info[taskId] = (u, newPriority)
        # 旧条目留在堆里，弹出时再丢弃
        heappush(self.heap, (-newPriority, -taskId))

    def rmv(self, taskId):
        del self.info[taskId]

    def execTop(self):
        while self.heap:
            np_, nt = heappop(self.heap)
            t = -nt
            # 有效 = 任务还在，且优先级与当前一致
            if t in self.info and self.info[t][1] == -np_:
                return self.info.pop(t)[0]
        return -1
```

**复杂度。** 时间 `add`、`edit`、`execTop` 均摊 `O(log n)`，`rmv` 为 `O(1)`，空间 `O(操作总数)`。

**易错点。**
- 只校验优先级、不校验任务还在：`rmv(101)` 后旧条目被当成有效，`execTop` 返回 `1`，应为 `-1`。
- 只校验任务存在、不比较优先级：`edit(102,8)` 后旧的高优先级条目仍有效，错误先执行 102。
- 堆键写成 `(-priority, taskId)`：并列时取了 `taskId` 最小的。

**追问。**
- 并列时改成先加入先执行？：堆键换成 `(-优先级, 加入序号)`。
- 为什么不直接从堆里删？：`heapq` 不支持按值删除，懒删除让 `rmv` 是 `O(1)`。

**同模式。** LC 146 LRU 缓存、LC 295 数据流的中位数、LC 1845 座位预约管理系统、LC 2034 股票价格波动
