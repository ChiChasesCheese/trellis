---
slug: twisted-mirror-path-count
---
## Q
**LC 3665 统计镜子反射路径数目**｜Medium

`m x n` 网格里 `1` 是镜子。机器人从 `(0,0)` 只能右或下走到 `(m-1,n-1)`；向右进入镜子被转向下、向下进入镜子被转向右，移到镜子的下方或右方格子（可连续反射，出界则无效）。求路径数，对 `10^9+7` 取模。

## A
**一句话。** 反射结果取决于进入方向，所以拆成 `right`、`down` 两张表：镜子把向右进入转成对下方的向下进入，向下进入转成对右方的向右进入。

```python
def mirror_paths(grid):
    MOD = 10**9 + 7
    m, n = len(grid), len(grid[0])
    R = [[0] * n for _ in range(m)]    # R：向右试图进入 (i,j)
    D = [[0] * n for _ in range(m)]    # D：向下试图进入 (i,j)
    R[0][0] = 1
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            if j:                         # 来自左边
                a, b = R[i][j-1], D[i][j-1]
                # 镜子：只有向下进入的被转向右
                R[i][j] = b if grid[i][j-1] else (a+b) % MOD
            if i:                         # 来自上边
                a, b = R[i-1][j], D[i-1][j]
                # 镜子：只有向右进入的被转向下
                D[i][j] = a if grid[i-1][j] else (a+b) % MOD
    return (R[-1][-1] + D[-1][-1]) % MOD
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 只开一张 `dp` 表：同一面镜子被向右和向下进入的去向不同，混在一起就错。
- 把镜子当停靠点继续走：机器人不会停在镜子上，镜子只是中转。

**追问。**
- 反射出界怎么处理？：DP 里没有对应格子，自然不被累加。

**同模式。** LC 62 不同路径、LC 63 不同路径 II、LC 1301 最大得分的路径数目、LC 576 出界的路径数
