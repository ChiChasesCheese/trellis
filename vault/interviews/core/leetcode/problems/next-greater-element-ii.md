---
slug: next-greater-element-ii
---
## Q
**LC 503 下一个更大元素 II**｜Medium

循环数组 `nums`，返回每个元素向后（循环）第一个比它大的数，没有则为 `-1`。

## A
**一句话。** 单调栈存等待答案的下标，把数组走两圈模拟循环。

```python
def next_greater_elements(nums):
    n = len(nums)
    ans = [-1] * n
    stack = []                     # 还没找到更大数的下标
    for i in range(2 * n):         # 两圈
        x = nums[i % n]
        while stack and nums[stack[-1]] < x:
            ans[stack.pop()] = x
        if i < n:                  # 第二圈只回答，不入栈
            stack.append(i)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 第二圈也入栈：栈里出现重复下标，白做无用功。
- 判断用 `<=`：相等不算更大，`[2,2,2]` 会得 `[2,2,2]`，应为 `[-1,-1,-1]`。
- 栈里存值不存下标：无法写回 `ans` 的位置。

**追问。**
- 下一个更小元素？：把 `<` 改成 `>`。
- 要距离而不是值（LC 739）？：写 `i - 弹出的下标`。

**同模式。** LC 496 下一个更大元素 I、LC 739 每日温度、LC 84 柱状图中最大的矩形、LC 901 股票价格跨度
