---
id: uth-python-asyncio-1-loop
node: python.asyncio
type: qa
step: 1
---
## Q
**一个线程怎么同时等很多件事**｜Python · CPython 3.14

`asyncio` 的事件循环每轮迭代（`_run_once`）做哪几件事？`await asyncio.sleep(3)` 到时间是怎么被唤醒的？

## A
**背景。** 程序大部分时间在「等」：等网络回包、等定时。每件事开一个线程去干等，线程一多，内存和切换开销都很大。事件循环（event loop）只用一个线程：把要等的事登记起来，每轮看谁已经好了，就接着跑谁的后续代码（回调，callback）。

**结构。** 三样东西：`_ready` 是现在就能跑的回调队列（`deque`）；`_scheduled` 是按触发时间排的最小堆，堆顶最早；`selector` 是向操作系统问「哪些网络连接有数据了」，可以阻塞等待。例：`sleep(3)` 就是往堆里放一项「3 秒后唤醒我」；下一轮 `_ready` 空，就等 3 秒，到期后移进 `_ready` 执行。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<text x="80" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">_scheduled 最小堆</text>
<circle cx="80" cy="44" r="15" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="80" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3.0</text>
<line x1="70" y1="57" x2="52" y2="76" stroke-width="1.2" stroke="currentColor"/>
<line x1="90" y1="57" x2="108" y2="76" stroke-width="1.2" stroke="currentColor"/>
<circle cx="48" cy="90" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="48" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5.2</text>
<circle cx="112" cy="90" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="112" y="94" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4.1</text>
<text x="262" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">_ready 队列</text>
<rect x="205" y="32" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="225" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">cb1</text>
<rect x="245" y="32" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="265" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">cb2</text>
<rect x="285" y="32" width="40" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="305" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">cb3</text>
<line x1="96" y1="44" x2="203" y2="44" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="203.0,44.0 197.0,47.0 197.0,41.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="150" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">到期 heappop</text>
<rect x="95" y="150" width="150" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">selector.select(timeout)</text>
<line x1="240" y1="150" x2="262" y2="60" stroke-width="1.2" stroke="currentColor"/>
<polygon points="262.0,60.0 263.5,66.5 257.7,65.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="300" y="115" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">I/O 就绪</text>
<line x1="80" y1="106" x2="120" y2="148" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<polygon points="120.0,148.0 113.7,145.7 118.0,141.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="108" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">timeout</text>
<text x="170" y="202" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每轮只跑此刻 _ready 里的回调</text>
</svg>
```

**细节。**

- 先算等待时间：`_ready` 非空就是 0，否则取堆顶触发时间减当前时间。
- `selector.select(timeout)` 阻塞等待，I/O 就绪的回调进 `_ready`。
- 堆顶已到期的定时回调逐个 `heappop`，移进 `_ready`。
- 只执行此刻 `_ready` 里的回调，执行中新加的留到下一轮。

**为什么。** 取最近的到期时间只需看堆顶，O(1)，插入 O(log n)；`sleep` 就是用 `call_later` 往堆里放一项。

**例题：** LC 1834 单线程 CPU

给二维数组 `tasks`，`tasks[i] = [入队时间, 处理时长]`。单线程 CPU 空闲且有任务已入队时，选处理时长最短的（并列选下标最小的），开始后必须执行完。返回 CPU 处理任务的下标顺序，`n <= 10^5`。例：`[[1,2],[2,4],[3,2],[4,1]]` 返回 `[0,2,3,1]`。

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
