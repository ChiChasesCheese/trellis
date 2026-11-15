---
slug: out-of-boundary-paths
---
## Q
**LC 576 出界的路径数**｜Medium

`m×n` 网格里一个球从 `(startRow, startColumn)` 出发，每次可上下左右移动一格，最多移动 `maxMove` 次。求让球出界的路径条数，对 `10⁹+7` 取模。

## A
**一句话。** 记忆化搜索：`dfs(i, j, k)` 是从 `(i, j)` 出发还剩 `k` 步的出界方案数，出界即返回 1，步数用完返回 0，其余是四个方向之和。

```python
def find_paths(m, n, maxMove, startRow, startColumn):
    MOD = 10**9 + 7
    @cache
    def dfs(i, j, k):                  # 还剩 k 步
        if not (0 <= i < m and 0 <= j < n):
            return 1                   # 已出界：这条路径成立
        if k == 0:
            return 0
        res = 0
        for a, b in ((i+1,j), (i-1,j), (i,j+1), (i,j-1)):
            res += dfs(a, b, k - 1)
        return res % MOD
    return dfs(startRow, startColumn, maxMove)
```

**复杂度。** 时间 `O(m·n·maxMove)`，空间 `O(m·n·maxMove)`。

**易错点。**
- 先判步数再判出界：出界发生在最后一步时也要计 1，必须先判出界。
- 出界后继续搜索：出界就结束，不能再从界外走。
- 忘了取模：路径数增长很快，每次相加后取模。

**追问。**
- 改成迭代 DP？：`f[k][i][j]` 为 `k` 步后在 `(i, j)` 的方案数，边缘格每多一个出界方向就累计一次答案。
- 求概率而非条数？：每步每个方向乘 `1/4`，如骑士概率那题。

**同模式。** LC 688 骑士在棋盘上的概率、LC 935 骑士拨号器、LC 62 不同路径、LC 1220 统计元音字母序列的数目
