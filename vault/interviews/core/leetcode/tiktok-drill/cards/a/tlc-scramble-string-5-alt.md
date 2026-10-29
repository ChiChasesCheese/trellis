---
id: tlc-scramble-string-5-alt
node: a.scramble-string
type: qa
step: 5
---
## Q
**LC 87 扰乱字符串**｜另一种解法

不用递归，怎样自底向上填表？它和记忆化搜索各适合什么时候？

## A
**思路。** `dp[L][i][j]` 表示 `s1[i:i+L]` 能否扰乱成 `s2[j:j+L]`。长度 1 时直接比较字符；长度 `L` 只依赖更短的长度，所以按 `L` 从小到大填，转移与记忆化版本相同。

```python
def is_scramble_table(s1: str, s2: str) -> bool:
    n = len(s1)
    # dp[length][i][j]：s1[i : i+length] 能否扰乱成 s2[j : j+length]
    dp = [[[False] * n for _ in range(n)] for _ in range(n + 1)]
    for i in range(n):
        for j in range(n):
            dp[1][i][j] = s1[i] == s2[j]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            for j in range(n - length + 1):
                dp[length][i][j] = any(
                    (dp[k][i][j] and dp[length - k][i + k][j + k])               # 不交换
                    or (dp[k][i][j + length - k] and dp[length - k][i + k][j])   # 交换
                    for k in range(1, length)
                )
    return dp[n][0][0]
```

运行：`"great", "rgeat"` → `True`，`"abcde", "caebd"` → `False`，`"a", "a"` → `True`。

**复杂度。** 时间 `O(n^4)`，空间 `O(n^3)`，没有递归。

**取舍。** 填表版会算满所有 `O(n^3)` 个状态，没有计数剪枝，`n = 30` 时一般比记忆化慢一个数量级，但顺序固定、没有递归深度和缓存开销，适合要求非递归或要改写成其他语言的场合。记忆化只访问从 `(0, 0, n)` 出发真正可达的状态，配合计数剪枝通常快得多，代码也更贴近「切一刀、交换或不交换」的定义。面试里先写记忆化，再说明可以改成按长度填表。
