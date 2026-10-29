---
id: tlc-distinct-subsequences-4-followup
node: a.distinct-subsequences
type: qa
step: 4
---
## Q
**LC 115 不同的子序列**｜追问

面试官接着问：（1）结果不保证在 32 位内，要对 `10^9 + 7` 取模？（2）要输出其中一种具体选法？（3）`s` 极长、`t` 很短，或者反过来，怎么优化？（4）表太大怎么办？

## A
1. **取模**：在累加处取模，其他不变：

```python
def num_distinct_mod(s: str, t: str, mod: int = 10**9 + 7) -> int:
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = 1
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j]
            if s[i - 1] == t[j - 1]:
                dp[i][j] = (dp[i][j] + dp[i - 1][j - 1]) % mod
    return dp[m][n]
```
   Python 的 `int` 不溢出，取模只是为了符合题目要求的输出范围；Java / C++ 里必须每次取模，否则中间值会溢出。
2. **输出一种选法**：完整的二维表直接回溯，从 `(m, n)` 出发：若 `dp[i][j] > dp[i-1][j]`（说明用了 `s[i-1]`）且 `s[i-1] == t[j-1]`，记录下标 `i - 1`，退到 `(i-1, j-1)`；否则退到 `(i-1, j)`。
3. **规模不对称**：若 `len(t) > len(s)`，直接返回 `0`。还可以先把 `s` 过滤成只含 `t` 中出现过的字符，缩短外层循环和表的行数。
4. 空间可以压到 O(n)：见 Python 工具箱「DP 降维」。

**Python 提醒**：主循环从 `1` 开始，`s[i - 1]`、`t[j - 1]` 才是第 `i`、`j` 个字符；如果循环从 `0` 开始，`s[i - 1]` 在 `i = 0` 时是 `s[-1]`（负下标取到最后一个字符）而不报错，结果悄悄出错。
