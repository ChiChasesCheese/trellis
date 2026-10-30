---
id: tlc-balanced-binary-tree-2-code
node: a.balanced-binary-tree
type: qa
step: 2
---
## Q
**LC 110 平衡二叉树**｜写出 Python 实现

给定二叉树的根节点 `root`（节点数 `0` 到 `5000`，节点值 `-10^4` 到 `10^4`），判断它是否高度平衡：任一节点的左右子树高度之差的绝对值都不超过 `1`。空树是平衡的。要求 `O(n)`。

## A
**思路。** 内层函数 `height(node)` 后序返回子树高度，不平衡时返回 `-1`。左子树不平衡就立即返回；右子树不平衡或左右高度差大于 `1` 也返回 `-1`；否则返回较大的高度加一。最后判断根的返回值是不是 `-1`。

```python
def is_balanced(root: TreeNode | None) -> bool:
    def height(node: TreeNode | None) -> int:   # 返回子树高度；不平衡时返回 -1 并一路上传
        if node is None:
            return 0
        left = height(node.left)
        if left == -1:
            return -1
        right = height(node.right)
        if right == -1 or abs(left - right) > 1:
            return -1
        return max(left, right) + 1

    return height(root) != -1
```

运行：`[3,9,20,null,null,15,7]` → `True`，`[1,2,2,3,3,null,null,4,4]` → `False`，`[]` → `True`，`[1,2]` → `True`，`[1,2,null,3]` → `False`。

**复杂度。** 时间 `O(n)`：每个节点访问一次，不重复求高度；空间 `O(h)`：递归栈，最坏（链状）`O(n)`。

**写法要点。**
- 一个函数同时返回“高度”和“是否平衡”（用 `-1` 编码），不用返回元组 `(bool, int)`，调用方少一次解包。
- 左子树失败就**不递归右子树**：提前剪枝，不平衡的树往往很快就返回。
- 条件 `right == -1 or abs(left - right) > 1` 把“右边失败”和“高度差过大”合并，短路求值保证 `-1` 不参与相减。
- 5000 层的链会超过 Python 默认递归上限：调用前 `sys.setrecursionlimit(10000)`，或改成显式栈（见追问）。
- 把 `height` 定义成内层函数，不污染命名空间，`root` 由闭包之外传入。
