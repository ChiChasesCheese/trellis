---
id: problems-google-maps-contraction-hierarchies-mechanism
node: problems.geo.google-maps
type: qa
step: 3
tags: [grown]
---
## Q
In a road-network routing design, how does Contraction Hierarchies (CH) preprocessing let a query at serve time avoid exploring most of the graph, and why is that necessary for point-to-point routes spanning a continental-scale road network?

## A
CH orders every node by an importance heuristic and then contracts them from least to most important, one at a time: when a node is removed, a shortcut edge is added directly between any pair of its neighbors whose shortest path actually went through it, preserving distances. A query then runs a bidirectional search that only follows edges toward more-important nodes from both the origin and destination side, so it explores almost none of the low-importance local-road nodes and instead converges quickly through the highway-level shortcuts. Plain Dijkstra fails at continental scale because it settles nodes in order of raw distance from the origin, and a route spanning thousands of kilometers forces it to settle a large fraction of all nodes before reaching the destination — CH avoids this by moving that cost into a one-time offline preprocessing step instead of paying it on every query.

## Q zh
在路网路径规划设计中，Contraction Hierarchies（CH，收缩分层）的预处理是如何让查询时的搜索避免遍历图中大部分节点的？为什么这对横跨洲际尺度路网的点对点路线规划是必要的？

## A zh
CH 按某种重要性启发式给所有节点排序，然后按重要性从低到高逐个收缩（contract）节点：移除一个节点时，如果它的某两个邻居之间的最短路径确实经过它，就在这两个邻居之间直接加一条保留原距离信息的捷径边（shortcut）。查询时做一次双向搜索，起点侧和终点侧都只沿着通向更重要节点的方向扩展，这样几乎不会遍历不重要的本地道路节点，而是很快通过高速公路级别的捷径收敛。朴素 Dijkstra 在洲际尺度会失效，是因为它按到起点的距离从近到远逐个结算节点，一条横跨数千公里的路线会迫使它在到达终点之前结算掉图中相当大比例的节点——CH 把这部分开销挪到一次性的离线预处理阶段，而不是每次查询都重新付出这个代价。
