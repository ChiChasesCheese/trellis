---
id: tlc-distinct-subsequences-2-code
node: b.distinct-subsequences
type: qa
step: 2
---
## Q
**LC 115 不同的子序列**｜写出 Python 实现

字符串 `s`、`t`（长度各在 `1` 到 `1000`，由英文字母组成）。返回 `s` 的子序列中等于 `t` 的个数（不同下标选法算不同方案）。结果保证在 32 位有符号整数范围内。要求 `O(mn)` 时间。

## A
**思路。** `dp[j]` 表示当前已读前缀里 `t[:j]` 的出现次数，`dp[0] = 1`。读入 `s` 的每个字符 `ch`，从大到小遍历 `j`：若 `t[j - 1] == ch`，用这个字符去配 `t[j - 1]`，方案数加上读入 `ch` 之前的 `dp[j - 1]`；不等则 `dp[j]` 不变（不用这个字符）。

```python
def num_distinct(s: str, t: str) -> int:
    dp = [1] + [0] * len(t)                # dp[j]：s 目前读过的前缀里，t[:j] 作为子序列出现的次数
    for ch in s:
        for j in range(len(t), 0, -1):     # 倒序：dp[j - 1] 还是读 ch 之前的旧值
            if t[j - 1] == ch:
                dp[j] += dp[j - 1]
    return dp[-1]
```

运行：`("rabbbit", "rabbit")` → `3`，`("babgbag", "bag")` → `5`，`("a", "aa")` → `0`，`("aaa", "a")` → `3`，`("abc", "abc")` → `1`。

**复杂度。** 时间 `O(mn)`：外层 `m` 个字符，内层 `n` 步；空间 `O(n)`：一个长度 `n + 1` 的数组。

**写法要点。** `[1] + [0] * len(t)` 一行建出带初值的数组；`range(len(t), 0, -1)` 倒序遍历 `j = n, n-1, ..., 1`，是一维 0/1 背包式 DP 的标配写法；`dp[-1]` 读最后一个元素，省去 `len(t)`；`dp[j] += dp[j - 1]` 原地累加，计数 DP 的转移就是加法，不需要 `max`。
