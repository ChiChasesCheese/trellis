---
slug: binary-tree-inorder-traversal
---
## Q
**LC 94 二叉树的中序遍历**｜Easy

返回二叉树的中序遍历（左、根、右）。

## A
**一句话。** 递归：先左子树，再记录当前节点，最后右子树。

```python
def inorder_traversal(root):
    res = []

    def dfs(node):
        if node is None:
            return
        dfs(node.left)
        res.append(node.val)   # 夹在两次递归之间就是中序
        dfs(node.right)

    dfs(root)
    return res
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- `append` 放错位置：放在递归前是前序，`[1,null,2,3]` 得 `[1,2,3]`；放在后面是后序，应为 `[1,3,2]`。
- 链状树递归深度可达 `n`：超过 CPython 默认上限约 `1000` 会 `RecursionError`。

**追问。**
- 迭代怎么写？：显式栈，一路压左孩子；弹出时访问，再转向右子树。
- `O(1)` 空间呢？：Morris 遍历，用前驱的空右指针做临时线索。

**同模式。** LC 98 验证二叉搜索树、LC 230 二叉搜索树中第 K 小的元素、LC 144 二叉树的前序遍历、LC 145 二叉树的后序遍历
