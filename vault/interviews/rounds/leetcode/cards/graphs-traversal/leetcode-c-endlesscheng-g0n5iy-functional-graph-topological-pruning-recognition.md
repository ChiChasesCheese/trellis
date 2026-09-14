---
id: leetcode-c-endlesscheng-g0n5iy-functional-graph-topological-pruning-recognition
node: graphs-traversal.functional-graph-topological-pruning
type: cloze
anki: 1787272481280
tags: [concept-cloze, leetcode, recall, recognition]
---
每个节点恰有一个后继，且需要分离环与入树时，用 {{c1::基环树拓扑剥离}}。

每个节点出度为一的函数图由若干环及其入树组成；先拓扑剥离所有非环节点，同时传播树链 DP，剩余节点即为环。

**Evidence**

图论

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.19%20-%20%E5%9F%BA%E7%8E%AF%E6%A0%91%E6%8B%93%E6%89%91%E5%89%A5%E7%A6%BB)
