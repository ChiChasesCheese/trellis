---
id: leetcode-q-parallel-courses-iii-pattern
node: graphs-traversal.directed-acyclic-graph
type: qa
anki: 1787776730726
tags: [lc::2050, leetcode, pattern, recall]
---
## Q
给定课程依赖关系（DAG）和每门课耗时，求完成所有课程的最短时间（并行选课），如何建模？

## A
本质是求 DAG 上的最长路径（关键路径）。定义 finish[v] = 完成课程 v（含其自身耗时）所需的最早时间。递推：finish[v] = time[v] + max(finish[u] for u 是 v 的前驱)。两种实现方式：1) 记忆化 DFS，dfs(v) 返回从 v 出发能到达的最深路径耗时，自顶向下累加；2) Kahn 拓扑排序 BFS，入度为 0 的节点入队，出队时把当前 finish 值传递并更新后继节点的 finish（取 max），入度归零后入队。答案是所有节点 finish 值的最大值。

**Evidence**

两个实现都在 note 中：minimumTime0 用 @cache 装饰的 dfs(node) 做记忆化递归；minimumTime 用 deque 实现 Kahn 算法，用 ind 数组统计入度，用 node_time[nxt-1] = max(node_time[nxt-1], node_time[node-1] + time[nxt-1]) 做状态转移，最终返回 max(node_time)。

[原文 ↗](obsidian://open?vault=lc&amp;file=questions%2F2050%20-%20Parallel%20Courses%20III)
