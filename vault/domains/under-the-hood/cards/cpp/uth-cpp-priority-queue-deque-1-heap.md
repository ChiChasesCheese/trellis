---
id: uth-cpp-priority-queue-deque-1-heap
node: cpp.priority-queue-deque
type: qa
step: 1
---
## Q
**priority_queue 是怎么实现的**｜C++ · libstdc++ 16

`std::priority_queue` 是独立的数据结构吗？默认大顶还是小顶？

## A
**背景。** 想要“每次拿走最大的那个”。排好序的数组拿最大 O(1)，插入要后移，O(n)；不排序则找最大要扫一遍，O(n)。堆（heap）折中：只要求每个节点不小于它的孩子，最大的永远在最顶上。

**结构。** 堆摊在数组里：下标 i 的孩子在 2i+1、2i+2，没有指针。`std::priority_queue` 只是 `vector` 加 `push_heap` / `pop_heap` 的一层包装。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<line x1="159.136" y1="31.1393" x2="110.864" y2="62.8607" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<line x1="180.864" y1="31.1393" x2="229.136" y2="62.8607" stroke="currentColor" stroke-width="1"/>
<line x1="92.1282" y1="80.3458" x2="72.8718" y2="105.654" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<line x1="107.872" y1="80.3458" x2="127.128" y2="105.654" stroke="currentColor" stroke-width="1"/>
<line x1="232.128" y1="80.3458" x2="212.872" y2="105.654" stroke="currentColor" stroke-width="1"/>
<line x1="247.872" y1="80.3458" x2="267.128" y2="105.654" stroke="currentColor" stroke-width="1"/>
<line x1="59.8166" y1="127.922" x2="50.1834" y2="150.078" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<circle cx="170" cy="24" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="170" y="28.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<circle cx="100" cy="70" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="100" y="74.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<circle cx="240" cy="70" r="13" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="240" y="74.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<circle cx="65" cy="116" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="65" y="120.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="135" cy="116" r="13" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="135" y="120.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="205" cy="116" r="13" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="205" y="120.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<circle cx="275" cy="116" r="13" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="275" y="120.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="45" cy="162" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2" stroke-dasharray="4 3"/>
<text x="45" y="166.2" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">10</text>
<text x="72" y="166" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新压入 10</text>
<text x="8" y="14" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下标 i 的孩子</text>
<text x="8" y="28" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">= 2i+1 与 2i+2</text>
<text x="196" y="166" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">10 比父节点大就换:</text>
<text x="196" y="180" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">换过 3, 7, 9 三层到顶</text>
<rect x="22" y="196" width="34" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="39" y="210.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<text x="39" y="230" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="60" y="196" width="34" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="77" y="210.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="77" y="230" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="98" y="196" width="34" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="115" y="210.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<text x="115" y="230" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="136" y="196" width="34" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="153" y="210.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="153" y="230" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="174" y="196" width="34" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="191" y="210.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="191" y="230" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="212" y="196" width="34" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="229" y="210.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="229" y="230" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="250" y="196" width="34" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="267" y="210.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="267" y="230" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="288" y="196" width="34" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="305" y="210.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<text x="305" y="230" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
</svg>
```

**细节。**

- 例：压入 10：先放数组末尾，比父节点大就交换，换 3 次到顶，最多换树高 log n 次
- 默认比较器是 `less`，所以是大顶堆（实测依次压入 3 1 4 1 5，`top()` 为 5）
- 用一批数据直接构造时调用 `make_heap`，从最后一个非叶节点往前逐个下沉（和较大的孩子换位置），总共 O(n)，比逐个 `push` 的 O(n log n) 快

**为什么。** 数组存堆没有指针，内存连续，缓存友好。

**坑。** 小顶堆要写 `priority_queue<int, vector<int>, greater<int>>`；没有 decrease-key（把堆里某项改小），Dijkstra 靠重复入堆、弹出时跳过过期项。

**例题：** LC 253 会议室 II（同类：LC 23 合并 K 个升序链表）

给一组会议时间 `[start, end]`，求最少需要几间会议室，一个会议结束的时刻可以立刻开始下一个。例：`[[0,30],[5,10],[15,20]]` → `2`。小顶堆里放各房间的结束时间，堆顶是最早空出来的。

```python
import heapq


def min_meeting_rooms(intervals: list[list[int]]) -> int:
    ends: list[int] = []                           # 小根堆：每个在用会议室的结束时间
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:              # 最早结束的会议已结束：复用它的房间
            heapq.heapreplace(ends, end)           # 弹出旧结束时间并压入新的，一次 O(log n)
        else:
            heapq.heappush(ends, end)              # 没有空房间：新开一间
    return len(ends)                               # 堆里剩几个 = 同时在用的房间数峰值
```
