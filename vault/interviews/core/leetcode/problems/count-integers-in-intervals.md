---
slug: count-integers-in-intervals
---
## Q
**LC 2276 统计区间中的整数数目**｜Hard

设计 `CountIntervals`：`add(left, right)` 加入闭区间，`count()` 返回至少被一个区间覆盖的整数个数。坐标到 `10^9`，操作 `10^5` 次。

## A
**一句话。** 维护按左端排序的不相交区间和覆盖总数 `total`；新区间加入时，把与它相交的区间全部吞并（从 `total` 减去它们的长度），再加上合并后区间的长度，`count()` 直接返回 `total`。

**图解。** 已有 `[2,3]`、`[7,10]`，加入 `[5,8]` 吞并 `[7,10]` 得 `[5,10]`，总数 `2 + 6 = 8`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 170">
<text x="62.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<text x="86.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<text x="110.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<text x="134.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">4</text>
<text x="158.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">5</text>
<text x="182.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">6</text>
<text x="206.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">7</text>
<text x="230.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">8</text>
<text x="254.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">9</text>
<text x="278.0" y="26.9" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">10</text>
<text x="42" y="54.9" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已有</text>
<rect x="50" y="40" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="74" y="40" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="98" y="40" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="122" y="40" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="146" y="40" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="40" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="194" y="40" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="218" y="40" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="242" y="40" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="266" y="40" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="42" y="82.9" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">加入</text>
<rect x="50" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="74" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="98" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="122" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="146" y="68" width="24" height="24" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="68" width="24" height="24" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="194" y="68" width="24" height="24" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="218" y="68" width="24" height="24" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<rect x="242" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="266" y="68" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="42" y="110.9" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">之后</text>
<rect x="50" y="96" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="74" y="96" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="98" y="96" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="122" y="96" width="24" height="24" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="146" y="96" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="170" y="96" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="194" y="96" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="218" y="96" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="242" y="96" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<rect x="266" y="96" width="24" height="24" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="16" y="134" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">[5,8] 与 [7,10] 相交，吞并成 [5,10]</text>
<text x="16" y="152" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor" font-weight="600">total = 2 + 6 = 8</text>
</svg>

```python
class CountIntervals:
    def __init__(self):
        self.L, self.R = [], []    # 不相交区间，按左端排序
        self.total = 0

    def add(self, left, right):
        L, R = self.L, self.R
        i = bisect_left(R, left)   # 第一个右端 >= left 的
        j = i
        while j < len(L) and L[j] <= right:   # 相交就吞并
            left = min(left, L[j])
            right = max(right, R[j])
            self.total -= R[j] - L[j] + 1
            j += 1
        L[i:j] = [left]
        R[i:j] = [right]
        self.total += right - left + 1

    def count(self):
        return self.total
```

**复杂度。** 每个区间至多被吞并一次，均摊 `O(log n)` 次比较（切片移动最坏 `O(n)`）；空间 `O(n)`。

**易错点。**
- 用左端点二分找起点：前一个区间可能左端更小但右端伸进来，要按右端二分。
- 吞并时忘了先减去旧区间的长度：重叠部分会被重复计数。

**追问。**
- 动态开点线段树？：结点存区间内被覆盖的个数，整段被覆盖就不再往下走，`count` 读根。
- 为什么右端数组也有序？：区间互不相交且按左端排序，右端自然递增。

**同模式。** LC 56 合并区间、LC 57 插入区间、LC 715 Range 模块
