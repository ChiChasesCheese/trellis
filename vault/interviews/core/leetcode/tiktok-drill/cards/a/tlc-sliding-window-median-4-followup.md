---
id: tlc-sliding-window-median-4-followup
node: a.sliding-window-median
type: qa
step: 4
---
## Q
**LC 480 滑动窗口中位数**｜追问

面试官接着问：（1）如果允许用 `SortedList` 呢？（2）只有插入、没有滑出（数据流中位数）？（3）要窗口里第 `p` 小的数，而不是中位数？

## A
1. **`SortedList`**（`sortedcontainers` 库，LeetCode 环境自带，但不是标准库）：`add`、`remove` 都是约 `O(log k)`，按下标取中间元素，代码最短，`O(n log k)`。

```python
# usage：需要第三方库 sortedcontainers
from sortedcontainers import SortedList


def median_sliding_window_sl(nums: list[int], k: int) -> list[float]:
    window = SortedList(nums[:k])
    res: list[float] = []
    for i in range(k, len(nums) + 1):
        res.append((window[(k - 1) // 2] + window[k // 2]) / 2)   # 奇数时两个下标相同
        if i < len(nums):
            window.remove(nums[i - k])
            window.add(nums[i])
    return res
```

面试中先确认能否用第三方库；不能就写对顶堆。
2. **数据流中位数（LC 295）**：没有删除，就没有 `delayed`；插入时先进 `small`，把 `small` 堆顶挪到 `large`，若 `large` 更多再挪回一个。每步 `O(log n)`。
3. **第 `p` 小**：把不变量 2 改成「`small` 的有效个数恰为 `p`」，答案是 `small` 的堆顶；平衡、延迟删除的逻辑不变。

**Python 提醒**：`heapq` 没有「删除任意元素」；`list.remove` 加 `heapify` 每次 `O(k)`，而延迟删除把代价摊到元素浮上堆顶的那一刻。
