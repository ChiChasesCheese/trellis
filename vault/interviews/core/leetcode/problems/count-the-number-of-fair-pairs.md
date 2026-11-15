---
slug: count-the-number-of-fair-pairs
---
## Q
**LC 2563 统计公平数对的数目**｜Medium

整数数组 `nums`，求满足 `i < j` 且 `lower <= nums[i]+nums[j] <= upper` 的数对个数。

## A
**一句话。** 数对只看值，排序不改答案；拆成「和 `<= upper` 的对数」减「和 `<= lower-1` 的对数」，每个都用相向双指针数。

**图解。** 排序后 `t = 6`：`0+5 <= 6`，`i` 与 `(i, j]` 里 4 个数都能配，记 4 对后 `i` 右移。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 144">
<text x="54" y="30.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">排序后</text>
<rect x="62" y="12" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="77.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="92" y="12" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="107.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="122" y="12" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="137.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="152" y="12" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="167.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="182" y="12" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="197.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="212" y="12" width="30" height="30" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="227.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="77.0" y="64.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i</text>
<text x="197.0" y="64.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">j</text>
<text x="16" y="90" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">t = 6：7 太大，j 先左移一格</text>
<text x="16" y="108" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0 + 5 <= 6：i 配 (i, j] 共 4 对</text>
<text x="16" y="126" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">记 cnt += j - i，然后 i 右移</text>
</svg>

```python
def count_fair_pairs(nums, lower, upper):
    nums.sort()
    def at_most(t):             # 和 <= t 的数对个数
        cnt, i, j = 0, 0, len(nums) - 1
        while i < j:
            if nums[i] + nums[j] <= t:
                cnt += j - i    # i 与 (i, j] 都能配
                i += 1
            else:
                j -= 1
        return cnt
    return at_most(upper) - at_most(lower - 1)
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`（不计排序）。

**易错点。**
- 减的是 `at_most(lower)`：和恰为 `lower` 的数对被错减掉。
- 满足时只加 `1`：`nums[i]` 配 `(i, j]` 里任何一个都满足，要加 `j - i`。

**追问。**
- 排序后 `i < j` 还成立吗？：每对无序数只数一次，排序前后的对数一样。
- 改用二分？：对每个 `i` 在 `(i, n)` 二分两个边界，同样 `O(n log n)`。

**同模式。** LC 167 两数之和 II - 输入有序数组、LC 15 三数之和、LC 2824 统计和小于目标的下标对数目、LC 1099 小于 K 的两数之和
