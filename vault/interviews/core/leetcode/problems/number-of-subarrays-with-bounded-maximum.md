---
slug: number-of-subarrays-with-bounded-maximum
---
## Q
**LC 795 区间子数组个数**｜Medium

整数数组 `nums` 与 `left`、`right`，求最大值落在 `[left, right]` 的非空连续子数组个数。

## A
**一句话。** 枚举右端 `i`，记最近一个 `> right` 的位置 `bad` 和最近一个 `>= left` 的位置 `good`，合法起点正好在 `(bad, good]`，加 `good - bad`。

**图解。** `left=2, right=8`，右端到 `6` 时 `bad=1`（9）、`good=4`，起点可取下标 2、3、4，共 3 个。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 144">
<text x="48" y="30.6" text-anchor="end" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">nums</text>
<rect x="56" y="12" width="30" height="30" rx="1" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="86" y="12" width="30" height="30" rx="1" style="fill:var(--dim,#6b7280);fill-opacity:0.16" stroke="currentColor" stroke-width="1.2"/>
<text x="101.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">9</text>
<rect x="116" y="12" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="146" y="12" width="30" height="30" rx="1" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1.2"/>
<text x="161.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="176" y="12" width="30" height="30" rx="1" style="fill:var(--accent,#3b6fd4);fill-opacity:0.45" stroke="currentColor" stroke-width="1.2"/>
<text x="191.0" y="30.6" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="101.0" y="64.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">bad</text>
<text x="191.0" y="64.6" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">good</text>
<text x="16" y="90" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">left=2, right=8，右端 i = 4</text>
<text x="16" y="108" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">9 > 8：子数组不能跨过 bad</text>
<text x="16" y="126" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">起点在 (bad, good] = {2,3,4}，加 3</text>
</svg>

```python
def num_subarray_bounded_max(nums, left, right):
    ans, bad, good = 0, -1, -1
    for i, x in enumerate(nums):
        if x > right:
            bad = i            # 子数组不能包含它
        if x >= left:
            good = i           # 子数组要包含至少一个它
        ans += max(0, good - bad)   # 起点在 (bad, good]
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 加 `i - bad`：会把最大值 `< left` 的子数组也算进来。
- 漏了 `max(0, …)`：`good < bad` 时为负数，答案被减小。

**追问。**
- 另一种写法？：`count(<= right) - count(<= left-1)`，`count(<= t)` 数「最大值不超过 t」的子数组，按连续段长度累加。
- 改成最小值和最大值都受限？：同时记最近的最小值、最大值和越界位置，就是 LC 2444。

**同模式。** LC 560 和为 K 的子数组、LC 2444 统计定界子数组的数目、LC 713 乘积小于 K 的子数组
