---
id: uth-python-asyncio-2-lazy-cancel
node: python.asyncio
type: qa
step: 2
---
## Q
**取消的定时器怎么从堆里删掉**｜Python · CPython 3.14

`call_later` 返回的句柄调用 `cancel()` 后，它会马上从最小堆里移除吗？

## A
**背景。** 堆只保证堆顶最小。要删掉中间某个元素，得先在数组里找到它，O(n)，还要重新整理，代价不小。而定时器经常在到期前就被取消。

**结构。** 所以不删：只给句柄打上已取消的标记，仍留在堆里，这叫惰性删除（lazy deletion）。轮到它当堆顶时再丢掉。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最小堆 (call_later 句柄)</text>
<line x1="170" y1="58" x2="100" y2="78" stroke-width="1.2" stroke="currentColor"/>
<line x1="170" y1="58" x2="240" y2="78" stroke-width="1.2" stroke="currentColor"/>
<line x1="100" y1="106" x2="62" y2="126" stroke-width="1.2" stroke="currentColor"/>
<line x1="100" y1="106" x2="138" y2="126" stroke-width="1.2" stroke="currentColor"/>
<line x1="240" y1="106" x2="202" y2="126" stroke-width="1.2" stroke="currentColor"/>
<line x1="240" y1="106" x2="278" y2="126" stroke-width="1.2" stroke="currentColor"/>
<circle cx="170" cy="44" r="14" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="48" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<line x1="161" y1="35" x2="179" y2="53" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="100" cy="92" r="14" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="100" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="240" cy="92" r="14" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="240" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="62" cy="140" r="14" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="62" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<line x1="53" y1="131" x2="71" y2="149" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="138" cy="140" r="14" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="138" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="202" cy="140" r="14" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="202" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<line x1="193" y1="131" x2="211" y2="149" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<circle cx="278" cy="140" r="14" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="278" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="20" y="168" width="14" height="14" rx="3" fill="none" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="42" y="179" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">cancel() 只打标记 仍留在堆里</text>
</svg>
```

**细节。**

- 每轮循环，堆顶如果是已取消的，就 `heappop` 丢掉。
- 堆里超过 100 项且已取消的占一半以上时，过滤掉它们再 `heapify`（把剩下的重新整理成堆）。
- 实测 1000 个定时器取消尾部 400 个，堆仍是 1000；累计取消 600 个后降到 400。

**为什么。** `cancel` 只是打标记，O(1)；清理的代价摊到各轮里。

**例题：** LC 3607 电网维护

`c` 个电站由固定的连接组成电网，初始都在线。查询 `[1, x]`：`x` 在线就返回 `x`，否则返回同一连通分量里编号最小的在线电站，没有返回 `-1`；查询 `[2, x]`：让 `x` 离线。`c <= 10^5`，查询数 `<= 2 * 10^5`。

```python
import heapq

def process_queries(
    c: int, connections: list[list[int]], queries: list[list[int]]
) -> list[int]:
    parent = list(range(c + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in connections:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    heaps: dict[int, list[int]] = {}
    for station in range(1, c + 1):
        heaps.setdefault(find(station), []).append(station)
    for heap in heaps.values():
        heapq.heapify(heap)

    online = [True] * (c + 1)
    answers = []
    for kind, station in queries:
        if kind == 2:
            online[station] = False
            continue
        if online[station]:
            answers.append(station)
            continue
        heap = heaps[find(station)]
        while heap and not online[heap[0]]:
            heapq.heappop(heap)
        answers.append(heap[0] if heap else -1)
    return answers
```
