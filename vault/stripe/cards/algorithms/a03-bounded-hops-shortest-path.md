---
id: a03-bounded-hops-shortest-path
node: stripe.algorithms
type: qa
---

## Q
当题目要求"最多经过 K 站/跳的最短路/最低价"时，为什么不能直接用 Dijkstra？

## A
标准做法是 **Bellman-Ford 按轮松弛**：跑 K+1 轮，每轮基于上一轮的 dist **副本**松弛一次，
保证每一轮只能多走一跳。Dijkstra 只保证全局最短路，不天然带"跳数上限"这个维度，
而 Bellman-Ford 按轮推进正好把"轮数"和"跳数"对应起来，天然满足限制。

**最易错处**：如果直接在原地更新 dist（不用副本），会导致一轮内传播多跳，
本质上退化成了不限跳数的最短路，答案偏小。
