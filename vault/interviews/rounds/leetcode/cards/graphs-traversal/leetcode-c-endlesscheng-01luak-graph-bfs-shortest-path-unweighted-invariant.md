---
id: leetcode-c-endlesscheng-01luak-graph-bfs-shortest-path-unweighted-invariant
node: graphs-traversal.graph-bfs-shortest-path-unweighted
type: cloze
anki: 1787272408105
tags: [concept-cloze, invariant, leetcode, recall]
---
BFS 最短路正确性的核心不变量是：队列按 {{c1::到起点的距离单调不减}} 的顺序出队，因此节点第一次被赋值的 dis 就是最终答案。

队列中节点按到起点的距离单调不减出队（BFS 分层性质）；一个节点第一次被更新 dis 时，该值就是最终最短路，之后不会再变小

**Evidence**

§1.2 广度优先搜索（BFS）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.02%20-%20BFS%20%E6%B1%82%E5%8D%95%E6%BA%90%E6%9C%80%E7%9F%AD%E8%B7%AF%EF%BC%88%E6%97%A0%E6%9D%83%E5%9B%BE%EF%BC%89)
