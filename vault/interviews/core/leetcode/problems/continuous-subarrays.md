---
slug: continuous-subarrays
---
## Q
**LC 2762 不间断子数组**｜Medium

统计子数组个数，要求子数组内任意两数之差的绝对值 `≤ 2`。`n` 到 `10^5`。

## A
**一句话。** 条件等价于「最大值 - 最小值 ≤ 2」，越短越合法：滑动窗口加两个单调队列维护窗口最值，每个右端点贡献 `right - left + 1`。

```python
def continuous_subarrays(nums):
    mx, mn = deque(), deque()   # 下标；值递减 / 递增
    left = ans = 0
    for right, x in enumerate(nums):
        while mx and nums[mx[-1]] <= x:
            mx.pop()
        mx.append(right)
        while mn and nums[mn[-1]] >= x:
            mn.pop()
        mn.append(right)
        while nums[mx[0]] - nums[mn[0]] > 2:
            left += 1
            if mx[0] < left:     # 队首滑出窗口
                mx.popleft()
            if mn[0] < left:
                mn.popleft()
        ans += right - left + 1  # 以 right 结尾的都合法
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 每次重新求窗口最值：退化成 `O(n^2)`。
- 答案用 `int`：`n = 10^5` 时子数组数到 `5·10^9`，别的语言要 `long`。

**追问。**
- 不用单调队列？：差值只允许 2，窗口用 `Counter`，`max(cnt) - min(cnt) > 2` 时收缩，键最多 3 个。
- 求最长而不是计数（LC 1438）？：同一窗口，记录 `right - left + 1` 的最大值。

**同模式。** LC 239 滑动窗口最大值、LC 1438 绝对差不超过限制的最长连续子数组、LC 2302 统计得分小于 K 的子数组数目
