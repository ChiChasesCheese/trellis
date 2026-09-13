---
id: leetcode-c-endlesscheng-01luak-graph-functional-graph-cycle-recognition
node: graphs-traversal.graph-functional-graph-cycle
type: cloze
anki: 1787272409207
tags: [concept-cloze, leetcode, recall, recognition]
---
当图中每个节点的出度恰好为 1，且题目暗示存在唯一环时，应识别为{{c1::基环树}}（内向基环图）结构。

每个节点恰好一条出边（或每条边视为唯一后继）构成的图称为基环树/内向基环图，整体结构是“一个环 + 若干挂在环上的树”；通过反复剥除入度为 0 的叶子节点（类似拓扑排序），剩下未被剥除的节点就是环上的节点。

**Evidence**

§2.3 基环树

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.06%20-%20%E5%9F%BA%E7%8E%AF%E6%A0%91-%E5%86%85%E5%90%91%E5%9B%BE%E6%89%BE%E7%8E%AF%EF%BC%88%E6%8B%93%E6%89%91%E5%89%A5%E5%8F%B6%EF%BC%89)
