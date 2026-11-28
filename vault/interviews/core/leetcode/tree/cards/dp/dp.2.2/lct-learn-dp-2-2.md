---
id: lct-learn-dp-2-2
node: dp.2.2
type: qa
step: 1
---
## Q
**动态规划 › 网格图 DP › 进阶**｜学习卡

套路是什么？

## A
**一句话。** 网格 DP 进阶：要么把额外信息放进状态（第二个人、进入方向），要么倒推让状态只剩一个量，要么在「更大才能走」的无环图上记忆化 DFS。

下图：网格 DP 进阶的三条出路。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<polygon points="120.0,20.0 129.0,7.5 211.0,7.5 220.0,20.0 211.0,32.5 129.0,32.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">正着推推不动？</text>
<rect x="11.6" y="64.5" width="96.9" height="55" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60" y="81.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">还缺信息</text>
<text x="60" y="96.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">两个人 / 方向</text>
<text x="60" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">→ 加进状态</text>
<rect x="108.0" y="64.5" width="124" height="55" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="81.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">起点需求取决于后面</text>
<text x="170" y="96.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">（地下城血量）</text>
<text x="170" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">→ 从终点倒推</text>
<rect x="241.1" y="64.5" width="93.8" height="55" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="288" y="81.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">只能走向更大</text>
<text x="288" y="96.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">的格子：无环</text>
<text x="288" y="111.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">→ 记忆化 DFS</text>
<path d="M 120.0 20.0 L 60.0 20.0 L 60.0 64.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="60.0,64.5 57.0,58.2 63.0,58.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 170.0 32.5 L 170.0 64.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,64.5 167.0,58.2 173.0,58.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 220.0 20.0 L 288.0 20.0 L 288.0 64.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="288.0,64.5 285.0,58.2 291.0,58.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="160" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">倒推：f[i][j] = max(1, min(下, 右) - d[i][j])</text>
<text x="170" y="178" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">终点右、下的哨兵设 1，其余 inf</text>
</svg>

```python
def min_hp(d):                   # 倒推：f[i][j] = 进入前至少的血量
    m, n = len(d), len(d[0])
    f = [[inf] * (n + 1) for _ in range(m + 1)]
    f[m][n - 1] = f[m - 1][n] = 1    # 仅终点的右、下是 1
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            need = min(f[i + 1][j], f[i][j + 1]) - d[i][j]
            f[i][j] = max(1, need)   # 血量任何时刻 >= 1
    return f[0][0]

def longest_path(g):             # 无环图上的记忆化 DFS
    m, n = len(g), len(g[0])
    @cache
    def go(i, j):                # 从 (i, j) 出发的最长递增路
        v, best = g[i][j], 1
        for x, y in (i+1, j), (i-1, j), (i, j+1), (i, j-1):
            if 0 <= x < m and 0 <= y < n and g[x][y] > v:
                best = max(best, go(x, y) + 1)
        return best
    return max(go(i, j) for i in range(m) for j in range(n))
```

**要点。**
- LC 174 为什么倒推？：正向要同时记当前血量和路径最低点，两个量互相牵制；倒推只需一个量「进入前至少要多少血」。
- LC 741 怎么改？：返程反过来看就是第二个人也向下 / 右走，两人同步走 `k` 步，状态 `(k, r1, r2)`，列号 `= k - r`；同一格的樱桃只摘一次。
- LC 3665 怎么改？：反射结果取决于进入方向，所以开 `right`、`down` 两张表；镜子把向右进入转成向下，向下进入转成向右。
- LC 329 为什么能记忆化？：严格递增所以没有环，每格的最长路只算一次；也可以反复剥掉出度为 `0` 的格子（拓扑排序）。

**易错点。**
- LC 174 漏掉 `max(1, ...)`：`[[5]]` 应得 `1`，会得 `-4`。
- LC 741 `r1 == r2` 时樱桃加两次：`[[1,1],[1,1]]` 得 `5`，应为 `4`。
- LC 329 严格大于写成大于等于：相等邻格成环，`[[5,5],[5,5]]` 递归爆栈，应为 `1`。

**对应题目。** LC 174 地下城游戏、LC 329 矩阵中的最长递增路径、LC 741 摘樱桃、LC 3665 统计镜子反射路径数目
