---
slug: max-consecutive-ones
---
## Q
**LC 485 最大连续 1 的个数**｜Easy

二进制数组 `nums`，求最长连续 `1` 的个数。

## A
**一句话。** 遇 `1` 当前段加一，遇 `0` 清零，每步更新最大值。

```python
def find_max_consecutive_ones(nums):
    best = run = 0
    for x in nums:
        run = run + 1 if x == 1 else 0
        best = max(best, run)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 只在遇到 `0` 时更新最大值：`[1,1,1]` 漏掉末尾那段，得 `0`，应为 `3`。
- 遇到 `0` 忘记清零：`[1,1,0,1]` 得 `3`，应为 `2`。

**追问。**
- 允许翻转至多 `k` 个 `0` 呢？：滑动窗口，窗口内 `0` 的个数不超过 `k`（LC 1004）。

**同模式。** LC 1004 最大连续 1 的个数 III、LC 487 最大连续 1 的个数 II、LC 53 最大子数组和
