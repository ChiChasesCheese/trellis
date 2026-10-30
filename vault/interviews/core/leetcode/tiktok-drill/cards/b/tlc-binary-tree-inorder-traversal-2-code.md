---
id: tlc-binary-tree-inorder-traversal-2-code
node: b.binary-tree-inorder-traversal
type: qa
step: 2
---
## Q
**LC 94 二叉树的中序遍历**｜写出 Python 实现

二叉树根结点 `root`（结点数 `0..100`，值在 `[-100, 100]`，可以为空）。写 `inorder_traversal(root)`，返回中序遍历的值列表。

## A
**思路。** 内层函数 `dfs(node)`：空结点直接返回；否则先递归左子树，再把当前值追加进结果，最后递归右子树。追加夹在两次递归之间，就是中序。

```python
def inorder_traversal(root: TreeNode | None) -> list[int]:
    result: list[int] = []

    def dfs(node: TreeNode | None) -> None:
        if node is None:
            return
        dfs(node.left)                 # 先把整个左子树走完
        result.append(node.val)        # 再访问自己：夹在左右之间就是中序
        dfs(node.right)                # 最后走右子树

    dfs(root)
    return result
```

运行：`[1,null,2,3]` → `[1, 3, 2]`，`[]` → `[]`，`[1]` → `[1]`。

**复杂度。** 时间 `O(n)`：每个结点访问一次；空间 `O(h)`：递归栈深度等于树高。

**写法要点。** 结果列表放在外层，内层 `dfs` 靠闭包直接 `append`，不用 `nonlocal`（只是修改列表，不是重新绑定变量）；`dfs` 没有返回值，类型标注为 `-> None`；`TreeNode | None` 的联合类型标注不需要 `Optional`。深度：题目限定至多 `100` 个结点没问题，但 `1500` 层的左斜链会超过 CPython 默认递归上限（约 `1000`）而抛 `RecursionError`，迭代写法见追问卡。
