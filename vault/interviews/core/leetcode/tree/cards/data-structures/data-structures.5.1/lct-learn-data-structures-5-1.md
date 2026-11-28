---
id: lct-learn-data-structures-5-1
node: data-structures.5.1
type: qa
step: 1
---
## Q
**常用数据结构 › 堆（优先队列） › 基础**｜学习卡

套路是什么？

## A
**一句话。** 堆 `O(log n)` 取出当前最值并放回新元素：「每步贪心处理当前最大（最小）并放回」用堆，「始终只关心前 `k` 大」用大小为 `k` 的最小堆，`heapq` 是最小堆，要最大堆就存负数。

下图：两种用法按题意选；`heapq` 是最小堆。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<polygon points="126.0,20.0 135.0,7.5 205.0,7.5 214.0,20.0 205.0,32.5 135.0,32.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">题目要什么？</text>
<rect x="24.6" y="60.0" width="120.9" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="76.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">每步取最大并放回</text>
<text x="85" y="91.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">堆存负数 = 最大堆</text>
<rect x="32.1" y="120.0" width="105.8" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="85" y="136.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">pop 最重的两个</text>
<text x="85" y="151.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">差值 push 回去</text>
<rect x="194.6" y="60.0" width="120.9" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="76.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">始终只要前 k 大</text>
<text x="255" y="91.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">大小为 k 的最小堆</text>
<rect x="204.6" y="120.0" width="100.7" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="136.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">push 后超过 k</text>
<text x="255" y="151.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">就 pop 最小</text>
<rect x="202.1" y="182.5" width="105.8" height="25" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="255" y="199.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">堆顶 = 第 k 大</text>
<path d="M 126.0 20.0 L 85.0 20.0 L 85.0 60.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,60.0 82.0,53.7 88.0,53.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 214.0 20.0 L 255.0 20.0 L 255.0 60.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255.0,60.0 252.0,53.7 258.0,53.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 85.0 100.0 L 85.0 120.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85.0,120.0 82.0,113.7 88.0,113.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 255.0 100.0 L 255.0 120.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255.0,120.0 252.0,113.7 258.0,113.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 255.0 160.0 L 255.0 182.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255.0,182.5 252.0,176.2 258.0,176.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>

```python
def last_stone_weight(stones):       # LC 1046
    h = [-x for x in stones]         # 最大堆：存负数
    heapify(h)                       # O(n)，比逐个 push 快
    while len(h) > 1:
        a = -heappop(h)              # 最重
        b = -heappop(h)              # 次重
        if a != b:
            heappush(h, -(a - b))    # 差值放回；相等则同归于尽
    return -h[0] if h else 0
class KthLargest:                    # LC 703
    def __init__(self, k, nums):
        self.k, self.h = k, []       # 最小堆，只留最大的 k 个
        for x in nums:
            self.add(x)
    def add(self, val):
        heappush(self.h, val)
        if len(self.h) > self.k:
            heappop(self.h)          # 弹掉最小的，剩前 k 大
        return self.h[0]             # 堆顶就是第 k 大
```

**要点。**
- 为什么对？：堆是数组存的完全二叉树，根最小；`push` 向上、`pop` 向下交换，路径是树高 `O(log n)`。前 `k` 大的最小堆里，新元素不超过堆顶就至多第 `k + 1` 大，进不了前 `k`。
- LC 2530 怎么改？：每次取最大 `x` 加分，用 `heapreplace(h, -((x + 2) // 3))` 换成 `ceil(x / 3)`。
- LC 1834 怎么改？：按到达时间排序，指针把 `<= t` 的任务以 `(耗时, 下标)` 压堆；堆空就把 `t` 跳到下一个到达时间。

**易错点。**
- 最大堆忘了取反：`[2,7,4,1,8,1]` 应得 `1`；相等的两块不能放回，`[2,2]` 应得 `0`。
- 向上取整写成 `x // 3 + 1`：`x = 3` 应得 `1`，会得 `2`；正确是 `(x + 2) // 3`。
- LC 1834 堆空时不跳时间，或堆里不放下标：`[[5,2],[7,2]]` 应得 `[0,1]`，耗时相同时取下标小的。

**对应题目。** LC 703 数据流中的第 K 大元素、LC 1046 最后一块石头的重量（Last Stone Weight）、LC 2530 执行 K 次操作后的最大分数、LC 1834 单线程 CPU
