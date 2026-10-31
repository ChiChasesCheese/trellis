---
id: tlc-design-task-manager-0-whole
node: c.design-task-manager
type: qa
---
## Q
**LC 3408 设计任务管理器**｜Medium · LC TikTok 全时段热度 26/100

设计 `TaskManager`：`TaskManager(tasks)` 用 `[userId, taskId, priority]` 列表初始化；`add(userId, taskId, priority)` 给用户添加一个优先级为 `priority` 的任务（保证 `taskId` 不在系统中）；`edit(taskId, newPriority)` 更新已存在任务的优先级；`rmv(taskId)` 删除任务；`execTop()` 执行所有用户任务中优先级最高的一个（并列时取 `taskId` 最大的），执行后任务从系统删除，返回它所属的 `userId`，没有任务返回 `-1`。一个用户可以有多个任务。`1 <= tasks.length <= 10^5`，`0 <= userId, taskId <= 10^5`，`0 <= priority, newPriority <= 10^9`，四种操作总次数不超过 `2 * 10^5`，输入保证 `taskId` 合法。例：初始 `[[1,101,10],[2,102,20],[3,103,15]]`；`add(4,104,5)`；`edit(102,8)`；`execTop()` → `3`；`rmv(101)`；`add(5,105,15)`；`execTop()` → `5`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用大根堆按 `(优先级, taskId)` 取最大，用字典 `taskId -> (userId, 优先级)` 记录真实状态；`edit` 和 `rmv` 不去堆里找，只改字典，弹出时再丢弃过期条目（懒删除）。

**识别。** 「动态取最大值，且元素会被修改或删除」是堆 + 懒删除的典型场景：堆不支持按值删除或改键，懒删除把这些操作都变成 `O(log n)` 的追加。

**推导。** 暴力：每次 `execTop` 扫描全部任务取最大，`O(n)`，`2 * 10^5` 次操作会超时。洞察：把 `edit` 当作「插入一个新条目」，旧条目变成过期；弹出堆顶时用字典校验条目是否还有效（任务存在且优先级一致），无效就继续弹。Python 只有小根堆，所以存 `(-priority, -taskId)`。

```python
from heapq import heappop, heappush


class TaskManager:
    def __init__(self, tasks: list[list[int]]) -> None:
        self.info: dict[int, tuple[int, int]] = {}      # taskId -> (userId, 当前优先级)，系统里「真实存在」的任务
        self.heap: list[tuple[int, int]] = []           # (-优先级, -taskId)：堆顶就是优先级最高、同级 taskId 最大
        for user_id, task_id, priority in tasks:
            self.add(user_id, task_id, priority)

    def add(self, userId: int, taskId: int, priority: int) -> None:
        self.info[taskId] = (userId, priority)
        heappush(self.heap, (-priority, -taskId))

    def edit(self, taskId: int, newPriority: int) -> None:
        user_id, _ = self.info[taskId]
        self.info[taskId] = (user_id, newPriority)
        heappush(self.heap, (-newPriority, -taskId))    # 旧条目留在堆里不删，等弹出时再识别（懒删除）

    def rmv(self, taskId: int) -> None:
        del self.info[taskId]                           # 同样只改 info，堆里的旧条目以后会被丢弃

    def execTop(self) -> int:
        while self.heap:
            neg_priority, neg_task = heappop(self.heap)
            task_id = -neg_task
            # 条目有效 <=> 任务还在系统里，且堆里记的优先级就是它当前的优先级
            if task_id in self.info and self.info[task_id][1] == -neg_priority:
                return self.info.pop(task_id)[0]        # 执行后从系统中删除，返回所属用户
        return -1
```

运行：按示例，`execTop()` 依次返回 `3`、`5`；只有一个任务时执行一次得到 `1`，再执行返回 `-1`。

**复杂度。** `add` / `edit` 均摊 `O(log n)`，`rmv` `O(1)`，`execTop` 均摊 `O(log n)`（每个条目最多入堆一次、出堆一次）；空间 `O(操作总数)`。

**拓展优化。**
- 堆里积累的过期条目过多时（比如大量 `edit`），可以在过期比例超过一半时重建堆，控制空间。
- 需要按用户查询任务时，再维护 `userId -> 任务集合` 的字典。

**易错点。**
- `edit` 后优先级相同的旧条目：把优先级改成原值会产生两个都「有效」的条目，第一个被执行后，第二个因 `taskId` 不在 `info` 中被丢弃，不会重复执行。
- 只检查任务是否存在而不比较优先级：`edit` 之后的旧条目（优先级更高）仍会被认为有效，`edit(102, 8)` 后 `execTop()` 会错误地先执行 102 而返回 `2`，应为 `3`。
- 堆键写成 `(-priority, taskId)`：并列时会取 `taskId` 最小的，题目要求最大。

**追问。**
- 并列时的规则变成「先加入先执行」：堆键换成 `(-priority, 加入序号)`。
- 多线程使用：加锁；或每个用户一个堆再加一个全局堆。

**同模式。** LC 146 LRU 缓存、LC 295 数据流的中位数、LC 1845 座位预约管理系统、LC 2034 股票价格波动、LC 1912 设计电影租借系统。
