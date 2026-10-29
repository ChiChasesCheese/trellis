---
id: uth-cpp-priority-queue-deque-3-deque
node: cpp.priority-queue-deque
type: qa
step: 3
---
## Q
**deque 为什么两头都能 O(1)**｜C++ · std::deque

`std::deque` 的 `push_front` 不用搬元素，它是怎么存的？

## A
**背景。** 想要两头都能快速加减的队列。`vector` 在头部插入要把所有元素后移，O(n)；链表两头都快，但每个元素一次分配，内存散得到处都是。折中是把数据分成许多固定大小的小块，块的地址另外放进一个数组，两头增长只需新增一块。

**结构。** 块指针数组，每个指针指向一块固定大小的连续内存。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">块指针数组(map)</text>
<rect x="12" y="24" width="40" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="70" y="24" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="90" y="40.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">●</text>
<rect x="128" y="24" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="148" y="40.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">●</text>
<rect x="186" y="24" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="206" y="40.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">●</text>
<rect x="244" y="24" width="40" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<line x1="90" y1="48" x2="90" y2="80" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="90,80 87.3,74.0 92.7,74.0" style="fill:var(--accent,#3b6fd4)"/>
<line x1="148" y1="48" x2="148" y2="80" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="148,80 145.3,74.0 150.7,74.0" style="fill:var(--accent,#3b6fd4)"/>
<line x1="206" y1="48" x2="206" y2="80" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="206,80 203.3,74.0 208.7,74.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="64" y="82" width="52" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<rect x="66" y="90" width="11" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="78" y="90" width="11" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="90" y="90" width="11" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="102" y="90" width="11" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="122" y="82" width="52" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<rect x="124" y="90" width="11" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="136" y="90" width="11" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="148" y="90" width="11" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="160" y="90" width="11" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="180" y="82" width="52" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<rect x="182" y="90" width="11" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="194" y="90" width="11" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="206" y="90" width="11" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<rect x="218" y="90" width="11" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="70" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">↑ 头</text>
<text x="192" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">↑ 尾</text>
<text x="170" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两头增长只需新增一块,旧块不搬</text>
</svg>
```

**细节。**

- libstdc++ 每块 512 字节（元素 ≥ 512 字节时每块 1 个）
- libc++ 每块 4096 字节：实测 `deque<int>` 一块连续 1024 个
- 头尾增长只需新增块
- 实测 `push_back` 十万次后，最早元素的地址不变

**为什么。** 头部插入 O(1)，也不整体搬迁元素；代价是按下标访问要先查块指针、再查块内位置，多一次间接寻址（多跳一次）。

**坑。** `std::queue` 与 `std::stack` 默认底层容器就是 `deque`。

**例题：** LC 239 滑动窗口最大值（同类：LC 622 设计循环队列）

给整数数组 `nums` 和窗口大小 `k`，窗口每次右移一格，返回每个窗口内的最大值。例：`[1,3,-1,-3,5,3,6,7]`、`k = 3` → `[3,3,5,5,6,7]`。双端队列两头都要进出：队尾弹掉更小的数，队首弹掉滑出窗口的下标。

```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    window: deque[int] = deque()  # 存下标，对应值从队首到队尾单调递减
    result: list[int] = []
    for i, num in enumerate(nums):
        while window and nums[window[-1]] <= num:
            window.pop()
        window.append(i)
        if window[0] <= i - k:  # 队首已经滑出窗口
            window.popleft()
        if i >= k - 1:
            result.append(nums[window[0]])
    return result
```
