---
slug: single-threaded-cpu
---
## Q
**LC 1834 单线程 CPU**｜Medium

任务 `[入队时间, 执行时间]`，单线程 CPU 空闲时从已入队任务中选执行时间最短的（并列选下标小的），做完才能选下一个。返回执行顺序。

## A
**一句话。** 事件模拟加最小堆：任务按入队时间排序，每次空闲时把已到达的全部入堆 `(执行时间, 下标)`，弹堆顶执行。

```python
def get_order(tasks):
    n = len(tasks)
    order = sorted(range(n), key=lambda i: tasks[i][0])
    heap, res = [], []
    t = p = 0                    # 当前时刻；下一个未入队任务的位置
    while len(res) < n:
        if not heap and t < tasks[order[p]][0]:
            t = tasks[order[p]][0]       # 空闲：时间跳到下一个到达
        while p < n and tasks[order[p]][0] <= t:
            i = order[p]
            heapq.heappush(heap, (tasks[i][1], i))
            p += 1
        cost, i = heapq.heappop(heap)    # 最短优先，并列下标小
        t += cost
        res.append(i)
    return res
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 堆空时不跳时间：`[[1,1],[100,1]]` 的 `heappop` 抛 `IndexError`。
- 堆键写成 `(执行时间, 入队时间)`：`[[3,2],[1,4],[2,2]]` 得 `[1,2,0]`，应为 `[1,0,2]`。
- 入堆条件写成 `<`：恰好在完成那刻到达的任务也要参与选择。

**追问。**
- 有 `k` 个 CPU？：再加一个堆存各 CPU 空闲时刻，每次取最早空闲的。
- 允许抢占（最短剩余时间优先）？：事件改为「下一个到达」与「当前任务完成」取更早者，到达时把当前任务的剩余时间放回堆。

**同模式。** LC 253 会议室 II、LC 621 任务调度器、LC 759 员工空闲时间、LC 295 数据流的中位数
