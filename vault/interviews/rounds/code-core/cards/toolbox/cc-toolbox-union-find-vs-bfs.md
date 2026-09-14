---
id: cc-toolbox-union-find-vs-bfs
node: toolbox.union-find
type: qa
---
## Q
Components can be answered with union-find or with BFS over an adjacency dict. What decides?

## A
**DSU when edges arrive incrementally and the questions are "same component?" and "how big?"; BFS when you need the graph itself.**

- DSU has **no un-union**. A spec with removals, or an "as of time t" view, forces a rebuild — so BFS over a filtered edge set wins there.
- DSU gives no path, no distance and no neighbour list: "who is *directly* linked to X" and "shortest chain between X and Y" are BFS questions ([[cc-algorithms-graph-traversal-bfs-layers]]).
- Memory: DSU is one dict of parents; BFS needs full adjacency, which matters at 10^6 edges.
- Enumerating each component's members from a DSU is one extra pass — `groups[find(x)].append(x)` — and the iteration order of that pass is what makes the output deterministic ([[cc-algorithms-graph-traversal-components]]).
- Counting the target itself is the classic off-by-one: a lone record is a component of size 1, not 0.

## Q zh
连通块既可以用并查集回答，也可以在邻接表上 BFS。用什么来决定？

## A zh
**边是增量到达、问题是「同一块吗」「多大」时用 DSU；需要图本身时用 BFS。**

- DSU **不能撤销合并**。带删除的 spec，或「截至 t 时刻」的视图，都会逼你重建 —— 那种场合是在过滤后的边集上 BFS 更好。
- DSU 不给路径、不给距离、不给邻居表：「谁与 X *直接*相连」和「X 到 Y 的最短链」都是 BFS 的问题（[[cc-algorithms-graph-traversal-bfs-layers]]）。
- 内存：DSU 只是一个 parent 字典；BFS 需要完整邻接表，在 10^6 条边时这很要紧。
- 从 DSU 枚举每个连通块的成员只多一趟 —— `groups[find(x)].append(x)` —— 而这一趟的遍历顺序决定了输出是否确定（[[cc-algorithms-graph-traversal-components]]）。
- 把目标自身算进去是经典的 off-by-one：一条孤立记录构成大小为 1 的连通块，而不是 0。
