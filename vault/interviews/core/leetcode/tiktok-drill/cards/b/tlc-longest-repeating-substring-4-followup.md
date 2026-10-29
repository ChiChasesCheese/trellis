---
id: tlc-longest-repeating-substring-4-followup
node: b.longest-repeating-substring
type: qa
step: 4
---
## Q
**LC 1062 最长重复子串**｜追问

面试官接着问：（1）不用二分，能不能直接 `O(n^2)` 的 DP？（2）`n` 增大到 `3 * 10^4`，二分加集合还行吗？（3）要返回具体的子串？

## A
1. **DP**：`dp[i][j]` 表示以 `s[i-1]` 和 `s[j-1]`（`i < j`）结尾的最长公共后缀长度；相同则等于左上角 `dp[i-1][j-1] + 1`，不同则为 `0`；第 `0` 行、第 `0` 列是空前缀，全为 `0`；答案是全表最大值：

```python
def longest_repeating_dp(s: str) -> int:
    n = len(s)
    # dp[i][j]（i < j）：以 s[i-1] 和 s[j-1] 结尾的最长公共后缀长度
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    best = 0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):      # 只填 j > i：同一个子串不能和自己配对
            if s[i - 1] == s[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                best = max(best, dp[i][j])
    return best
```
   运行：`"abcd"` → `0`，`"abbaba"` → `2`，`"aabcaabdaab"` → `3`，`"aaaa"` → `3`。时间 `O(n^2)`（`n = 2000` 约 `2 * 10^6` 次更新，约 `0.1` 秒），空间 `O(n^2)`；不需要集合占用的大量内存，复杂度上界也不依赖哈希。空间可以压到 O(n)：见 Python 工具箱「DP 降维」。
2. **`n = 3 * 10^4`**：二分外层不变，判定 `has_repeat(L)` 用滚动哈希（Rabin-Karp）把每个窗口的哈希用 `O(1)` 更新，整次判定 `O(n)`，总计 `O(n log n)`；哈希相同时再比对真实子串，防止碰撞，这就是 LC 1044 的做法。`O(n^2)` 的 DP 在 `n = 3 * 10^4` 时约 `4.5 * 10^8` 次更新，Python 里跑不完。
3. **返回子串**：`has_repeat` 改成返回第一个重复窗口的起点（没有返回 `-1`），二分结束时记录最近一次成功的 `(起点, 长度)`，最后切片。DP 版则在刷新 `best` 时同时记下 `i`。

**Python 提醒**：`dp = [[0] * (n + 1) for _ in range(n + 1)]` 每行是独立的列表；写成 `[[0] * (n + 1)] * (n + 1)` 所有行是同一个列表，填一格等于同时改所有行。
