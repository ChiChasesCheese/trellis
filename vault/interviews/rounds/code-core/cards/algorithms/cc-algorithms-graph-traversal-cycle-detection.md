---
id: cc-algorithms-graph-traversal-cycle-detection
node: algorithms.graph-traversal
type: qa
---
## Q
Detect a cycle — in a directed graph and in an undirected one. Same code?

## A
**No, and using one for the other is a standard wrong answer.**

**Directed:** a node is *in progress* (on the current DFS path) or *done*. An edge into an in-progress node is a back edge → cycle. A plain `visited` set is not enough: it reports the diamond `a→b, a→c, b→d, c→d` as a cycle when there is none. Iteratively, Kahn's algorithm gives the same answer for free ([[cc-algorithms-topological-cycle-shortfall]]).

**Undirected:** DFS or BFS with a visited set, but skip the edge you arrived by — otherwise every single edge looks like a 2-cycle. With parallel edges, skip by *edge id*, not by parent node, or a genuine 2-cycle is missed.

Union-find also detects an undirected cycle: an edge whose endpoints already share a root closes one ([[cc-toolbox-union-find-find]]).

## Q zh
检测环 —— 在有向图和无向图里。是同一份代码吗？

## A zh
**不是，而且把其中一种用到另一种上是标准的错误答案。**

**有向图：** 节点要么*进行中*（在当前 DFS 路径上），要么*已完成*。指向「进行中」节点的边是回边 → 有环。仅用 `visited` 集合不够：它会把菱形 `a→b, a→c, b→d, c→d` 误报为有环。迭代地看，Kahn 算法免费给出同样的答案（[[cc-algorithms-topological-cycle-shortfall]]）。

**无向图：** 用 visited 集合做 DFS 或 BFS，但要跳过你来时的那条边 —— 否则每一条边看起来都像一个二元环。存在平行边时，按*边的 id* 跳过而不是按父节点，否则会漏掉真正的二元环。

并查集也能检测无向图的环：一条两端已同根的边就闭合了一个环（[[cc-toolbox-union-find-find]]）。
