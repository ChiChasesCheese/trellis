---
id: leetcode-q-detonate-the-maximum-bombs-pattern
node: math-number-theory.geometry
type: qa
anki: 1787102261831
tags: [lc::2101, leetcode, pattern, recall]
---
## Q
如何求「引爆炸弹」（LC 2101）能引爆的最大炸弹数？

## A
对每对炸弹 (a, b)，若 a 到 b 的欧氏距离 ≤ a 的半径，则建有向边 a→b（a 炸能引爆 b，不代表 b 炸能引爆 a）。建图后枚举每个炸弹作为起点做 BFS/DFS，统计可达节点数，取所有起点中的最大值即为答案。核心不变量：图是有向的（因为半径可能不同），因此必须枚举所有起点分别求可达集合，不能只跑一次。复杂度 O(n^2) 建图 + O(n) 次 BFS(O(n+e))，整体 O(n^3)。

**Evidence**

g[idx1].append(idx2) 仅当 dist <= r1（单向判断两次，分别对应 r1、r2）；随后 max(bfs(i) for i in range(n)) 枚举所有起点取最大可达数。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F2101%20-%20Detonate%20the%20Maximum%20Bombs)
