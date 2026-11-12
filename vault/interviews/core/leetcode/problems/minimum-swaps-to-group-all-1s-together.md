---
slug: minimum-swaps-to-group-all-1s-together
---
## Q
**LC 1151 最少交换次数来组合所有的 1**｜Medium

二进制数组 `data`，可交换任意两个位置，求把所有 `1` 连成一段的最少交换次数。

## A
**一句话。** 设 `1` 共 `w` 个，答案是 `w` 减去所有长为 `w` 的定长窗口里 `1` 的最大个数。

```python
def min_swaps(data):
    w = sum(data)
    cur = sum(data[:w])
    best = cur
    for i in range(w, len(data)):
        cur += data[i] - data[i - w]   # 右进左出
        best = max(best, cur)
    return w - best
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 只试以第一个 `1` 开头的窗口：`[1,0,0,0,1,1,1]` 的窗口 `[0,1,1,1]` 只需 `1` 次，而首个窗口要 `3` 次。
- 把初始窗口漏出候选：`best` 要用第一个窗口的 `cur` 初始化。

**追问。**
- 数组是环形（LC 2134）？：把前 `w - 1` 个元素接到末尾再滑窗。
- 只允许交换相邻元素（LC 1703）？：要算每个 `1` 移到目标位置的距离和，以中位数为中心。

**同模式。** LC 2134 最少交换次数来组合所有的 1 II、LC 1004 最大连续 1 的个数 III、LC 643 子数组最大平均数 I
