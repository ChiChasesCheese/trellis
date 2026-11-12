---
slug: maximum-sum-circular-subarray
---
## Q
**LC 918 环形子数组的最大和**｜Medium

环形数组 `nums`（首尾相连）的非空子数组的最大和。

## A
**一句话。** 答案要么不跨首尾（Kadane 最大段），要么跨首尾（总和减去中间最小段）。

```python
def max_subarray_sum_circular(nums):
    total = cur_max = cur_min = 0
    best_max, best_min = -inf, inf
    for x in nums:
        total += x
        cur_max = max(cur_max + x, x)
        cur_min = min(cur_min + x, x)
        best_max = max(best_max, cur_max)
        best_min = min(best_min, cur_min)
    if best_max < 0:        # 全负：total - best_min 会得空段
        return best_max
    return max(best_max, total - best_min)
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 忘了全负数：`[-3,-2,-3]` 得 `0`，应为 `-2`。
- 只做普通 Kadane：`[5,-3,5]` 得 `5`，漏掉跨首尾的 `[5,5]`，应为 `10`。

**追问。**
- 要返回具体区间？：Kadane 里记录起点；跨首尾时区间是最小段之外的两头。
- 数据是流式的？：两个 Kadane 与总和都能增量更新，每个数 `O(1)`。

**同模式。** LC 53 最大子数组和、LC 152 乘积最大子数组、LC 213 打家劫舍 II、LC 862 和至少为 K 的最短子数组
