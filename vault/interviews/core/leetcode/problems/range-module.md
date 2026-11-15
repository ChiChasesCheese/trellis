---
slug: range-module
---
## Q
**LC 715 Range 模块**｜Hard

设计 `RangeModule`，跟踪半开区间 `[left, right)`：`addRange` 加入、`removeRange` 删除、`queryRange` 问是否被完整跟踪。坐标到 `10^9`，操作 `10^4` 次。

## A
**一句话。** 用一个有序端点列表 `a` 表示不相交区间 `[a0,a1) ∪ [a2,a3) ∪ …`；一个点被覆盖当且仅当 `<= x` 的端点个数为奇数；增删时用二分找到受影响的端点段，整段替换。

**图解。** 端点下标为偶数是左端、奇数是右端；`addRange(15, 35)` 把 `[20, 30]` 两个端点换掉，合并成 `[10, 40)`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 144">
<text x="54" y="30.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">端点 a</text>
<rect x="62" y="12" width="36" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="80.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10</text>
<rect x="98" y="12" width="36" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="116.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">20</text>
<rect x="134" y="12" width="36" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="152.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">30</text>
<rect x="170" y="12" width="36" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="188.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">40</text>
<text x="54" y="64.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">下标</text>
<text x="80.0" y="64.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0</text>
<text x="116.0" y="64.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<text x="152.0" y="64.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2</text>
<text x="188.0" y="64.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<text x="16" y="90" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">原来：[10, 20) ∪ [30, 40)</text>
<text x="16" y="108" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">add(15, 35)：15、35 都落在区间内（下标奇数）</text>
<text x="16" y="126" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">删掉 20、30 两个端点，剩 [10, 40)</text>
</svg>

```python
class RangeModule:
    def __init__(self):
        self.a = []            # 端点：[a0,a1) ∪ [a2,a3) ∪ …

    def addRange(self, left, right):
        i = bisect_left(self.a, left)
        j = bisect_right(self.a, right)
        mid = []
        if i % 2 == 0:
            mid.append(left)   # left 在空隙里：成为新左端
        if j % 2 == 0:
            mid.append(right)  # right 在空隙里：成为新右端
        self.a[i:j] = mid

    def queryRange(self, left, right):
        i = bisect_right(self.a, left)
        j = bisect_left(self.a, right)
        return i == j and i % 2 == 1   # 同一段里且被覆盖

    def removeRange(self, left, right):
        i = bisect_left(self.a, left)
        j = bisect_right(self.a, right)
        mid = []
        if i % 2 == 1:
            mid.append(left)   # left 在区间里：截成新右端
        if j % 2 == 1:
            mid.append(right)  # right 在区间里：截成新左端
        self.a[i:j] = mid
```

**复杂度。** 二分 `O(log n)`，切片替换最坏 `O(n)`；空间 `O(n)`。

**易错点。**
- `bisect_left`/`bisect_right` 用反：区间半开，`left` 恰好等于某右端点时要与前一段合并，用 `bisect_left` 才能把那个端点删掉。
- 查询只看 `left` 是否被覆盖：`(left, right)` 中间不能再有端点。

**追问。**
- 动态开点线段树？：按需建结点，存「整段是否被覆盖」并带赋值懒标记，坐标 `10^9` 也只开 `O(q log U)` 个结点。
- 有序集合写法？：`SortedList` 存 `(左, 右)` 区间，增删时合并或切开相交的区间，均摊 `O(log n)`。

**同模式。** LC 56 合并区间、LC 57 插入区间、LC 2276 统计区间中的整数数目、LC 352 将数据流变为多个不相交区间
