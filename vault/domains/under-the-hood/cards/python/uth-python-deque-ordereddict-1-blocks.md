---
id: uth-python-deque-ordereddict-1-blocks
node: python.deque-ordereddict
type: qa
step: 1
---
## Q
**deque 为什么两端都是 O(1)**｜Python · CPython 3.14

要从队列两头加、取，`list` 为什么不行？`collections.deque` 的内部是链表还是数组？

## A
**背景。** `list` 头部增删要把后面全部挪一格，O(n)。想两端都快，可以用链表：每个元素一个节点，改指针就行，不用搬数据。但一个元素一个节点，要带两个指针，每个元素还要单独申请一次内存，浪费。

**结构。** 折中：双向链表，每个节点不放一个元素，而是一整块 64 个槽（`BLOCKLEN = 64`），两端各记一个块内下标。在头尾增删只改端点块里的一个槽，满了才挂一个新块。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<rect x="14" y="50" width="88" height="40" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="18" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="28" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="38" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="48" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="58" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="68" y="58" width="10" height="24" rx="3" fill="none" stroke-width="0.8" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="78" y="58" width="10" height="24" rx="3" fill="none" stroke-width="0.8" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="88" y="58" width="10" height="24" rx="3" fill="none" stroke-width="0.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="58" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">64 槽</text>
<rect x="126" y="50" width="88" height="40" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="130" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="140" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="150" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="160" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="170" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="180" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="190" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="200" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<text x="170" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">64 槽</text>
<rect x="238" y="50" width="88" height="40" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<rect x="242" y="58" width="10" height="24" rx="3" fill="none" stroke-width="0.8" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="252" y="58" width="10" height="24" rx="3" fill="none" stroke-width="0.8" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="262" y="58" width="10" height="24" rx="3" fill="none" stroke-width="0.8" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="272" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="282" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="292" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="302" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<rect x="312" y="58" width="10" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="0.8"/>
<text x="282" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">64 槽</text>
<line x1="102" y1="62" x2="126" y2="62" stroke-width="1.2" stroke="currentColor"/>
<polygon points="126.0,62.0 120.0,65.0 120.0,59.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="102.0,62.0 108.0,59.0 108.0,65.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="214" y1="62" x2="238" y2="62" stroke-width="1.2" stroke="currentColor"/>
<polygon points="238.0,62.0 232.0,65.0 232.0,59.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<polygon points="214.0,62.0 220.0,59.0 220.0,65.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="68" y1="138" x2="68" y2="94" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="68.0,94.0 71.0,100.0 65.0,100.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="68" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">leftindex</text>
<line x1="257" y1="138" x2="257" y2="94" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="257.0,94.0 260.0,100.0 254.0,100.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="257" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">rightindex</text>
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">双向链表 每个节点是一整块</text>
</svg>
```

**细节。**

- 不搬动其他元素，也不用 `realloc`（扩大内存块）。
- 实测 `appendleft` 加 `popleft` 约 22 纳秒。

**为什么。** 一元素一节点要带两个指针，额外开销 200%；分块后链接开销约 3%，相邻元素也靠在一起。

**例题：** LC 239 滑动窗口最大值

整数数组 `nums` 和窗口大小 `k`，窗口每次向右滑一格，返回每个窗口内的最大值。`1 <= nums.length <= 10^5`，`1 <= k <= nums.length`。

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
