---
slug: binary-tree-preorder-traversal
---
## Q
**LC 144 二叉树的前序遍历**｜Easy

返回二叉树的前序遍历（根、左、右）。

## A
**一句话。** 递归：先记录根，再递归左子树、右子树。

```python
def preorder_traversal(root):
    ans = []
    def dfs(node):
        if node is None:
            return
        ans.append(node.val)   # 根 → 左 → 右
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 迭代写法先压左孩子：栈后进先出，要先压右孩子再压左孩子，左边才会先出栈。
- 空树没处理：`root = None` 时返回 `[]`。

**追问。**
- 迭代写法？：栈里先放根，弹出就记录，再依次压右、左孩子。
- `O(1)` 空间？：Morris 遍历，借用左子树最右结点的空右指针连回当前结点，第一次到达时记录。

**同模式。** LC 94 二叉树的中序遍历、LC 145 二叉树的后序遍历、LC 102 二叉树的层序遍历、LC 105 从前序与中序遍历序列构造二叉树
