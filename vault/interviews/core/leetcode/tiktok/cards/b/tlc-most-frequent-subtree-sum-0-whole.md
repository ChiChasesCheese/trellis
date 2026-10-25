---
id: tlc-most-frequent-subtree-sum-0-whole
node: b.most-frequent-subtree-sum
type: qa
---
## Q
**LC 508 出现次数最多的子树元素和**｜Medium · TikTok 高频

给二叉树的根结点 `root`，返回出现次数最多的**子树元素和**；如果有多个和出现次数并列最多，全部返回（顺序不限）。一个结点的子树元素和，是以它为根的子树上所有结点（含它自己）的值之和。节点数在 `[1, 10^4]`，`-10^5 <= Node.val <= 10^5`。例：`root = [5,2,-3]` → `[2,-3,4]`（三个和各出现一次，都返回）；`root = [5,2,-5]` → `[2]`（子树和依次为 `2`、`-5`、`2`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 后序遍历求每个节点的子树和（自身 + 左子树和 + 右子树和），用 `Counter` 计数；最后返回出现次数等于最大次数的所有和。`O(n)`。

**识别。** 「子树的聚合量 + 统计频次」：先算出每个节点的子树和（自底向上），再用哈希表计数。「并列最多的全部返回」意味着不能用 `most_common(1)`，要先求最大次数再过滤。节点数到 `10^4`，树可能是一条链，递归会超过 Python 默认深度。

**推导。** 暴力：对每个节点单独遍历它的子树求和，链状树上 `O(n^2)` → 父节点的子树和 = 自身 + 两个孩子的子树和，孩子的和之前已算过，重复遍历是浪费 → 后序一遍，每个节点只算一次 → 为避免深递归，用先序栈得到 `order`，倒序处理保证孩子先于父亲，每个节点的和存进字典，同时 `freq[s] += 1`。

```python
from collections import Counter


def find_frequent_tree_sum(root: TreeNode | None) -> list[int]:
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

运行：`[5,2,-3]` → `[-3, 2, 4]`（排序后，顺序不限）；`[5,2,-5]` → `[2]`；`[0]` → `[0]`；`[1]` → `[1]`；`10^4` 个节点的右斜链 → 返回 `10000` 个互不相同的和，不抛 `RecursionError`。

**复杂度。** 时间 `O(n)`；空间 `O(n)`（`order`、`total`、`freq`）。

**易错点。**
- 用 `freq.most_common(1)` 只取一个：并列时漏掉其他值，`[5,2,-3]` 三个和各一次，只会返回其中一个。
- 只对根或叶子计数：每个节点（包含叶子）都有自己的子树和，都要计一次。
- 空孩子当 `None` 参与加法：抛 `TypeError`；用 `total.get(child, 0)` 或让 `None` 对应 `0`。

**追问。**
- 只要其中一个众数，或者要最小的众数：`min(s for s, c in freq.items() if c == top)`。
- 同时返回每个众数出现的次数：`{s: c for s, c in freq.items() if c == top}`。
- 内存紧张：`total` 字典只在处理父亲之前需要，可在父亲算完后删除孩子的条目，把额外空间降到树的「宽度」量级。

**同模式。** LC 563 二叉树的坡度、LC 543 二叉树的直径、LC 124 二叉树中的最大路径和、LC 1339 分裂二叉树的最大乘积、LC 437 路径总和 III。
