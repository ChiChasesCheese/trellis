---
id: tlc-lowest-common-ancestor-of-a-binary-search-tree-2-code
node: b.lowest-common-ancestor-of-a-binary-search-tree
type: qa
step: 2
---
## Q
**LC 235 二叉搜索树的最近公共祖先**｜Easy · 字节高频｜写出 Python 实现

BST 的根结点 `root`，两个不同的结点 `p`、`q`（都在树里，所有结点值唯一）。返回它们的最近公共祖先，一个结点可以是自己的祖先。要求 `O(h)` 时间、`O(1)` 空间。

## A
**思路。** 取 `lo = min(p.val, q.val)`、`hi = max(p.val, q.val)`。从根开始：结点值比 `lo` 小，目标都在右边；比 `hi` 大，目标都在左边；否则落在 `[lo, hi]` 内，就是答案。

```python
def lowest_common_ancestor(root: TreeNode | None, p: TreeNode, q: TreeNode) -> TreeNode | None:
    lo, hi = min(p.val, q.val), max(p.val, q.val)    # 不假设 p 比 q 小
    node = root
    while node:
        if node.val < lo:              # 两个目标都在右子树
            node = node.right
        elif node.val > hi:            # 两个目标都在左子树
            node = node.left
        else:                          # lo <= node.val <= hi：两路在此分叉（或 node 本身就是其一）
            return node
    return None
```

运行（`root = [6,2,8,0,4,7,9,null,null,3,5]`，返回结点的值）：`p = 2, q = 8` → `6`，`p = 2, q = 4` → `2`，`p = 8, q = 2` → `6`，`p = 3, q = 5` → `4`；10 万个结点的链状 BST 上也直接返回，没有递归深度问题。

**复杂度。** 时间 `O(h)`：每步下降一层；空间 `O(1)`：只有一个游标 `node`。

**写法要点。** `min` / `max` 先把 `p`、`q` 的先后顺序抹平；`while node:` 利用结点对象的真值（没有 `__bool__` 的对象总是真）判断是否走到空；用循环代替递归，既省栈又避开 Python 默认 1000 层的递归上限；返回的是结点对象，不是值。
