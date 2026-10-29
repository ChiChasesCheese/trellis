---
id: tlc-most-frequent-subtree-sum-2-code
node: a.most-frequent-subtree-sum
type: qa
step: 2
---
## Q
**LC 508 出现次数最多的子树元素和**｜写出 Python 实现

二叉树 `root`（节点数 `[1, 10^4]`，`-10^5 <= Node.val <= 10^5`），返回出现次数最多的子树元素和，并列时全部返回，顺序不限。要求链状树上也不递归爆栈。

## A
**思路。** 用栈做一次先序遍历得到 `order`，倒序处理，每个节点的子树和 = 自身值 + 左右孩子的子树和，算出后在 `Counter` 里计一次。最后取最大次数，把所有达到它的和列出来。

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

运行：`[5,2,-3]` → `[-3, 2, 4]`（排序后）；`[5,2,-5]` → `[2]`；`[0]` → `[0]`；`10^4` 个节点的右斜链 → `10000` 个和各出现一次，全部返回。

**复杂度。** 时间 `O(n)`：先序一遍、倒序一遍，计数与取最大各 `O(n)`；空间 `O(n)`。

**写法要点。** `total.get(node.left, 0)` 对 `None` 和对象都成立，省掉判空；`Counter` 的 `freq[s] += 1` 对新键默认从 `0` 起；`max(freq.values())` 配合列表推导式能收集**所有**并列众数，比 `most_common(1)` 更不容易漏。
