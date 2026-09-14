---
id: leetcode-c-endlesscheng-g0n5iy-zero-one-bfs-invariant
node: shortest-path-uf-flow.zero-one-bfs
type: cloze
anki: 1787272482881
tags: [concept-cloze, invariant, leetcode, recall]
---
0-1 BFS 中经 0 权边松弛成功的节点必须加入 {{c1::队首}}。

双端队列中的候选距离保持非递减处理顺序；0 权松弛后的节点必须先于当前距离加一的候选处理

**Evidence**

图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.24%20-%20%E5%9B%BE%E8%AE%BA%EF%BC%9A0-1%20BFS)
