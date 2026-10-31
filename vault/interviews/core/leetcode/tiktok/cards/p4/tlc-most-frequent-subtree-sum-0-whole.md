---
id: tlc-most-frequent-subtree-sum-0-whole
node: p4.most-frequent-subtree-sum
type: qa
---
## Q
**LC 508 出现次数最多的子树元素和**｜Medium · 近一年被问：美国 1 次、国内 0 次 · 最近 2026-04-11（美国面试记录）

给二叉树的根结点 `root`，返回出现次数最多的**子树元素和**；如果有多个和出现次数并列最多，全部返回（顺序不限）。一个结点的子树元素和，是以它为根的子树上所有结点（含它自己）的值之和。节点数在 `[1, 10^4]`，`-10^5 <= Node.val <= 10^5`。例：`root = [5,2,-3]` → `[2,-3,4]`（三个和各出现一次，都返回）；`root = [5,2,-5]` → `[2]`（子树和依次为 `2`、`-5`、`2`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 后序遍历求每个节点的子树和（自身 + 左子树和 + 右子树和），用 `Counter` 计数；最后返回出现次数等于最大次数的所有和。`O(n)`。

**识别。** 「子树的聚合量 + 统计频次」：先算出每个节点的子树和（自底向上），再用哈希表计数。「并列最多的全部返回」意味着不能用 `most_common(1)`，要先求最大次数再过滤。节点数到 `10^4`，树可能是一条链，递归深度见易错点。

**推导。** 暴力：对每个节点单独遍历它的子树求和，链状树上 `O(n^2)` → 父节点的子树和 = 自身 + 两个孩子的子树和，孩子的和之前已算过，重复遍历是浪费 → 后序一遍，每个节点只算一次：递归函数返回子树和，算出来就 `freq[s] += 1`。

```python
from collections import Counter


def find_frequent_tree_sum(root: TreeNode | None) -> list[int]:
    freq: Counter[int] = Counter()

    def subtree_sum(node: TreeNode | None) -> int:   # 返回 node 的子树和，顺便给它计一次数
        if node is None:
            return 0
        s = node.val + subtree_sum(node.left) + subtree_sum(node.right)
        freq[s] += 1
        return s

    subtree_sum(root)
    top = max(freq.values(), default=0)        # 空树时 freq 为空，default 避免 ValueError
    return [s for s, c in freq.items() if c == top]
```

运行：`[5,2,-3]` → `[-3, 2, 4]`（排序后，顺序不限）；`[5,2,-5]` → `[2]`；`[0]` → `[0]`；`[1]` → `[1]`；`10^4` 个节点的右斜链 → 返回 `10000` 个互不相同的和（调大递归上限后；默认上限下抛 `RecursionError`）。

**复杂度。** 时间 `O(n)`；空间 `O(n)`（`freq`，最坏每个子树和都不同；加上最深 `O(n)` 的递归栈）。

**易错点。**
- 用 `freq.most_common(1)` 只取一个：并列时漏掉其他值，`[5,2,-3]` 三个和各一次，只会返回其中一个。
- 只对根或叶子计数：每个节点（包含叶子）都有自己的子树和，都要计一次。
- 空孩子当 `None` 参与加法：抛 `TypeError`；让 `subtree_sum(None)` 返回 `0`。
- 递归深度：`10^4` 个节点的右斜链，深度 `10^4`，超过 CPython 默认递归上限约 `1000`，抛 `RecursionError`；要 `sys.setrecursionlimit` 调大，或改成迭代（见追问）。

**追问。**
- 只要其中一个众数，或者要最小的众数：`min(s for s, c in freq.items() if c == top)`。
- 同时返回每个众数出现的次数：`{s: c for s, c in freq.items() if c == top}`。
- 不想动递归上限：用栈得到先序序列，倒序处理（孩子先于父亲），每个节点的和存进字典：
```python
from collections import Counter


def find_frequent_tree_sum_stack(root: TreeNode | None) -> list[int]:
    if root is None:
        return []
    order: list[TreeNode] = []
    stack = [root]
    while stack:                               # 先序：父总在子之前
        node = stack.pop()
        order.append(node)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    total: dict[TreeNode, int] = {}            # 每个节点的子树和
    freq: Counter[int] = Counter()
    for node in reversed(order):               # 倒着扫 = 孩子先于父亲
        s = node.val + total.get(node.left, 0) + total.get(node.right, 0)
        total[node] = s
        freq[s] += 1
    top = max(freq.values())
    return [s for s, c in freq.items() if c == top]
```

**同模式。** LC 563 二叉树的坡度、LC 543 二叉树的直径、LC 124 二叉树中的最大路径和、LC 1339 分裂二叉树的最大乘积、LC 437 路径总和 III。
