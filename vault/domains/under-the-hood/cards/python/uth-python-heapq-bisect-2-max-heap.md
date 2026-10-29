---
id: uth-python-heapq-bisect-2-max-heap
node: python.heapq-bisect
type: qa
step: 2
---
## Q
**heappop 为什么先下沉到底**｜Python · CPython 3.14

`heappop` 把末尾元素放到堆顶后，为什么不是比较到合适位置就停，而是先一路下沉到叶子？最大堆呢？

## A
**背景。** 取走堆顶后要补一个空位：直接把末尾元素放上去，再和孩子比较、一层层往下换，看起来最自然。但末尾元素原本就在最底层，通常是个大数，几乎总要沉回底部，每层都要比两次。

**结构。** `_siftup`：每层只比较两个孩子，把较小的孩子上移一格，让空位一路走到叶子，再把原来的末尾元素放在那里，往上浮回去。例：堆 `[1,3,2,5,4,8,7]` 取走 1：2 上移，8 上移，空位到了叶子；7 放进去，比父亲 8 小，换上去，比 2 大，停。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 220">
<line x1="158.454" y1="33.9174" x2="111.546" y2="66.0826" stroke-width="1.2" stroke="currentColor"/>
<line x1="181.546" y1="33.9174" x2="228.454" y2="66.0826" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="91.7516" y1="85.3121" x2="73.2484" y2="110.688" stroke-width="1.2" stroke="currentColor"/>
<line x1="108.248" y1="85.3121" x2="126.752" y2="110.688" stroke-width="1.2" stroke="currentColor"/>
<line x1="231.752" y1="85.3121" x2="213.248" y2="110.688" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<circle cx="170" cy="26" r="14" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="100" cy="74" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="240" cy="74" r="14" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="240" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<circle cx="65" cy="122" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="65" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="135" cy="122" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="135" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="205" cy="122" r="14" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="205" y="126" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">7</text>
<text x="227" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">7 上浮</text>
<text x="170" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1 被取走 空位沿较小的孩子下沉</text>
<text x="170" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">到叶子 再把末尾元素 7 从那里上浮</text>
<text x="170" y="200" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">比较次数少 因为 7 通常留在底部</text>
</svg>
```

**细节。**

- 源码注释的实测：1000 次 `heappop` 的比较次数从约 14996 降到约 8680。
- 3.14 起有了 `heappush_max`、`heappop_max`、`heapify_max`；以前只能存负数。

**为什么。** 比较可能是自定义的 `__lt__`，很贵，省比较比省赋值重要。

**例题：** LC 295 数据流的中位数

设计 `MedianFinder`：`add_num(num)` 往数据流加入一个整数；`find_median()` 返回目前所有数的中位数（个数为偶数时取中间两个的平均）。调用总数最多 `5 * 10^4`。

```python
import heapq

class MedianFinder:
    def __init__(self) -> None:
        self.small: list[int] = []  # 较小一半，取负数模拟最大堆
        self.large: list[int] = []  # 较大一半，最小堆

    def add_num(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0
```
