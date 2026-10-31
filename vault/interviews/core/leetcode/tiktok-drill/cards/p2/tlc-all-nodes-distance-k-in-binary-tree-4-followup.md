---
id: tlc-all-nodes-distance-k-in-binary-tree-4-followup
node: p2.all-nodes-distance-k-in-binary-tree
type: qa
step: 4
---
## Q
**LC 863 二叉树中所有距离为 K 的结点**｜追问

面试官接着问：（1）不允许额外的 `O(n)` 父指针表，能做吗？（2）同一棵树要回答很多次不同 `(target, k)` 的查询？（3）把「距离为 `k`」改成「距离不超过 `k`」或要每个结点的距离？

## A
1. **不建父表**：一次后序 DFS，`dfs(node)` 返回「`target` 到 `node` 的距离」（`target` 不在该子树里返回 `-1`）。若 `target` 在左子树且距离为 `d`，则 `node` 自己距离 `d+1`，再向**右子树**向下找深度 `k-d-2` 的结点。额外空间 `O(h)`，代价是代码更绕、要分三种情况。
2. **多次查询**：父指针表与 `(target, k)` 无关，只建一次；之后每次查询是一次 `O(n)` BFS。查询特别多时可以把 BFS 换成「按祖先链 + 子树深度」的预处理，面试里说出思路即可。
3. **不超过 `k` / 每结点距离**：把 `seen` 换成 `dist: dict[TreeNode, int]`，入队时记 `dist[nb] = dist[node] + 1`，`dist[nb] <= k` 的都收集。

**Python 提醒**：不要把 `visited` 写成 `list`，`nb not in seen_list` 是 `O(n)`，整体退化成 `O(n^2)`；也不要用 `val` 当键就假设值唯一——此处唯一，其他树题常常不唯一，用结点对象本身当键最稳。
