---
id: tlc-binary-tree-inorder-traversal-2-code
node: b.binary-tree-inorder-traversal
type: qa
step: 2
---
## Q
**LC 94 二叉树的中序遍历**｜写出 Python 实现

二叉树根结点 `root`（结点数 `0..100`，值在 `[-100, 100]`，可以为空）。写 `inorder_traversal(root)`，用迭代（不用递归）返回中序遍历的值列表。

## A
**思路。** 当前结点 `node` 不空就压栈并向左走；走到头后弹出栈顶、访问、转向它的右孩子；`node` 和栈都空时结束。

```python
def inorder_traversal(root: TreeNode | None) -> list[int]:
    result: list[int] = []
    stack: list[TreeNode] = []
    node = root
    while node or stack:
        while node:                    # 一路向左，沿途结点都等着“左子树完成后”再访问
            stack.append(node)
            node = node.left
        node = stack.pop()             # 最左的结点：左子树已处理完
        result.append(node.val)        # 访问自己
        node = node.right              # 然后处理右子树
    return result
```

运行：`[1,null,2,3]` → `[1, 3, 2]`，`[]` → `[]`，`[1]` → `[1]`；`10^4` 个结点的左斜链（远超题目上限 `100`）→ 长度 `10000`，没有递归溢出。

**复杂度。** 时间 `O(n)`：每个结点入栈、出栈各一次；空间 `O(h)`：栈深至多是树高。

**写法要点。** 外层 `while node or stack` 的两个条件分别覆盖「还有右子树要走」和「还有祖先等着访问」。内层 `while node` 把「一路向左」写成循环，比递归直接。同一个变量 `node` 先当“下潜指针”，弹出后当“当前访问的结点”，最后又变成“右子树入口”，注意顺序。`TreeNode | None` 的联合类型标注不需要 `Optional`。
