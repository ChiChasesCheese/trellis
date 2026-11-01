---
id: tlc-tops-validate-binary-search-tree-0-whole
node: trees.validate-binary-search-tree
type: qa
---
## Q
**LC 98 验证二叉搜索树**｜Medium · 全公司热度第 127 名 · Blind 75、NeetCode 150、Hot 100、Top Interview 150

给你一个二叉树的根节点 `root`，判断其是否是一个有效的二叉搜索树。有效二叉搜索树定义如下：节点的左子树只包含严格小于当前节点的数；节点的右子树只包含严格大于当前节点的数；所有左子树和右子树自身必须也是二叉搜索树。树中节点数目范围在 `[1, 10^4]` 内，`-2^31 <= Node.val <= 2^31 - 1`。

例：`root = [2,1,3]` → `true`；`root = [5,1,4,null,null,3,6]` → `false`（根是 `5`，但右子节点是 `4`）。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 带区间约束的树递归（pass bounds down）；BST 的合法性是整棵子树的约束，不是父子之间的约束。

**一句话。** 递归时把每个结点允许的取值开区间 `(lo, hi)` 传下去：往左走收紧上界，往右走收紧下界。

**识别。** 「验证 BST」且定义里写的是整棵子树「只包含」，就是区间约束，不是比较父子。`n <= 10^4`，线性。

**推导。** 最直观的写法是检查 `left.val < node.val < right.val`，但这只比较了父子：例如 `[5,4,6,null,null,3,7]`：每个父子对都合法，但 `3` 在 `5` 的右子树里，却比 `5` 小，局部检查看不出来。真正的约束是：一个结点必须小于所有祖先中「它在其右子树里」的那些，并大于「它在其左子树里」的那些。把这些约束压缩成一个区间 `(lo, hi)` 随递归传下：走左子树时上界收紧为当前值，走右子树时下界收紧为当前值。

```python
from math import inf


def is_valid_bst(root: TreeNode | None) -> bool:
    def valid(node: TreeNode | None, lo: float, hi: float) -> bool:
        if not node:                    # 空树合法
            return True
        if not lo < node.val < hi:      # 必须严格落在祖先给出的开区间内
            return False
        return (valid(node.left, lo, node.val)        # 左子树都要小于当前值
                and valid(node.right, node.val, hi))  # 右子树都要大于当前值

    return valid(root, -inf, inf)       # 根没有约束，用 ±inf 而不是 ±2^31
```

**运行。** `[2,1,3]` → `True`；`[5,1,4,null,null,3,6]` → `False`；`[-2147483648]` → `True`；`[2,2,2]` → `False`。

**复杂度。** 时间 `O(n)`，每个结点访问一次；空间 `O(h)`（递归栈）。

**拓展优化。**
- 中序遍历法：BST 的中序序列严格递增，所以只要记住上一个访问的值，当前值必须大于它。
```python
def is_valid_bst_inorder(root: TreeNode | None) -> bool:
    prev = -inf
    def inorder(node: TreeNode | None) -> bool:
        nonlocal prev
        if not node:
            return True
        if not inorder(node.left):          # 先左
            return False
        if node.val <= prev:                # 严格递增：相等也不行
            return False
        prev = node.val
        return inorder(node.right)          # 后右

    return inorder(root)
```
- 显式栈的迭代中序：见 LC 94，适合树很深时避免递归上限。

**易错点。**
- 只比较父子：`[5,4,6,null,null,3,7]` 逐个父子对都合法，会错误返回 `True`，正确是 `False`（`3` 小于祖先 `5`）。
- 用 `-2**31`、`2**31 - 1` 当初始边界并用严格不等号：`[-2147483648]` 本身落在边界上，会被误判成 `False`。边界要用 `±inf`。
- 递归深度等于树高：`n = 10^4` 的退化链会超过 CPython 默认约 1000 的递归上限而 `RecursionError`；要么调高上限，要么改显式栈。

**同模式。** LC 230 二叉搜索树中第 K 小的元素、LC 99 恢复二叉搜索树、LC 450 删除二叉搜索树中的节点、LC 530 二叉搜索树的最小绝对差。
