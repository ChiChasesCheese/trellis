---
id: tlc-subtree-of-another-tree-2-code
node: p3.subtree-of-another-tree
type: qa
step: 2
---
## Q
**LC 572 另一个树的子树**｜写出 Python 实现

`root` 有 `1` 到 `2000` 个节点，`subRoot` 有 `1` 到 `1000` 个节点，值在 `[-10^4, 10^4]`。判断 `root` 中是否有一棵子树与 `subRoot` 结构和值完全相同（`root` 自己也算）。树可能退化成一条链。

## A
**思路。** 「完全相同」写成递归：两边同时为空为真，只有一边为空为假，否则根值相等且左对左、右对右都相同。外层再递归：`root` 本身与 `subRoot` 相同，或者 `subRoot` 是左子树或右子树的子树；走到空节点返回 `False`。

```python
def is_same(a: TreeNode | None, b: TreeNode | None) -> bool:
    if a is None or b is None:
        return a is b                              # 同时为空才算相同，只有一边为空就不同
    return a.val == b.val and is_same(a.left, b.left) and is_same(a.right, b.right)


def is_subtree(root: TreeNode | None, sub_root: TreeNode | None) -> bool:
    if root is None:
        return False                               # 走到空还没匹配上
    return is_same(root, sub_root) or is_subtree(root.left, sub_root) or is_subtree(root.right, sub_root)
```

运行：`[3,4,5,1,2]` 里找 `[4,1,2]` → `True`；`[3,4,5,1,2,null,null,null,null,0]` 里找 `[4,1,2]` → `False`；深度 2000 的右链里找深度 1000 的右链，调高递归上限后 → `True`，深度 2000 的左链里找右链 → `False`；默认上限下第一组链输入抛 `RecursionError`。

**复杂度。** 时间 `O(m·n)`：外层访问 `m` 个节点，每个节点上的 `is_same` 最多比较 `n` 个节点；空间 `O(m)`，是递归栈的深度。

**写法要点。** `a is b` 一行同时处理「两边都空」和「只有一边为空」：两个 `None` 是同一个对象，一个 `None` 加一个节点则不是；`and` 与 `or` 的短路让不相等的分支立刻停止；`is_same` 单独成函数，LC 100 直接复用；深度超过约 `1000` 要 `sys.setrecursionlimit`，或用 `-4` 卡的显式栈版本。
