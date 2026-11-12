---
slug: deepest-leaves-sum
---
## Q
**LC 1302 层数最深叶子节点的和**｜Medium

二叉树，返回最深一层叶子节点的值之和。

## A
**一句话。** 前序 DFS 带深度，遇到更深的层就重置累加和，同层则累加。

```python
def deepest_leaves_sum(root):
    best = -1       # 目前最大深度
    total = 0       # 该深度所有节点的和

    def dfs(node, depth):
        nonlocal best, total
        if node is None:
            return
        if depth > best:        # 更深：之前的和作废
            best, total = depth, node.val
        elif depth == best:
            total += node.val
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return total
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 更深时只更新深度，忘了把 `total` 重置为当前值：浅层的和被带进答案。
- 额外判断叶子：最深一层的节点一定是叶子，多判断只会出错。

**追问。**
- 最深叶子的最近公共祖先（LC 865）？：后序返回 `(深度, 节点)`，左右深度相同则当前节点是答案。
- 想避开递归深度限制？：改 BFS 按层求和，最后一层的和就是答案。

**同模式。** LC 104 二叉树的最大深度、LC 102 二叉树的层序遍历、LC 513 找树左下角的值、LC 865 具有所有最深节点的最小子树
