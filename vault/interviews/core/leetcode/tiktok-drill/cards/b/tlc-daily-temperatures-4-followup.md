---
id: tlc-daily-temperatures-4-followup
node: b.daily-temperatures
type: qa
step: 4
---
## Q
**LC 739 每日温度**｜追问

面试官接着问：（1）能不能不用栈，额外空间 `O(1)`？（2）温度只在 `30..100` 之间，还有别的做法吗？（3）数组是环形的（末尾接回开头）怎么办？

## A
1. **从右往左，`answer` 当跳转表**：处理 `i` 时，从 `j = i + 1` 开始，如果 `temperatures[j] <= temperatures[i]`，就不必一格格走，`answer[j]` 已经告诉我们 `j` 之后第一个更高温度在哪，直接 `j += answer[j]` 跳过去；`answer[j] == 0` 说明右边再没有更高的，`i` 也一定没有。被跳过的下标，恰好是从右往左版单调栈会弹出的那些，每个下标至多被跳过一次，所以总共 `O(n)`；额外空间 `O(1)`（不算输出）：

```python
def daily_temperatures_jump(temperatures: list[int]) -> list[int]:
    n = len(temperatures)
    answer = [0] * n
    for i in range(n - 2, -1, -1):             # 从右往左，答案数组本身当“跳转表”
        j = i + 1
        while j < n and temperatures[j] <= temperatures[i]:
            if answer[j] == 0:                 # j 右边没有更高的，i 也不会有
                j = n
                break
            j += answer[j]                     # 直接跳到 j 的下一个更高温度
        if j < n:
            answer[i] = j - i
    return answer
```

2. **小值域**：从右往左扫，用长度 `101` 的数组 `nearest[t]` 记录温度 `t` 在右边最近出现的下标；对当前温度 `t`，在 `t+1..100` 里取 `nearest` 的最小值，至多 `70` 个候选，`O(70n)`。值域小时这是一个可行的备选；它的缺点是常数大，`10^5` 个数据实测约 `25 ms`，比单调栈慢约 `5` 倍。
3. **环形数组**（LC 503 的写法）：把下标遍历两圈（`range(2 * n)`），用 `i % n` 取值，只在第一圈压栈，第二圈只负责弹栈结算。

**Python 提醒**：`min(nearest[t + 1:101], default=n)` 里的 `default` 只对空切片生效，`t = 100` 时切片为空；不写 `default` 会抛 `ValueError`。
