---
slug: constrained-subsequence-sum
---
## Q
**LC 1425 带限制的子序列和**｜Hard

整数数组 `nums`，求非空子序列的最大和，要求相邻两个选中元素的下标差不超过 `k`。

## A
**一句话。** `f[i]` 是以 `i` 结尾的最大和，等于 `nums[i] + max(0, f[i-k .. i-1] 的最大值)`；窗口最大值用单调递减队列，答案是 `max(f)`。

```python
def constrained_subset_sum(nums, k):
    f = [0] * len(nums)
    q = deque()                # 下标，f 值从队首到队尾递减
    for i, x in enumerate(nums):
        if q and q[0] < i - k:
            q.popleft()        # 超出 k 步
        best = f[q[0]] if q else 0
        f[i] = x + max(best, 0)    # 前面全负就从 i 重新开始
        while q and f[q[-1]] <= f[i]:
            q.pop()
        q.append(i)
    return max(f)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 少了 `max(best, 0)`：前面的和为负时应该从 `nums[i]` 单独开始。
- 返回 `f[-1]`：子序列不必以最后一个元素结尾，要取全体最大值。

**追问。**
- 和 LC 1696 的区别？：那题必须从头走到尾，这里起点、终点任选，所以多了「与 0 取 max」和「取全局最大」。
- `k = 1` 时是什么？：就是最大子数组和（Kadane）。

**同模式。** LC 239 滑动窗口最大值、LC 1696 跳跃游戏 VI、LC 53 最大子数组和
