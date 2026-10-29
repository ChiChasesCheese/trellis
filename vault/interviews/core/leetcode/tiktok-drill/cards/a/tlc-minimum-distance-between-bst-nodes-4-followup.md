---
id: tlc-minimum-distance-between-bst-nodes-4-followup
node: a.minimum-distance-between-bst-nodes
type: qa
step: 4
---
## Q
**LC 783 二叉搜索树节点最小距离**｜追问

面试官接着问：（1）不用递归怎么写？（2）如果树不是 BST？（3）要求 `O(1)` 额外空间呢？

## A
1. **迭代中序**：用显式栈模拟递归：一路把左孩子压栈，弹出栈顶访问，再转向它的右子树。树退化成长链时也不会碰到递归深度限制。

```python
from math import inf


def min_diff_in_bst_iter(root: TreeNode | None) -> int:
    best = inf
    prev: int | None = None
    stack: list[TreeNode] = []
    node = root
    while stack or node:
        while node:                     # 一路向左，把路径压栈
            stack.append(node)
            node = node.left
        node = stack.pop()              # 按升序弹出
        if prev is not None:
            best = min(best, node.val - prev)
        prev = node.val
        node = node.right
    return best
```

`[4,2,6,1,3]` → `1`，`[1,0,48,null,null,12,49]` → `1`。这个模板也是 LC 173 BST 迭代器和 LC 230 第 K 小元素的骨架。
2. **不是 BST**：中序不再有序，只能收集所有值后 `sorted`，再用 `itertools.pairwise` 比相邻：`min(b - a for a, b in pairwise(sorted(vals)))`，`O(n log n)`。
3. **`O(1)` 空间**：Morris 中序遍历。访问节点前，找到它左子树的最右节点，把其空的右指针临时指回当前节点；第二次到达时断开并访问。每条边最多走两次，时间仍 `O(n)`，遍历结束后树恢复原样。

**Python 提醒**：递归默认深度上限约 1000（`sys.getrecursionlimit()`）；节点数上万的链状树要用迭代写法，不要靠调大上限。
