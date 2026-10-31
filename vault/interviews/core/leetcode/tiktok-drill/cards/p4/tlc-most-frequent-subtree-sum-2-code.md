---
id: tlc-most-frequent-subtree-sum-2-code
node: p4.most-frequent-subtree-sum
type: qa
step: 2
---
## Q
**LC 508 出现次数最多的子树元素和**｜写出 Python 实现

二叉树 `root`（节点数 `[1, 10^4]`，`-10^5 <= Node.val <= 10^5`），返回出现次数最多的子树元素和，并列时全部返回，顺序不限。

## A
**思路。** 后序递归：`subtree_sum(node)` 返回以 `node` 为根的子树和 = 自身值 + 左右子树和，算出后在 `Counter` 里计一次。最后取最大次数，把所有达到它的和列出来。

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

运行：`[5,2,-3]` → `[-3, 2, 4]`（排序后）；`[5,2,-5]` → `[2]`；`[0]` → `[0]`；`10^4` 个节点的右斜链 → `10000` 个和各出现一次，全部返回（调大递归上限后；默认上限下抛 `RecursionError`）。

**复杂度。** 时间 `O(n)`：每个节点访问一次，计数与取最大各 `O(n)`；空间 `O(n)`：`freq` 加最深 `O(n)` 的递归栈。

**写法要点。** `subtree_sum(None)` 返回 `0`，叶子不需要特判；`subtree_sum` 是嵌套函数，直接往外层的 `freq` 里计数，不用 `nonlocal`（只改内容、不重绑名字）；`Counter` 的 `freq[s] += 1` 对新键默认从 `0` 起；`max(freq.values())` 配合列表推导式能收集**所有**并列众数，比 `most_common(1)` 更不容易漏；`default=0` 让空树不抛 `ValueError`。
