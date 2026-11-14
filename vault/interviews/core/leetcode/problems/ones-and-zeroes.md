---
slug: ones-and-zeroes
---
## Q
**LC 474 一和零**｜Medium

二进制字符串数组 `strs`，选一个子集使 `0` 总数不超过 `m`、`1` 总数不超过 `n`，求子集最大大小。

## A
**一句话。** 二维费用的 0/1 背包：每个串花 `(零个数, 一个数)`、价值 1；`f[i][j][k]` 为前 `i` 个串在容量 `(j, k)` 下的最多个数。

```python
def find_max_form(strs, m, n):
    L = len(strs)
    f = [[[0] * (n + 1) for _ in range(m + 1)]
         for _ in range(L + 1)]
    for i, s in enumerate(strs):
        z, o = s.count('0'), s.count('1')
        for j in range(m + 1):
            for k in range(n + 1):
                best = f[i][j][k]                    # 不选
                if j >= z and k >= o:                # 选
                    best = max(best, f[i][j - z][k - o] + 1)
                f[i + 1][j][k] = best
    return f[L][m][n]
```

**复杂度。** 时间 `O(L·m·n)`，空间 `O(L·m·n)`。

**易错点。**
- 压成二维后正序枚举容量：同一个串会被选多次，变成完全背包。
- 把串长当费用：费用是 `0` 和 `1` 的个数两维，不是长度。

**追问。**
- 省空间？：去掉第一维，`j`、`k` 都从大到小枚举，`O(m·n)`。
- 求方案数？：`max` 换成相加，`f[0][0][0] = 1`。

**同模式。** LC 416 分割等和子集、LC 494 目标和、LC 879 盈利计划
