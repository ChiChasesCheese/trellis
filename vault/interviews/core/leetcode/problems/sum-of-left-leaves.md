---
slug: sum-of-left-leaves
---
## Q
**LC 404 左叶子之和**｜Easy

求二叉树所有左叶子（是父结点左孩子的叶子）的值之和。

## A
**一句话。** DFS 时带上「我是不是左孩子」：到达叶子时是左孩子就返回它的值，否则返回 0。

```python
def sum_of_left_leaves(root):
    def dfs(node, is_left):
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return node.val if is_left else 0
        return dfs(node.left, True) + dfs(node.right, False)
    return dfs(root, False)    # 根不是左叶子
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 把所有左孩子都加上：左孩子还有子树时不是叶子。
- 根是叶子时也算：只有一个结点的树答案是 0。

**追问。**
- 不传参数？：在父结点判断 `node.left` 是不是叶子，是就加上它的值，再递归右子树和非叶子的左子树。
- BFS 写法？：层序遍历，出队时检查它的左孩子是否叶子。

**同模式。** LC 112 路径总和、LC 104 二叉树的最大深度、LC 129 求根节点到叶节点数字之和
