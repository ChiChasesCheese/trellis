---
slug: increasing-triplet-subsequence
---
## Q
**LC 334 递增的三元子序列**｜Medium

整数数组 `nums`，判断是否存在 `i < j < k` 使 `nums[i] < nums[j] < nums[k]`。要求 `O(n)` 时间、`O(1)` 空间。

## A
**一句话。** 维护长度为 1、2 的递增子序列的最小结尾 `first`、`second`，来一个比 `second` 大的数就找到了三元组。

**图解。** `first` 改成 0 后 `second` 仍是 4：它背后有一个更早的 `1 < 4`，6 来了就成立。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 160">
<text x="62" y="30.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">x</text>
<rect x="70" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="100" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="115.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="130" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="160" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="175.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="190" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="205.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="220" y="12" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="235.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="62" y="64.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">first</text>
<rect x="70" y="46" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="100" y="46" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="115.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="130" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="160" y="46" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="175.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="190" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="205.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="220" y="46" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="235.0" y="64.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="62" y="98.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">second</text>
<rect x="70" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">∞</text>
<rect x="100" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="115.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">∞</text>
<rect x="130" y="80" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="145.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="160" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="175.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="190" y="80" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="205.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="220" y="80" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="235.0" y="98.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="16" y="124" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">浅色：这一步被更新的值</text>
<text x="16" y="142" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">6 > second = 4：找到 1 < 4 < 6</text>
</svg>

```python
def increasing_triplet(nums):
    first = second = inf   # 长度 1、2 的最小结尾
    for x in nums:
        if x <= first:
            first = x      # 更新后 second 仍有效
        elif x <= second:
            second = x     # first < x <= second
        else:
            return True    # x > second > 某个 first
    return False
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 比较用 `<`：相等的数会被当成更大的，`[1,1,1]` 误判为 `True`，必须 `<=`。
- 以为 `first` 一定在 `second` 前面：`first` 被更新后可能在后面，但 `second` 背后总有一个更早更小的数。

**追问。**
- 推广到长度 `k`？：就是 LIS 的贪心加二分，维护 `tails` 数组，长度到 `k` 即可。
- 要返回三个下标？：额外记下 `second` 被设置时的那个 `first` 的下标。

**同模式。** LC 300 最长递增子序列、LC 2826 将三个组排序、LC 1671 得到山形数组的最少删除次数
