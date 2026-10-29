---
id: tlc-minimum-distance-between-bst-nodes-2-code
node: a.minimum-distance-between-bst-nodes
type: qa
step: 2
---
## Q
**LC 783 二叉搜索树节点最小距离**｜写出 Python 实现

给 BST 的根节点（2 到 100 个节点，值在 `0` 到 `10^5`），返回任意两个不同节点值之差的最小值，要求 `O(n)`。

## A
**思路。** 中序遍历按升序访问节点，最小差只会出现在相邻两个值之间。用 `prev` 记上一个访问的值，每到一个节点就用 `node.val - prev` 更新答案。

```python
from math import inf


def min_diff_in_bst(root: TreeNode | None) -> int:
    best = inf
    prev: int | None = None              # 中序遍历中上一个节点的值

    def inorder(node: TreeNode | None) -> None:
        nonlocal best, prev
        if node is None:
            return
        inorder(node.left)
        if prev is not None:             # 中序是升序：只需和前一个值比
            best = min(best, node.val - prev)
        prev = node.val
        inorder(node.right)

    inorder(root)
    return best
```

运行：`[4,2,6,1,3]` → `1`，`[1,0,48,null,null,12,49]` → `1`，`[5,1,null,null,4]` → `1`，`[0,null,100000]` → `100000`。

**复杂度。** 时间 `O(n)`，每个节点访问一次；空间 `O(h)`，`h` 为树高，链状树时是 `O(n)`。

**写法要点。** 内层函数用 `nonlocal` 改写外层的 `best`、`prev`（它们是重新赋值，不是改容器内容，所以必须声明）；`prev` 用 `None` 表示「还没访问过节点」，比用一个魔数初值更不易错；`math.inf` 作为最小值的初值，题目保证至少两个节点，返回时一定已被整数替换。
