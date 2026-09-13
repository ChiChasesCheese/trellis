---
id: leetcode-c-endlesscheng-yixpxw-grid-connected-components-dfs-invariant
node: graphs-traversal.grid-connected-components-dfs
type: cloze
anki: 1787272404205
tags: [concept-cloze, invariant, leetcode, recall]
---
网格 DFS 的关键不变量是：格子 {{c1::进入 DFS 时立即标记为已访问}}，因此不会被重复计入同一或不同连通块。

进入 DFS 时立刻标记 visited，保证每个格子至多属于一个连通块。；DFS 只沿合法、可通行且未访问的相邻格子扩展。；外层扫描中每次新 DFS 恰好对应一个尚未统计的连通块。

**Evidence**

一、网格图 DFS

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F04.01%20-%20%E7%BD%91%E6%A0%BC%E8%BF%9E%E9%80%9A%E5%9D%97%20DFS)
