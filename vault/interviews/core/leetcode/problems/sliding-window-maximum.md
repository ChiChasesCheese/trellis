---
slug: sliding-window-maximum
---
## Q
**LC 239 滑动窗口最大值**｜Hard

大小为 `k` 的窗口从左到右滑动，返回每个窗口的最大值。

## A
**一句话。** 单调递减双端队列存下标：新数入队前弹掉队尾所有不大于它的，队首滑出窗口就弹出，队首即最大值。

```python
def max_sliding_window(nums, k):
    window = deque()             # 下标，对应值递减
    ans = []
    for i, x in enumerate(nums):
        while window and nums[window[-1]] <= x:
            window.pop()         # 更小又更早离开，没机会了
        window.append(i)
        if window[0] <= i - k:   # 队首滑出窗口
            window.popleft()
        if i >= k - 1:           # 窗口满了才记录
            ans.append(nums[window[0]])
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(k)`。

**易错点。**
- 队列存值不存下标：判不了过期，重复值会误弹，`[3,2,2,1,3]`、`k=2` 错得 `[3,2,1,3]`。
- 忘了弹过期队首：`[5,1,1,1]`、`k=2` 得 `[5,5,5]`，应为 `[5,1,1]`。
- 窗口未满就记录：多输出 `k-1` 个值。

**追问。**
- 变长窗口（LC 1438）？：双指针加两个单调队列，分别维护最大和最小。
- 不用队列还有 `O(n)` 解吗？：按 `k` 分块，算块内前缀最大和后缀最大，窗口最大值是两者之一。

**同模式。** LC 1438 绝对差不超过限制的最长连续子数组、LC 862 和至少为 K 的最短子数组、LC 1696 跳跃游戏 VI、LC 739 每日温度
