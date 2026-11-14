---
slug: binary-search
---
## Q
**LC 704 二分查找**｜Easy

升序数组 `nums`（元素互不相同）中查找 `target`，返回下标，不存在返回 `-1`。

## A
**一句话。** 左闭右开区间 `[lo, hi)` 找第一个 `>= target` 的位置，最后检查它是否等于 `target`。

**图解。** 每一步把 `[lo, hi)` 砍掉一半，最后 `lo` 停在第一个 `>= target` 的位置。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 156">
<text x="34" y="16" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<text x="62" y="16" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<text x="90" y="16" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<text x="118" y="16" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<text x="146" y="16" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<text x="174" y="16" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="20" y="22" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34.0" y="38.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-1</text>
<rect x="48" y="22" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="62.0" y="38.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="76" y="22" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90.0" y="38.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="104" y="22" width="28" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="118.0" y="38.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="132" y="22" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="146.0" y="38.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<rect x="160" y="22" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="174.0" y="38.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">12</text>
<text x="198" y="38" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">5 &lt; 9：lo = 4</text>
<rect x="20" y="54" width="28" height="24" rx="2" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="34.0" y="70.32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<rect x="48" y="54" width="28" height="24" rx="2" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="62.0" y="70.32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="76" y="54" width="28" height="24" rx="2" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="90.0" y="70.32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="104" y="54" width="28" height="24" rx="2" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="118.0" y="70.32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="132" y="54" width="28" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="146.0" y="70.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<rect x="160" y="54" width="28" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="174.0" y="70.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">12</text>
<text x="198" y="70" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">12 ≥ 9：hi = 5</text>
<rect x="20" y="86" width="28" height="24" rx="2" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="34.0" y="102.32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">-1</text>
<rect x="48" y="86" width="28" height="24" rx="2" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="62.0" y="102.32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="76" y="86" width="28" height="24" rx="2" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="90.0" y="102.32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="104" y="86" width="28" height="24" rx="2" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="118.0" y="102.32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="132" y="86" width="28" height="24" rx="2" style="fill:var(--accent,#3b6fd4);fill-opacity:0.32" stroke="currentColor" stroke-width="1.2"/>
<text x="146.0" y="102.32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<rect x="160" y="86" width="28" height="24" rx="2" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="174.0" y="102.32" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">12</text>
<text x="198" y="102" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">9 ≥ 9：hi = 4</text>
<text x="20" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">lo = hi = 4，nums[4] = 9 → 找到</text>
<text x="20" y="150" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">灰：已排除　深色：mid</text>
</svg>

```python
def search(nums, target):
    lo, hi = 0, len(nums)        # [lo, hi)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1         # 排除 [lo, mid]
        else:
            hi = mid             # mid 可能是答案
    if lo < len(nums) and nums[lo] == target:
        return lo
    return -1
```

**复杂度。** 时间 `O(log n)`，空间 `O(1)`。

**易错点。**
- 闭区间 `while lo <= hi` 却写 `hi = mid`：区间不收缩，`[5]`、`target=2` 死循环。
- 左闭右开却写 `lo = mid`：`[1,2]`、`target=2` 时死循环。
- 不检查 `lo < len(nums)`：`target` 比所有元素大时 `nums[lo]` 越界。

**追问。**
- 有重复元素，找首个或最后一个位置？：首个是 `bisect_left`，最后一个是 `bisect_right - 1`。
- 答案空间上的二分？：把有序数组换成单调的判定函数，同一模板（LC 875）。

**同模式。** LC 35 搜索插入位置、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 33 搜索旋转排序数组、LC 74 搜索二维矩阵
