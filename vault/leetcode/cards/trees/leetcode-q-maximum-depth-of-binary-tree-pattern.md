---
id: leetcode-q-maximum-depth-of-binary-tree-pattern
node: trees.binary-tree
type: qa
anki: 1787102222312
tags: [lc::104, leetcode, pattern, recall]
---
## Q
如何用两种方式（BFS 层序遍历 / DFS 后序遍历）求二叉树最大深度？各自的核心不变量是什么？

## A
BFS：用队列做层序遍历，每处理完一整层（用 for _ in range(len(que)) 固定当前层节点数）depth+=1，不变量是「每次内层循环恰好处理完当前层，队列末尾只剩下一层的节点」。DFS：maxDepth(root) = 1 + max(maxDepth(left), maxDepth(right))，root 为空返回 0，不变量是「子树的最大深度已知，父节点深度=子树深度+1」。两者时间复杂度都是 O(n)，空间复杂度 BFS 为 O(w)（w 为最大宽度），DFS 递归为 O(h)（h 为树高，最坏 O(n)）。

**Evidence**

My Solution 中给出了 maxDepth（BFS，用 deque 按层遍历并 depth += 1）和 maxDepth0（DFS，1 + max(左, 右)）两种实现。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F104%20-%20Maximum%20Depth%20of%20Binary%20Tree)
