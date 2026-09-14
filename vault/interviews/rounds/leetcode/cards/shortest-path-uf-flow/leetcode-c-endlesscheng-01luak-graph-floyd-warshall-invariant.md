---
id: leetcode-c-endlesscheng-01luak-graph-floyd-warshall-invariant
node: shortest-path-uf-flow.graph-floyd-warshall
type: cloze
anki: 1787272409905
tags: [concept-cloze, invariant, leetcode, recall]
---
Floyd 算法作为三维 DP，其阶段变量 k 必须放在{{c1::最外层循环}}，表示只允许经过编号不超过 k 的中转点。

外层循环变量 k 必须放在最外层，表示“只允许经过编号 ≤ k 的中转点”，这是 DP 的阶段变量，不能与 i、j 循环顺序互换；f[i][j] 在整个过程中单调不增

**Evidence**

§3.2 全源最短路：Floyd 算法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.08%20-%20%E5%85%A8%E6%BA%90%E6%9C%80%E7%9F%AD%E8%B7%AF%EF%BC%9AFloyd%20%E7%AE%97%E6%B3%95)
