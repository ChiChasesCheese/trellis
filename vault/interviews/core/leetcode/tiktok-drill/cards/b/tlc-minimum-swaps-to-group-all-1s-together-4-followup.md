---
id: tlc-minimum-swaps-to-group-all-1s-together-4-followup
node: b.minimum-swaps-to-group-all-1s-together
type: qa
step: 4
---
## Q
**LC 1151 最少交换次数来组合所有的 1**｜追问

面试官接着问：（1）数组是**环形**的，首尾相连也算连在一起（LC 2134）？（2）只允许交换**相邻**元素？（3）要返回的是某个最优方案对应的窗口位置？

## A
1. **环形数组**：目标窗口可以跨越首尾。把数组首部的前 `w - 1` 个元素接到尾部，再在拼接后的数组上滑动长度为 `w` 的窗口，只取起点在 `[0, n)` 内的窗口。`[0,1,0,1,1,0,0]` → `1`，`[0,1,1,1,0,0,1,1,0]` → `2`，`[1,1,0,0,1]` → `0`。
```python
from itertools import accumulate

def min_swaps_circular(data: list[int]) -> int:
    w, n = sum(data), len(data)
    if w == 0:
        return 0
    ext = data + data[:w - 1]                 # 展开成线性
    pre = list(accumulate(ext, initial=0))
    return w - max(pre[i + w] - pre[i] for i in range(n))
```
2. **只能交换相邻元素**（LC 1703 的变体）：不再是「数窗口里的 `0`」。设 `1` 的下标为 `p_0 < p_1 < ...`，先令 `q_i = p_i - i` 去掉它们之间自然的间隔，则把所有 `1` 聚到一起的最小相邻交换次数，是 `q_i` 到其中位数的距离之和。直觉是：绝对值之和在中位数处最小。
3. **返回窗口位置**：滑动时刷新 `best` 的同时记下对应的起点 `start = i - w + 1`；窗口 `[start, start + w)` 就是只需最少交换的目标位置。

**Python 提醒**：`accumulate(data, initial=0)` 会在前面多放一个 `0`，所以前缀数组长度是 `n + 1`，区间 `[i, i + w)` 的和是 `pre[i + w] - pre[i]`；不加 `initial=0` 时下标要整体偏一位，容易写出 off-by-one。`data[:w - 1]` 在 `w == 1` 时是空切片，拼接后不变，行为正确。
