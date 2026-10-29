---
id: uth-os-net-scheduler-1-rbtree
node: os-net.scheduler
type: qa
step: 1
---
## Q
**调度器怎么挑下一个任务**｜Linux · 内核 6.5 与 7.3

成千上万个可运行任务排队，Linux 怎么在 O(log n) 内挑出下一个上 CPU 的？

## A
**背景。** 多个任务抢一个 CPU，调度器要回答“下一个让谁跑”。公平的想法：谁到目前为止拿到的 CPU 时间最少，就让谁跑。给每个任务记一个“已获得的服务量”，叫虚拟运行时间 `vruntime`，每次取最小的。数据结构要同时支持取最小、插入、删除：扫一遍是 O(n)，有序数组插入慢，红黑树正合适。

**结构。** 红黑树（保持平衡的有序二叉树）：可运行任务按 `vruntime` 放进树里，调度器取最左节点（最小的）。例：树里有 20、30、40……的任务，最左的 20 先上 CPU，跑一会儿它的 `vruntime` 变大，再插回树里。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<line x1="170" y1="45" x2="110" y2="55" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="170" y1="45" x2="230" y2="55" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="110" y1="81" x2="80" y2="93" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="110" y1="81" x2="140" y2="93" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="230" y1="81" x2="200" y2="93" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="230" y1="81" x2="260" y2="93" fill="none" stroke="currentColor" stroke-width="1.2"/>
<circle cx="170" cy="32" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">50</text>
<circle cx="110" cy="68" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110" y="72" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">30</text>
<circle cx="230" cy="68" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230" y="72" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">80</text>
<circle cx="80" cy="106" r="13" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="80" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">20</text>
<circle cx="140" cy="106" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="140" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">40</text>
<circle cx="200" cy="106" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="200" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">70</text>
<circle cx="260" cy="106" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">90</text>
<text x="14" y="20" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">键 = vruntime</text>
<line x1="60" y1="148" x2="71.6295" y2="126.402" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M74.0,122.0 L73.7,129.5 L67.9,126.4 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="20" y="164" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">最左节点 下一个上 CPU</text>
<text x="20" y="182" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">缓存了指针 取走 O(1)</text>
</svg>
```

**细节。**

- 6.5 的 CFS（完全公平调度器）以 `vruntime` 为键，最左 = 跑得最少、最“亏欠”的任务
- 6.6 起新的调度算法 EEVDF 取代 CFS，树还是红黑树，键换成虚拟截止时间 `deadline`
- 树用 `rb_root_cached` 缓存了最左节点，取下一个是 O(1)，入队出队 O(log n)

**为什么。** 一棵按“已获得服务”排序的树，替换了旧版按优先级分桶的数组队列，不再需要靠启发式猜哪个任务是交互式的。

**例题：** LC 1834 单线程 CPU（同类：LC 253 会议室 II）

`tasks[i] = [enqueueTime, processingTime]`。单线程 CPU 空闲时，从已经入队的任务里选执行时间最短的（并列选下标小的）执行，做完再选下一个。返回任务的执行顺序。

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
