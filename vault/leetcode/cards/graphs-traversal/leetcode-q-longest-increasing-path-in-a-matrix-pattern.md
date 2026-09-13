---
id: leetcode-q-longest-increasing-path-in-a-matrix-pattern
node: graphs-traversal.directed-acyclic-graph
type: qa
anki: 1787102262358
tags: [lc::329, leetcode, pattern, recall]
---
## Q
矩阵中求最长严格递增路径（LeetCode 329），常见套路是什么？

## A
对每个格子做 DFS，只往四个方向中数值严格更大的邻居走（天然无环，无需 visited 数组），用 @cache（记忆化）缓存 dfs(i,j) 的结果=以(i,j)为起点的最长递增路径长度。递推式：dfs(i,j) = max(dfs(ni,nj) for 更大的邻居) + 1。最终答案是所有格子 dfs 值的最大值。因为严格递增保证不会成环，所以可以直接记忆化搜索而不用像普通图 DFS 那样处理访问状态。

**Evidence**

```
@cache
def dfs(i, j):
    best = 0
    for di, dj in ((0,1),(0,-1),(1,0),(-1,0)):
        ni, nj = i+di, j+dj
        if (0<=ni<m and 0<=nj<n) and matrix[ni][nj] > matrix[i][j]:
            best = max(best, dfs(ni, nj))
    return best + 1
return max(dfs(i,j) for i,j in product(range(m), range(n)))
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F329%20-%20Longest%20Increasing%20Path%20in%20a%20Matrix)
