---
id: tlc-most-frequent-subtree-sum-4-followup
node: p5.most-frequent-subtree-sum
type: qa
step: 4
---
## Q
**LC 508 出现次数最多的子树元素和**｜追问

面试官接着问：（1）只要一个众数，且要最小的那个？（2）树换成多叉树？（3）链状树让递归爆栈怎么办？

## A
1. **最小的众数**：`top = max(freq.values())` 后，`min(s for s, c in freq.items() if c == top)`；若同时要返回次数，用 `max(freq.items(), key=lambda kv: (kv[1], -kv[0]))`，先比次数、次数相同取和更小的。
2. **多叉树**：递归里 `s = node.val + sum(subtree_sum(c) for c in node.children)`，其余计数逻辑完全不变。
3. **递归爆栈**：`10^4` 个节点的链，深度超过默认上限约 `1000`。调大 `sys.setrecursionlimit`，或用栈得到先序序列、倒序处理（孩子先于父亲）：

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

   倒序版把每个孩子的和存在 `total` 里，父亲算完后可以 `del total[child]` 省内存。

**Python 提醒**：`max(freq.values())` 在空 `Counter` 上抛 `ValueError`；处理空树时要写 `default=0`（主解法已写），或先判断 `root is None`。
