---
id: tlc-maximum-depth-of-binary-tree-2-code
node: b.maximum-depth-of-binary-tree
type: qa
step: 2
---
## Q
**LC 104 二叉树的最大深度**｜写出 Python 实现

二叉树节点数在 `[0, 10^4]`，返回根到最远叶子的路径上的节点数（空树为 `0`）。

## A
**思路。** 直接用定义递归：空树深度 `0`，否则是 `1` 加上左右子树深度的较大者。每个节点只算一次。

```python
def max_depth(root: TreeNode | None) -> int:
    if root is None:                               # 空树深度为 0
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

运行：`[3,9,20,null,null,15,7]` → `3`，`[1,null,2]` → `2`，空树 → `0`，`[0]` → `1`，`10^4` 个节点的单链 → `10000`（调大递归上限后；默认上限下抛 `RecursionError`）。

**复杂度。** 时间 `O(n)`：每个节点访问一次；空间 `O(h)`：递归栈深度等于树高 `h`，最坏 `O(n)`。

**写法要点。** 空树判断放在最前，`None` 当基准情形，叶子不需要特判；`max` 直接比较两个子树的返回值；递归调用的是函数自己，不需要辅助函数或 `nonlocal`。深树的写法见追问。
