---
id: cc-algorithms-graph-traversal-components
node: algorithms.graph-traversal
type: qa
---
## Q
Enumerate connected components in a deterministic order, over records where some nodes appear only as a link target.

## A
**Loop over every node in the universe and start a traversal from each unvisited one.**

- The **node universe** must include nodes seen only as an edge endpoint. Building it from the record ids alone silently loses them, and they are the ones a hidden test adds.
- Determinism has two halves: iterate the universe in a defined order (first appearance, or sorted), and sort each component's members before printing. A `set`'s iteration order is not a contract ([[cc-toolbox-hash-set-vs-dict]]).
- Give a component a stable identity — the node that started it, or the DSU root ([[cc-toolbox-union-find-vs-bfs]]) — so later parts can refer to it.
- Singletons count: a node with no edges is a component of size 1, and "the group size includes the target itself" is the off-by-one that gets tested.

## Q zh
在某些节点只作为关联目标出现的记录上，按确定顺序枚举连通块。

## A zh
**遍历全集中的每个节点，从每个未访问的节点开始一次遍历。**

- **节点全集**必须包含只作为边端点出现的节点。仅从记录 id 构造全集会悄悄丢掉它们，而它们正是隐藏测试会加的。
- 确定性有两半：按定义好的顺序遍历全集（首次出现或排序），并在打印前对每个连通块的成员排序。`set` 的遍历顺序不是契约（[[cc-toolbox-hash-set-vs-dict]]）。
- 给连通块一个稳定标识 —— 开启它的那个节点，或 DSU 的根（[[cc-toolbox-union-find-vs-bfs]]）—— 好让后面的 part 能引用它。
- 单点也算：没有边的节点构成大小为 1 的连通块，而「组的大小包含目标自身」正是会被测的 off-by-one。
