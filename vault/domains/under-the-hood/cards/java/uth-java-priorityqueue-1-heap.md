---
id: uth-java-priorityqueue-1-heap
node: java.priorityqueue
type: qa
step: 1
---
## Q
**PriorityQueue 遍历为什么不是有序的**｜Java · OpenJDK 25

依次 `add` 5、3、8、1、9、2 后打印 `PriorityQueue`，输出是什么？为什么不是排好序的？

## A
**背景。** 要反复取出「当前最小的」，同时不断加入新元素：每次扫一遍是 O(n)，每次重排更贵。堆（heap）只保证一件事：每个父节点不大于它的孩子，所以最小的一定在顶上，其余顺序不管，维护起来便宜。

**结构。** 数组上的二叉最小堆（binary heap）：`queue[n]` 的两个孩子是 `queue[2n+1]` 和 `queue[2n+2]`，最小的在 `queue[0]`。新元素放末尾，比父亲小就换上去（上浮）。例：依次放 5、3、8、1、9、2。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 230">
<line x1="158.454" y1="31.9174" x2="111.546" y2="64.0826" stroke-width="1.2" stroke="currentColor"/>
<line x1="181.546" y1="31.9174" x2="228.454" y2="64.0826" stroke-width="1.2" stroke="currentColor"/>
<line x1="91.7516" y1="83.3121" x2="73.2484" y2="108.688" stroke-width="1.2" stroke="currentColor"/>
<line x1="108.248" y1="83.3121" x2="126.752" y2="108.688" stroke-width="1.2" stroke="currentColor"/>
<line x1="231.752" y1="83.3121" x2="213.248" y2="108.688" stroke-width="1.2" stroke="currentColor"/>
<circle cx="170" cy="24" r="14" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="100" cy="72" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="240" cy="72" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="240" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="65" cy="120" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="65" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="135" cy="120" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="135" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<circle cx="205" cy="120" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="205" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="62" y="146" width="36" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="80" y="163" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="80" y="188" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="98" y="146" width="36" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="116" y="163" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="116" y="188" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="134" y="146" width="36" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="152" y="163" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="152" y="188" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="170" y="146" width="36" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="188" y="163" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="188" y="188" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="206" y="146" width="36" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="224" y="163" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<text x="224" y="188" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="242" y="146" width="36" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="260" y="163" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<text x="260" y="188" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<text x="170" y="214" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">打印 = 数组顺序 只保证父不大于子</text>
</svg>
```

**细节。**

- 实测打印 `[1, 3, 2, 5, 9, 8]`，只保证堆序（父不大于子），不保证全局有序；连续 `poll` 才得到 `1 2 3 5 8 9`。
- 默认初始容量 11；容量小于 64 时扩为 `2n+2`，否则加 50%。
- `offer`、`poll` 是 O(log n)，`peek` 是 O(1)，`remove(Object)` 要先线性查找，是 O(n)。
- 最大堆传 `Comparator.reverseOrder()`。

**为什么。** 堆只维护「最小的在最前」这一点，比完整排序便宜得多。

**例题：** LC 253 会议室 II

给会议时间数组 `intervals`，`intervals[i] = [start, end]`，求同时容纳所有会议至少需要多少间会议室。`1 <= intervals.length <= 10^4`。

```python
import heapq

def min_meeting_rooms(intervals: list[list[int]]) -> int:
    ongoing: list[int] = []  # 各房间当前会议的结束时间，堆顶最早空出来
    for start, end in sorted(intervals):
        if ongoing and ongoing[0] <= start:
            heapq.heapreplace(ongoing, end)
        else:
            heapq.heappush(ongoing, end)
    return len(ongoing)
```
