---
id: lct-learn-data-structures-5-7
node: data-structures.5.7
type: qa
step: 1
---
## Q
**常用数据结构 › 堆（优先队列） › 对顶堆（动态第 K 小/大）**｜学习卡

套路是什么？

## A
**一句话。** 把有序序列从中间切开：较小一半放最大堆 `left`、较大一半放最小堆 `right`，两堆大小差 0 或 1 且 `left` 全体不超过 `right` 全体，中位数就在两个堆顶，加数 `O(log n)`。

下图：较小一半在最大堆、较大一半在最小堆，中位数只看两个堆顶。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<text x="170" y="20" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">有序序列从中间切开</text>
<rect x="70" y="34" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="90.0" y="52.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="110" y="34" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="130.0" y="52.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="150" y="34" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170.0" y="52.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<rect x="190" y="34" width="40" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="210.0" y="52.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<rect x="230" y="34" width="40" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="250.0" y="52.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<line x1="190" y1="28" x2="190" y2="70" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<line x1="70" y1="78" x2="70" y2="84" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="190" y1="78" x2="190" y2="84" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="70" y1="78" x2="190" y2="78" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="130.0" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">left：最大堆（存负数）</text>
<line x1="190" y1="78" x2="190" y2="84" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="270" y1="78" x2="270" y2="84" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="190" y1="78" x2="270" y2="78" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="230.0" y="96" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">right：最小堆</text>
<text x="170.0" y="118" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">堆顶 3</text>
<text x="220.0" y="118" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">堆顶 4</text>
<text x="170" y="142" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">len(left) - len(right) 只能是 0 或 1</text>
<text x="170" y="162" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">奇数个：中位数 = left 顶；偶数个：两顶平均</text>
</svg>

```python
class MedianFinder:                  # LC 295，只增不删
    def __init__(self):
        self.l, self.r = [], []      # l 存相反数：最大堆

    def add_num(self, num):
        l, r = self.l, self.r
        if len(l) == len(r):
            heappush(l, -heappushpop(r, num))    # 过右堆，最小搬左
        else:
            heappush(r, -heappushpop(l, -num))   # 过左堆，最大搬右

    def find_median(self):
        l, r = self.l, self.r
        if len(l) > len(r):
            return -l[0]
        return (r[0] - l[0]) / 2
```

**要点。**
- 为什么对？：不变量一，`l` 比 `r` 多 0 或 1 个；不变量二，`l` 最大值不超过 `r` 最小值。先过对面再搬回来，同时保持两条，不用讨论 `num` 是大是小。
- LC 480 怎么改？：堆不能删中间元素，用懒删除：`delayed[x] += 1` 只做标记，等浮到堆顶再弹；因堆长度里混有待删元素，另用 `lsz`、`rsz` 记有效个数，每次增删后按有效个数平衡并清理堆顶；元素归属看 `x <= -left[0]`。
- 窗口长度为偶数怎么取？：两个堆顶的平均，是小数。

**易错点。**
- 不经过对面直接按大小放：依次加入 `5, 1, 3` 应得中位数 `3`，错写得 `5`。
- 偶数个取平均写成整除：`1, 2` 应得 `1.5`；左堆存相反数却忘了取反，平均要写 `(r[0] - l[0]) / 2`。
- LC 480 用 `len(heap)` 当大小，或平衡后不清理新露出的堆顶：`[1,3,-1,-3,5,3,6,7]`、`k = 3` 应得 `[1,-1,-1,3,5,6]`。

**对应题目。** LC 295 数据流的中位数、LC 480 滑动窗口中位数
