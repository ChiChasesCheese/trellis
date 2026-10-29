---
id: uth-java-priorityqueue-2-scheduled
node: java.priorityqueue
type: qa
step: 2
---
## Q
**定时线程池怎么按时间取任务**｜Java · OpenJDK 25

`ScheduledThreadPoolExecutor` 里一堆延迟任务，工作线程怎么知道下一个该跑哪个、要睡多久？

## A
**背景。** 定时线程池里有很多「过一会儿再执行」的任务。线程要随时知道最早到期的是哪个，睡到那个时刻再醒。每次扫全部任务太慢，用堆最合适：堆顶永远是最早到期的。

**结构。** 任务队列 `DelayedWorkQueue` 是数组上的最小堆，按触发时间排序，时间相同按提交序号（`sequenceNumber`）排，先提交的先跑。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<line x1="89.514" y1="45.276" x2="58.486" y2="72.724" stroke-width="1.2" stroke="currentColor"/>
<line x1="110.486" y1="45.276" x2="141.514" y2="72.724" stroke-width="1.2" stroke="currentColor"/>
<line x1="41.1112" y1="94.1879" x2="28.8888" y2="115.812" stroke-width="1.2" stroke="currentColor"/>
<line x1="54.8888" y1="94.1879" x2="67.1112" y2="115.812" stroke-width="1.2" stroke="currentColor"/>
<circle cx="100" cy="36" r="14" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="100" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="48" cy="82" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="152" cy="82" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="152" y="86" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="22" cy="128" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="22" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<circle cx="74" cy="128" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="74" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="214" y="22" width="108" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="268" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">领头线程</text>
<line x1="214" y1="36" x2="120" y2="36" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="120.0,36.0 126.0,33.0 126.0,39.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="268" y="68" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只对堆顶</text>
<text x="268" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">限时等待</text>
<text x="170" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">结点上的数 = 到期时间</text>
<text x="170" y="170" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同为 5 时 先提交的先跑</text>
<text x="170" y="194" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个任务记着自己在堆里的下标</text>
</svg>
```

**细节。**

- 堆顶任务的延迟最小，线程只对堆顶睡眠。
- 每个任务记着自己的 `heapIndex`，取消时不用线性查找，O(log n) 就能从堆中摘掉；默认 `removeOnCancel` 为 `false`，取消的任务要等到期才清除。
- 只有一个领头线程做限时等待，其余线程无限等待。

**为什么。** 堆让取最近到期的任务是 O(1)，插入 O(log n)。`DelayQueue` 也是包着一个 `PriorityQueue`。

**例题：** LC 1834 单线程 CPU

给二维数组 `tasks`，`tasks[i] = [入队时间, 处理时长]`。单线程 CPU 空闲且有任务已入队时，选处理时长最短的（并列选下标最小的），开始后必须执行完。返回 CPU 处理任务的下标顺序，`n <= 10^5`。例：`[[1,2],[2,4],[3,2],[4,1]]` 返回 `[0,2,3,1]`。

```python
import heapq

def get_order(tasks: list[list[int]]) -> list[int]:
    n = len(tasks)
    order_by_enqueue = sorted(range(n), key=lambda i: tasks[i][0])
    order: list[int] = []
    ready: list[tuple[int, int]] = []
    clock = 0
    pointer = 0
    while len(order) < n:
        while pointer < n and tasks[order_by_enqueue[pointer]][0] <= clock:
            i = order_by_enqueue[pointer]
            heapq.heappush(ready, (tasks[i][1], i))
            pointer += 1
        if not ready:
            clock = tasks[order_by_enqueue[pointer]][0]
            continue
        processing_time, i = heapq.heappop(ready)
        clock += processing_time
        order.append(i)
    return order
```
