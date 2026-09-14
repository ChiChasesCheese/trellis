---
id: leetcode-c-endlesscheng-01luak-graph-topological-sort-kahn-recognition
node: graphs-traversal.graph-topological-sort-kahn
type: cloze
anki: 1787272408604
tags: [concept-cloze, leetcode, recall, recognition]
---
当题目给出若干“先修课程”式的有向依赖约束，要求给出一个合法学习顺序或判断是否有环时，应使用 {{c1::拓扑排序}}。

对有向无环图，用入度为 0 的节点作为初始队列，逐步“上完先修课”并减少后继节点入度，得到一个满足所有边方向约束的线性序；若最终排序节点数少于 n，说明图中有环。

**Evidence**

§2.1 拓扑排序

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.04%20-%20%E6%8B%93%E6%89%91%E6%8E%92%E5%BA%8F%EF%BC%88Kahn%20%E7%AE%97%E6%B3%95%EF%BC%89)
