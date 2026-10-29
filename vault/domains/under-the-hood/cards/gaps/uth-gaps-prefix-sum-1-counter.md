---
id: uth-gaps-prefix-sum-1-counter
node: gaps.prefix-sum
type: qa
step: 1
---
## Q
**监控计数为什么记「累计数」**｜Prometheus · v3.5

服务每 15 秒被采集一次。请求数该怎么记，事后才能算出任意一段时间内来了多少个请求？

## A
**背景。** 直觉做法：服务每 15 秒报「这 15 秒来了几个」。可只要丢一次采集，那 15 秒的数就永远没了；算 5 分钟的总数，还得把 20 个数加起来。Prometheus 反过来：计数器（counter）只报「从启动到现在一共来了几个」，只增不减。

**结构。** 每次采集存一个（时间，累计值）。累计值就是前缀和（prefix sum）。一段时间的增量 = 窗口里最后一个值 − 第一个值，一次减法，中间丢几次采集都不影响。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 166">
<line x1="20" y1="140" x2="276" y2="140" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<line x1="34" y1="129" x2="88" y2="112.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="88" y1="112.5" x2="142" y2="101.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="142" y1="101.5" x2="196" y2="79.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="196" y1="79.5" x2="250" y2="63" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="34" y1="129" x2="292" y2="129" fill="none" stroke="currentColor" stroke-width="1.8" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="292" y1="129" x2="292" y2="69" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M292,63 L288.5,70 L295.5,70 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<circle cx="34" cy="129" r="3.5" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="34" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">100</text>
<text x="34" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">0s</text>
<circle cx="88" cy="112.5" r="3.5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="88" y="103.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">130</text>
<text x="88" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">15s</text>
<circle cx="142" cy="101.5" r="3.5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="142" y="92.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">150</text>
<text x="142" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">30s</text>
<circle cx="196" cy="79.5" r="3.5" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="196" y="70.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">190</text>
<text x="196" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">45s</text>
<circle cx="250" cy="63" r="3.5" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="250" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">220</text>
<text x="250" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">60s</text>
<text x="300" y="94" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">增量</text>
<text x="300" y="110" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">120</text>
</svg>
```

例：`100, 130, 150, 190, 220`，增量 = 220 − 100 = 120，平均每秒 120 / 60 = 2 个。

**细节。**

- `increase()` 给增量，`rate()` 给每秒平均，都是「最后 − 第一」
- 官方说明：结果按窗口两端外推，所以整数计数器也能算出小数
- 窗口里至少要有 2 个样本才有结果（v3.5 源码）

**为什么。** 累计值丢一次采集只丢精度，不丢总数；服务只需在内存里加一个数。

**例题：** LC 303 区域和检索（同类：LC 1480 动态和）

给整数数组 `nums`（不会被修改），实现 `NumArray(nums)` 和 `sumRange(left, right)`，返回下标 `left` 到 `right`（含两端）的元素和，会被调用很多次。例：`nums = [-2,0,3,-5,2,-1]`，`sumRange(0,2)` → 1，`sumRange(2,5)` → -1。

```python
class NumArray:
    def __init__(self, nums: list[int]) -> None:
        self.prefix = [0]
        for x in nums:
            self.prefix.append(self.prefix[-1] + x)

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]
```
