---
id: tlc-house-robber-iii-2-code
node: b.house-robber-iii
type: qa
step: 2
---
## Q
**LC 337 打家劫舍 III**｜写出 Python 实现

二叉树 `root`（`1 <= 节点数 <= 10^4`，`0 <= Node.val <= 10^4`），父子节点不能同时被偷，返回能偷到的最大金额。

## A
**思路。** 后序递归：`go(node)` 返回 `(偷 node 的最大收益, 不偷 node 的最大收益)`。空孩子返回 `(0, 0)`；偷当前节点时孩子取各自的「不偷」，不偷时孩子各取两者较大。

```python
def rob(root: TreeNode | None) -> int:
    def go(node: TreeNode | None) -> tuple[int, int]:   # (偷 node 时子树最大收益, 不偷 node 时子树最大收益)
        if node is None:
            return 0, 0
        take_l, skip_l = go(node.left)
        take_r, skip_r = go(node.right)
        take = node.val + skip_l + skip_r                # 偷它：孩子必须不偷
        skip = max(take_l, skip_l) + max(take_r, skip_r) # 不偷它：孩子偷不偷都行，各取较大
        return take, skip

    return max(go(root))
```

运行：`[3,2,3,null,3,null,1]` → `7`；`[3,4,5,1,3,null,1]` → `9`；`None` → `0`；`[5]` → `5`；`10^4` 个节点的斜链 → `5000`（调大递归上限后；默认上限下抛 `RecursionError`）。

**复杂度。** 时间 `O(n)`：每个节点访问一次；空间 `O(h)`：递归栈，最坏 `O(n)`。

**写法要点。** `go(None)` 返回 `(0, 0)`，空孩子不需要特判；返回二元组而不是写两个函数，两个状态一次算完，避免孙子被重复求解；元组解包 `take_l, skip_l = go(...)` 让读孩子的两个状态一目了然；`max(go(root))` 在根的两个状态里取较大。
