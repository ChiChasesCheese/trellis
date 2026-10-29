---
id: tlc-python-dp-space-compression-3-one-row
node: python.dp-space-compression
type: qa
step: 3
---
## Q
**DP 降维｜一行原地：读上方旧值，读左边新值**

不同路径（LC 62）只用一个数组时，为什么内层 `j` 从左往右更新是对的？从右往左会得到什么？

## A
一维的 `dp[j]` 扮演两个角色：还没覆盖时是上一行的 `dp[i-1][j]`（上方，旧值），覆盖之后是本行的 `dp[i][j]`。

```python
def paths_one_row(m: int, n: int, forward: bool = True) -> int:
    dp = [1] * n                            # 第 0 行
    for i in range(1, m):
        cols = range(1, n) if forward else range(n - 1, 0, -1)
        for j in cols:
            dp[j] = dp[j] + dp[j - 1]       # 上方（旧）+ 左边（新）
    return dp[-1]

print(paths_one_row(3, 7), paths_one_row(3, 7, forward=False))   # 28 4
```

- 公式要的是 `dp[i-1][j] + dp[i][j-1]`：上方是**旧值**，左边是**新值**。
- 正序：算 `dp[j]` 时它还没被覆盖（旧，正是上方），`dp[j-1]` 已经被覆盖（新，正是左边），刚好对上。
- 倒序：`dp[j-1]` 还没覆盖，读到的是 `dp[i-1][j-1]`（左上角），公式变了，`(3, 7)` 得到 `4`，正确是 `28`。
- 判断方法：逐个检查要读的格子——要旧值的必须还没被写，要新值的必须已经被写。
