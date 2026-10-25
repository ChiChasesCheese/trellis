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
1. **DP**：`dp[j]` 表示以 `s[i-1]` 和 `s[j-1]`（`i < j`）结尾的最长公共后缀长度；相同则等于 `dp[j-1] + 1`（上一行），不同则为 `0`；答案是所有 `dp` 的最大值。`j` 倒序遍历，让 `dp[j-1]` 还是上一行的值：

```python
def longest_repeating_dp(s: str) -> int:
    n = len(s)
    dp = [0] * (n + 1)                     # dp[j]：以 s[i-1] 和 s[j-1] 结尾的最长公共后缀长度
    best = 0
    for i in range(1, n + 1):
        for j in range(n, i, -1):          # j > i，倒序以便 dp[j - 1] 还是上一行
            dp[j] = dp[j - 1] + 1 if s[i - 1] == s[j - 1] else 0
            best = max(best, dp[j])
    return best
```
   运行：`"abcd"` → `0`，`"abbaba"` → `2`，`"aabcaabdaab"` → `3`，`"aaaa"` → `3`。时间 `O(n^2)`（`n = 2000` 约 `2 * 10^6` 次更新），空间 `O(n)`，不需要集合占用的大量内存，复杂度上界也不依赖哈希。
2. **`n = 3 * 10^4`**：二分外层不变，判定 `has_repeat(L)` 用滚动哈希（Rabin-Karp）把每个窗口的哈希用 `O(1)` 更新，整次判定 `O(n)`，总计 `O(n log n)`；哈希相同时再比对真实子串，防止碰撞，这就是 LC 1044 的做法。`O(n^2)` 的 DP 在 `n = 3 * 10^4` 时约 `4.5 * 10^8` 次更新，Python 里跑不完。
3. **返回子串**：`has_repeat` 改成返回第一个重复窗口的起点（没有返回 `-1`），二分结束时记录最近一次成功的 `(起点, 长度)`，最后切片。DP 版则在刷新 `best` 时同时记下 `i`。

**Python 提醒**：`dp[j] = dp[j - 1] + 1 if 条件 else 0` 中条件表达式的优先级最低，整个右边是 `(dp[j-1] + 1) if 条件 else 0`，不需要额外括号；但把它放进更大的表达式里时要加括号。
