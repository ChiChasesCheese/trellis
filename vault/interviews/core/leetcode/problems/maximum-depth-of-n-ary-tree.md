---
slug: maximum-depth-of-n-ary-tree
---
## Q
**LC 559 N 叉树的最大深度**｜Easy

给一棵 N 叉树（结点有 `val` 和列表 `children`），返回从根到最远叶子的最长路径上的结点数。

## A
**一句话。** 一个结点的深度是 1 加上所有孩子深度的最大值，空树为 0。

```python
def max_depth(root):
    if not root:
        return 0
    deepest = 0
    for kid in root.children:
        deepest = max(deepest, max_depth(kid))
    return deepest + 1         # 叶子的 children 为空，得 1
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 对空 `children` 直接 `max(...)`：空序列会抛 `ValueError`，要给初值 `0`。
- 把深度算成边数：这里数的是结点数。

**追问。**
- 不递归怎么做？：BFS 按层数，每处理完一层深度加 1。
- 树很深会爆栈吗？：Python 默认递归上限约 1000 层，深链要改 BFS 或迭代 DFS。

**同模式。** LC 104 二叉树的最大深度、LC 429 N 叉树的层序遍历、LC 1376 通知所有员工所需的时间、LC 690 员工的重要性
