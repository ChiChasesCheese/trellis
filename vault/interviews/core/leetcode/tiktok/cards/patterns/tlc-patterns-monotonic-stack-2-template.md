---
id: tlc-patterns-monotonic-stack-2-template
node: patterns.monotonic-stack
type: qa
step: 2
---
## Q
**单调栈（Monotonic Stack）｜模板**

写出「找每个元素右边第一个更大元素」的单调栈模板，栈里存下标还是值？比较用 `<` 还是 `<=`？

## A
栈里存**下标**（值可以由下标取到，距离也由下标算出）。栈从底到顶保持单调；新元素 `x` 来了，把所有被 `x` 「解决」的栈顶弹出。

```python
def daily_temperatures(temperatures: list[int]) -> list[int]:
    ans = [0] * len(temperatures)
    st: list[int] = []                     # 栈里是还没等到更高温度的下标，温度递减
    for i, t in enumerate(temperatures):
        while st and temperatures[st[-1]] < t:   # 严格更高才算等到
            j = st.pop()
            ans[j] = i - j
        st.append(i)
    return ans
```

运行：`[73,74,75,71,69,72,76,73]` → `[1,1,4,2,1,1,0,0]`；`[30,40,50,60]` → `[1,1,1,0]`；`[30,60,90]` → `[1,1,0]`。时间、空间 `O(n)`。

四个变体只改两处：

| 要找 | 栈内顺序 | 弹出条件 |
|---|---|---|
| 右边第一个**更大** | 递减 | `栈顶 < x` |
| 右边第一个**更小** | 递增 | `栈顶 > x` |
| 左边第一个更大 / 更小 | 同上 | 弹出前**栈顶下标**就是答案（弹空则无） |

- 比较是 `<` 还是 `<=`，取决于「相等算不算」：LC 739 要**严格**更高，所以用 `<`。
- 栈里剩下的元素就是「右边没有更大的」，结果保持初值（这里是 `0`）。
- 一次遍历同时得到「左边第一个更小」（弹出后看栈顶）和「右边第一个更小」（被谁弹出），这是 LC 84 的基础。
