---
id: tlc-distinct-subsequences-4-followup
node: b.distinct-subsequences
type: qa
step: 4
---
## Q
**LC 115 不同的子序列**｜追问

面试官接着问：（1）结果不保证在 32 位内，要对 `10^9 + 7` 取模？（2）要输出其中一种具体选法？（3）`s` 极长、`t` 很短，或者反过来，怎么优化？

## A
1. **取模**：在累加处取模，其他不变：

```python
def num_distinct_mod(s: str, t: str, mod: int = 10**9 + 7) -> int:
    dp = [1] + [0] * len(t)
    for ch in s:
        for j in range(len(t), 0, -1):
            if t[j - 1] == ch:
                dp[j] = (dp[j] + dp[j - 1]) % mod
    return dp[-1]
```
   Python 的 `int` 不溢出，取模只是为了符合题目要求的输出范围；Java / C++ 里必须每次取模，否则中间值会溢出。
2. **输出一种选法**：保留二维表 `f[i][j]`，从 `(m, n)` 回溯：若 `f[i][j] > f[i-1][j]`（说明用了 `s[i-1]`）且 `s[i-1] == t[j-1]`，记录下标 `i - 1`，退到 `(i-1, j-1)`；否则退到 `(i-1, j)`。一维压缩版本丢了历史，不能回溯。
3. **规模不对称**：时间 `O(mn)` 对 `m`、`n` 是对称的，一维数组的长度是 `len(t)`，所以 `t` 短时更省空间。若 `len(t) > len(s)`，直接返回 `0`。还可以先把 `s` 过滤成只含 `t` 中出现过的字符，缩短外层循环。

**Python 提醒**：`range(len(t), 0, -1)` 的第二个参数 `0` 是开区间端点，所以 `j` 最小为 `1`；写成 `range(len(t), -1, -1)` 会多出 `j = 0`，访问 `t[-1]`（负下标取到最后一个字符）而不报错，结果悄悄出错。
