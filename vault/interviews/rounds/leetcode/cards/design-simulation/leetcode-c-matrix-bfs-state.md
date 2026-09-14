---
id: leetcode-c-matrix-bfs-state
node: design-simulation.matrix-bfs-state
type: cloze
anki: 1787102263909
tags: [concept-cloze, leetcode, recall]
---
在矩阵BFS处理带约束（如健康值）的最短路径时，visited 集合必须记录每个坐标 (x, y) 对应的{{c1::最优约束值（如最大health）}}，而不能只记录坐标本身是否访问过，否则会导致{{c2::同一坐标的不同状态被错误地当作重复而漏掉更优路径}}。

状态元组是 (x, y, health)，同一坐标在不同 health 值下代表不同的可行状态；只用 (x,y) 去重会丢失约束维度信息。

**Evidence**

Invariants: 状态元组包含坐标和所有约束维度；visited记录(x,y)的最优约束值，避免重复。Pitfalls: visited只记坐标而遗漏约束值，导致同坐标不同状态混淆。

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%9F%A9%E9%98%B5%20BFS%20%E7%8A%B6%E6%80%81%E6%9C%80%E7%9F%AD%E8%B7%AF)
