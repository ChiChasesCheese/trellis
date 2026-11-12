---
slug: maximum-width-ramp
---
## Q
**LC 962 最大宽度坡**｜Medium

求满足 `i < j` 且 `A[i] <= A[j]` 的最大 `j - i`，不存在返回 `0`。

## A
**一句话。** 候选左端点是前缀最小值的下标（单调栈），再从右往左扫右端点，能配对就弹栈更新。

```python
def max_width_ramp(nums):
    stack = []                 # 前缀最小值的下标，值严格递减
    for i, x in enumerate(nums):
        if not stack or x < nums[stack[-1]]:
            stack.append(i)
    best = 0
    for j in range(len(nums) - 1, -1, -1):   # 右端点从右往左
        while stack and nums[stack[-1]] <= nums[j]:
            best = max(best, j - stack.pop())
        if not stack:
            break
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 弹栈条件写成 `<`：相等也是坡，`[1,1]` 得 `0`，应为 `1`。
- 右端点从左往右扫：每个 `i` 要配最远的 `j`，从右往左第一次满足才是最远。

**追问。**
- 要返回坡的两端下标？：弹出时同时记下 `i` 和 `j`。
- 条件改成 `A[i] < A[j]`？：入栈和弹栈的比较都改成严格。

**同模式。** LC 496 下一个更大元素 I、LC 739 每日温度、LC 84 柱状图中最大的矩形、LC 1124 表现良好的最长时间段
