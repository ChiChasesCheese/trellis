---
id: uth-go-rust-go-scheduler-3-timers
node: go-rust.go-scheduler
type: qa
step: 3
---
## Q
**time.Sleep 的定时器放在哪里**｜Go · 1.27 运行时

成千上万个 `time.After` / `Sleep`，运行时怎么知道下一个该醒的是谁？

## A
**背景。** 运行时每轮只需要知道：最近要触发的定时器是哪个，到点了没有。每次都要“取最小值”，这正是堆（heap）擅长的事：堆顶永远是最小的，取走后整理一下就行。

**结构。** 每个 P 持有一个定时器最小堆，堆顶就是最近要触发的定时器；而且是四叉堆（4-ary heap，每个节点 4 个孩子）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">每个 P 一个定时器堆, 四叉堆 (4-ary)</text>
<circle cx="170" cy="40" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="170" y="44.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<line x1="170" y1="53" x2="50" y2="88" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<circle cx="50" cy="100" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="50" y="104.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<line x1="170" y1="53" x2="130" y2="88" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<circle cx="130" cy="100" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="130" y="104.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<line x1="170" y1="53" x2="210" y2="88" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<circle cx="210" cy="100" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="210" y="104.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<line x1="170" y1="53" x2="290" y2="88" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<circle cx="290" cy="100" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="290" y="104.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="8" y="54" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">孩子: 4i+1 到 4i+4</text>
<rect x="12" y="136" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="27" y="151.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="46" y="136" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="61" y="151.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="80" y="136" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="95" y="151.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="114" y="136" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="129" y="151.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="148" y="136" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="163" y="151.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="182" y="136" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="197" y="151.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="216" y="136" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="231" y="151.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="250" y="136" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="265" y="151.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<rect x="284" y="136" width="30" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="299" y="151.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<text x="8" y="182" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">堆顶 = 最近要触发的定时器, 调度循环每轮看一眼</text>
<text x="8" y="198" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">层数只有二叉堆的一半; 4 个孩子在数组里相邻</text>
</svg>
```

**细节。**

- 节点 i 的孩子是 `4i+1 … 4i+4`，父节点是 `(i-1)/4`
- 下沉时在连续的 4 个孩子里挑最早的那个
- 调度循环每轮检查本 P 堆顶的触发时间，到点就运行

**为什么。** 四叉堆层数只有二叉堆的一半，上浮更短；4 个孩子在数组里相邻，下沉时的比较集中在一两个缓存行里。

**例题：** LC 1834 单线程 CPU（同类：LC 253 会议室 II）

给一组任务 `[入队时间, 处理时长]`，单线程 CPU 空闲时从已入队的任务里挑处理时长最短的（并列取下标小的），返回执行顺序。例：`[[1,2],[2,4],[3,2],[4,1]]` → `[0,2,3,1]`。小顶堆按处理时长排，和定时器堆一样，只关心堆顶。

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
