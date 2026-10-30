---
id: tlc-daily-temperatures-2-code
node: b.daily-temperatures
type: qa
step: 2
---
## Q
**LC 739 每日温度**｜写出 Python 实现

整数数组 `temperatures`（长度 `1..10^5`，每个值在 `30..100`）。返回 `answer`，`answer[i]` 是第 `i` 天之后第一个更高温度出现在几天后，没有则 `0`。要求 `O(n)`。

## A
**思路。** 用栈存还没等到更高温度的下标，保持对应温度不增；来了新温度 `t` 就弹出所有比它低的下标并记录距离，然后把当前下标压栈。

```python
def daily_temperatures(temperatures: list[int]) -> list[int]:
    answer = [0] * len(temperatures)
    stack: list[int] = []              # 还在等更高温度的下标；对应温度自底向顶非严格递减
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:   # t 是它们等到的第一个更高温度
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)
    return answer                      # 栈里剩下的永远没等到，保持 0
```

运行：`[73,74,75,71,69,72,76,73]` → `[1, 1, 4, 2, 1, 1, 0, 0]`，`[30,40,50,60]` → `[1, 1, 1, 0]`，`[30,60,90]` → `[1, 1, 0]`，`[50]` → `[0]`，`[70,70,70]` → `[0, 0, 0]`。

**复杂度。** 时间 `O(n)`：内层 `while` 的弹出次数总和不超过入栈次数 `n`；空间 `O(n)`：严格递减序列时栈里装着全部下标。

**写法要点。** `enumerate` 同时拿下标和值；`temperatures[stack[-1]] < t` 里 `stack and` 先判空，避免空栈取下标；`answer` 先全部填 `0`，没等到更高温度的下标就不用再处理；栈用 `list` 的 `append` / `pop()`，都是尾部 `O(1)`。
