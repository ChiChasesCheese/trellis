---
id: tlc-single-threaded-cpu-4-followup
node: a.single-threaded-cpu
type: qa
step: 4
---
## Q
**LC 1834 单线程 CPU**｜追问

面试官接着问：（1）有 `k` 个 CPU 并行怎么办？（2）任务实时到达（流式），不能预先排序？（3）要求计算平均等待时间？

## A
1. **`k` 个 CPU。** 再加一个小堆 `busy` 存 `(空闲时刻, CPU 编号)`。每次取最早空闲的 CPU：把时间推进到该 CPU 的空闲时刻（或下一个任务的到达时刻，取较晚者），再从任务堆里取最短的任务分给它，并把 `(空闲时刻 + 执行时间, 编号)` 放回 `busy`。复杂度 `O(n log n + n log k)`。
2. **流式到达。** 不需要排序和指针：到达的任务直接 `heappush` 进任务堆；调度循环只在 CPU 空闲时 `heappop`。需要排序的只是离线场景里“把未来任务按时间放进池子”这一步。
3. **平均等待时间。** 等待时间 = 开始执行的时刻 - 到达时刻。循环里弹出任务前的 `t` 就是开始时刻，所以在 `res.append(i)` 旁边累加 `t - tasks[i][0]`，最后除以 `n`：
```python
from heapq import heappop, heappush

def average_wait(tasks: list[list[int]]) -> float:
    n = len(tasks)
    order = sorted(range(n), key=lambda i: tasks[i][0])
    heap: list[tuple[int, int]] = []
    done = p = t = wait = 0
    while done < n:
        if not heap and t < tasks[order[p]][0]:
            t = tasks[order[p]][0]
        while p < n and tasks[order[p]][0] <= t:
            i = order[p]
            heappush(heap, (tasks[i][1], i))
            p += 1
        cost, i = heappop(heap)
        wait += t - tasks[i][0]
        t += cost
        done += 1
    return wait / n
```
这是最短作业优先（SJF，shortest job first）调度，它使平均等待时间最小，代价是长任务可能饥饿。

**Python 提醒**：堆里放元组时，若前面的元素可能相同，后面必须是能比较的值（如下标）；直接放自定义对象或字典，相同键会触发 `TypeError: '<' not supported`。
