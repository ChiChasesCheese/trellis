---
id: uth-os-net-scheduler-3-eevdf
node: os-net.scheduler
type: qa
step: 3
---
## Q
**EEVDF：先合格再比截止时间**｜Linux · 内核 6.6 起

6.6 起的 EEVDF 比 CFS 多了什么？想要低延迟的任务怎么优先上 CPU？

## A
**背景。** 只按 `vruntime` 排队，公平是公平，却没法表达“我要低延迟”：交互任务想尽快跑一小段，而不是多拿份额。EEVDF 给每个任务一个虚拟截止时间 `deadline = vruntime + slice / 权重`（`slice` 是它请求的一次运行时长）。选择分两步：先筛出“合格”的任务（eligible，还被系统欠着 CPU，也就是 `vruntime` 不超过全体的平均值），再从合格者里选截止最早的。

**结构。** 仍是红黑树，按 `deadline` 排序；每个节点还记着自己子树里最小的 `vruntime`（增强红黑树）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="16" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" font-weight="bold">A</text>
<rect x="80" y="46" width="200" height="16" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<line x1="280" y1="43" x2="280" y2="65" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="16" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" font-weight="bold">B</text>
<rect x="120" y="88" width="120" height="16" rx="2" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<line x1="240" y1="85" x2="240" y2="107" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="16" y="142" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" font-weight="bold">C</text>
<rect x="200" y="130" width="26" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<line x1="226" y1="127" x2="226" y2="149" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="170" y1="26" x2="170" y2="156" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">V 平均</text>
<text x="286" y="58" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">合格</text>
<text x="246" y="100" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">选中</text>
<text x="232" y="142" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">不合格 但截止最早</text>
<text x="20" y="178" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">左端 vruntime 右端 deadline</text>
<text x="20" y="194" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">先看合格 再取最早的截止</text>
</svg>
```

**细节。**

- 靠子树里的最小 `vruntime` 跳过没有合格节点的整棵子树，挑选仍是 O(log n)
- 默认请求时长 `sysctl_sched_base_slice` 是 0.7 ms（再按 CPU 数缩放），任务可以用 `sched_setattr()` 要更短的

**为什么。** 短 `slice` 的截止时间更早，延迟敏感的任务无需靠加权重（那会多占 CPU）就能更快被选中。

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
