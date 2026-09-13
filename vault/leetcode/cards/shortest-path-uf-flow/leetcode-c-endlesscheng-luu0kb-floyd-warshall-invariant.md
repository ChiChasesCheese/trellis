---
id: leetcode-c-endlesscheng-luu0kb-floyd-warshall-invariant
node: shortest-path-uf-flow.floyd-warshall
type: cloze
anki: 1787272459181
tags: [concept-cloze, invariant, leetcode, recall]
---
Floyd 的第 k 轮后，路径内部只允许使用编号不超过 k 的 {{c1::中转点}}。

处理完中转点 k 后，dist[i][j] 是只允许 0..k 作内部点的最短路；每轮 k 固定后再更新所有 i,j；dist[i][i]=0，无法到达为无穷大

**Evidence**

三、图论：Floyd

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.12%20-%20%E5%9B%BE%E8%AE%BA%EF%BC%9AFloyd-Warshall)
