---
id: tlc-find-two-non-overlapping-sub-arrays-each-with-target-sum-4-followup
node: a.find-two-non-overlapping-sub-arrays-each-with-target-sum
type: qa
step: 4
---
## Q
**LC 1477 找两个和为目标值且不重叠的子数组**｜追问

面试官接着问：（1）如果元素可以是负数或零？（2）如果要选 `k` 个互不重叠的子数组？（3）要返回这两个子数组的位置？分别怎么改。

## A
1. **有负数或零**：窗口和不再单调，滑动窗口失效。改用前缀和 + 哈希表：`seen[pre]` 记录某个前缀和最近一次出现的下标，`pre - target` 在表中就找到了一个以当前下标结尾的目标子数组（取最近的，长度最短）：

```python
def min_sum_of_lengths_prefix(arr: list[int], target: int) -> int:
    n = len(arr)
    INF = n + 1
    seen: dict[int, int] = {0: -1}               # 前缀和 -> 最近一次出现的下标
    best = [INF] * (n + 1)
    ans = INF
    pre = 0
    for right, x in enumerate(arr):
        pre += x
        best[right + 1] = best[right]
        if (left := seen.get(pre - target)) is not None:   # arr[left+1..right] 的和为 target
            length = right - left
            ans = min(ans, best[left + 1] + length)
            best[right + 1] = min(best[right + 1], length)
        seen[pre] = right
    return -1 if ans == INF else ans
```

2. **`k` 个子数组**：状态加一维，`dp[j][i]` 表示在 `arr[:i]` 里选 `j` 个互不重叠目标子数组的最小总长度，窗口找到 `[left, right]` 时 `dp[j][right+1] = min(dp[j][right], dp[j-1][left] + length)`。用完整二维表，时间 `O(nk)`；空间可以压到 `O(n)`：见 Python 工具箱「DP 降维」。
3. **返回位置**：`best` 里改存 `(长度, 起点)` 元组，比较时元组自然先比长度。

**Python 提醒**：海象运算符 `(left := seen.get(...)) is not None` 不能写成 `if (left := ...)`，因为下标 `0` 为假值；`0` 是合法的下标，必须显式比较 `is not None`。
