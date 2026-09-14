---
id: leetcode-c-endlesscheng-g0n5iy-graph-dfs-state-and-timestamps-recognition
node: graphs-traversal.graph-dfs-state-and-timestamps
type: cloze
anki: 1787272482480
tags: [concept-cloze, leetcode, recall, recognition]
---
路径合法性依赖累计摘要，或需快速判断树上祖先关系时，用 {{c1::DFS 状态与时间戳}}。

当路径合法性依赖累计状态时，将状态随 DFS 传递；当要快速判断树上祖先关系时，记录进入和退出时间，把子树变成连续时间区间。

**Evidence**

图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.23%20-%20DFS%20%E7%8A%B6%E6%80%81%E4%B8%8E%E6%97%B6%E9%97%B4%E6%88%B3)
