---
id: tlc-matchsticks-to-square-4-followup
node: b.matchsticks-to-square
type: qa
step: 4
---
## Q
**LC 473 火柴拼正方形**｜追问

面试官接着问：（1）不想靠剪枝碰运气，有没有复杂度有保证的做法？（2）改成分成 `k` 份？（3）火柴数增加到几十根怎么办？

## A
1. **状态压缩 DP**：`dp[mask]` 表示用掉 `mask` 对应的火柴后，当前正在拼的那条边已有的长度（对 `side` 取模）；不可达记 `-1`。
```python
def makesquare_dp(matchsticks: list[int]) -> bool:
    total = sum(matchsticks)
    if total % 4:
        return False
    side = total // 4
    n = len(matchsticks)
    dp = [-1] * (1 << n)                       # dp[mask]：用掉 mask 里的火柴后，当前这条边已凑的长度；-1 不可达
    dp[0] = 0
    for mask in range(1 << n):
        if dp[mask] < 0:
            continue
        for i in range(n):
            if not mask >> i & 1 and dp[mask] + matchsticks[i] <= side:
                dp[mask | 1 << i] = (dp[mask] + matchsticks[i]) % side
    return dp[-1] == 0
```
`[1,1,2,2,2]` → `True`，`[3,3,3,3,4]` → `False`。时间 `O(2^n · n)`，`n = 15` 约 `5 · 10^5` 次操作，与输入内容无关；空间 `O(2^n)`。
2. **分成 `k` 份（LC 698）**：边长 `total / k`，回溯里的 `4` 换成 `k`，同样做「同长度的边只试一次」；状压 DP 里 `% side` 的做法不变，`dp[-1] == 0` 判断成功。
3. **几十根火柴**：`2^n` 状态放不下，回溯加强剪枝（相同长度的火柴只当作一种、先填满再换下一条边）仍可能很慢；这时问题是 NP 难，通常只能近似或限制规模。

**Python 提醒**：`not mask >> i & 1` 的优先级是 `not ((mask >> i) & 1)`，因为移位高于按位与，按位与高于 `not`；`mask | 1 << i` 是 `mask | (1 << i)`，移位优先于按位或。写位运算时不确定就加括号。
