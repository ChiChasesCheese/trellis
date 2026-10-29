---
id: tlc-single-threaded-cpu-2-code
node: a.single-threaded-cpu
type: qa
step: 2
---
## Q
**LC 1834 单线程 CPU**｜写出 Python 实现

`tasks[i] = [enqueueTime, processingTime]`（`1 <= n <= 10^5`，两个数都在 `1` 到 `10^9`）。单线程 CPU 空闲时从已到达的任务里选执行时间最短的（并列选下标最小），执行完才能选下一个；队列空时保持空闲。返回执行顺序。要求 `O(n log n)`。

## A
**思路。** 下标按到达时间排序；用指针 `p` 把已到达的任务压入堆，堆元素是 `(执行时间, 下标)`。每轮弹出堆顶执行，`t += 执行时间`；堆空时把 `t` 跳到下一个任务的到达时刻。

```python
from heapq import heappop, heappush

def get_order(tasks: list[list[int]]) -> list[int]:
    n = len(tasks)
    order = sorted(range(n), key=lambda i: tasks[i][0])   # 任务下标按入队时间排好
    heap: list[tuple[int, int]] = []                      # (执行时间, 下标)：元组比较天然先时间后下标
    res: list[int] = []
    t = p = 0                                             # t 当前时刻；p 下一个还没入队的任务在 order 里的位置
    while len(res) < n:
        if not heap and t < tasks[order[p]][0]:
            t = tasks[order[p]][0]                        # CPU 空闲且队列空：时间直接跳到下一个任务到达
        while p < n and tasks[order[p]][0] <= t:          # 把此刻已到达的任务全部入堆
            i = order[p]
            heappush(heap, (tasks[i][1], i))
            p += 1
        cost, i = heappop(heap)                           # 取最短的；并列时下标小的先出
        t += cost
        res.append(i)
    return res
```

运行：`[[1,2],[2,4],[3,2],[4,1]]` → `[0, 2, 3, 1]`，`[[7,10],[7,12],[7,5],[7,4],[7,2]]` → `[4, 3, 2, 0, 1]`，`[[5,2]]` → `[0]`，`[[1,1],[100,1]]` → `[0, 1]`。

**复杂度。** 时间 `O(n log n)`：排序 `O(n log n)`，`n` 次 `heappush` 和 `heappop` 各 `O(log n)`；空间 `O(n)`。

**写法要点。**
- `sorted(range(n), key=lambda i: tasks[i][0])` 只排下标，不改动原数组，结果里就是要返回的下标。
- `heapq` 是最小堆，元组 `(cost, i)` 逐项比较：先比执行时间，相同再比下标，不需要自定义比较函数；下标唯一，所以永远不会比到后面不可比较的对象。
- 外层条件写成 `len(res) < n`：`p == n` 且堆非空时仍要继续弹；`if not heap and ...` 保证访问 `order[p]` 时 `p < n`（堆空且未做完，说明还有没入堆的任务）。
- 更紧凑的变体：先 `jobs = sorted((enq, proc, i) for i, (enq, proc) in enumerate(tasks))`，再按元组顺序遍历，不用 `order` 间接索引。
