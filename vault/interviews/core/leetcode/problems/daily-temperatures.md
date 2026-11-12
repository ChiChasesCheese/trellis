---
slug: daily-temperatures
---
## Q
**LC 739 每日温度**｜Medium

给每日温度 `temperatures`，对每一天求下一个更高温度在几天后，没有则为 `0`。

## A
**一句话。** 单调栈存还在等更高温度的下标，新的一天弹出所有比它低的天并结算天数差。

```python
def daily_temperatures(temperatures):
    ans = [0] * len(temperatures)
    stack = []                  # 下标，温度从栈底到栈顶不增
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j      # 等了 i - j 天
        stack.append(i)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 弹出条件写成 `<=`：相等温度也被结算，`[70,70,80]` 得 `[1,1,0]`，应为 `[2,1,0]`。
- 栈里存温度不存下标：弹出时算不出天数差。
- 先压栈再比较：栈顶是自己，`while` 永不成立，输出全 `0`。

**追问。**
- 数组是环形的（LC 503）？：遍历 `2n` 次，用 `i % n` 取值。
- 温度范围很小怎么办？：从右往左，用小表记每个温度最近出现的下标，查比它高的温度里下标最小的。

**同模式。** LC 496 下一个更大元素 I、LC 503 下一个更大元素 II、LC 901 股票价格跨度、LC 84 柱状图中最大的矩形
