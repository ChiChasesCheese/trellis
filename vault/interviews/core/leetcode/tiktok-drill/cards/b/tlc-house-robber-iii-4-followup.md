---
id: tlc-house-robber-iii-4-followup
node: b.house-robber-iii
type: qa
step: 4
---
## Q
**LC 337 打家劫舍 III**｜追问

面试官接着问：（1）要返回具体偷了哪些房子，而不只是金额？（2）树换成多叉树？（3）`10^4` 个节点的链让递归爆栈？（4）房子围成环（LC 213）怎么办？

## A
1. **还原方案**：求出 `take`、`skip` 后自顶向下走一遍。根的决策是 `take[root] > skip[root]` 就偷；偷了某节点，它的孩子都走「不偷」分支；不偷某节点，每个孩子各自比较 `take` 与 `skip`，更大的那个决定它偷不偷。用递归带着 `(节点, 父亲是否被偷)` 向下走即可（需要先把每个节点的 `take`、`skip` 记进字典）。
2. **多叉树**：状态不变，`take[v] = v.val + Σ skip[c]`，`skip[v] = Σ max(take[c], skip[c])`，对 `children` 求和；递归里对 `children` 逐个调用 `go` 即可。
3. **递归爆栈**：`10^4` 的斜链超过默认递归上限（`1000`），抛 `RecursionError`。调大 `sys.setrecursionlimit`，或改迭代：先序入栈、倒序处理（孩子先于父亲）：

```python
def rob_stack(root: TreeNode | None) -> int:
    if root is None:
        return 0
    order: list[TreeNode] = []
    stack = [root]
    while stack:                              # 先序（根、右、左）：父一定排在子之前
        node = stack.pop()
        order.append(node)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    take: dict[TreeNode, int] = {}            # take[v]：偷 v 时子树最大收益
    skip: dict[TreeNode, int] = {}            # skip[v]：不偷 v 时子树最大收益
    for node in reversed(order):              # 倒序处理：孩子总先于父亲
        l, r = node.left, node.right
        skip[node] = max(take.get(l, 0), skip.get(l, 0)) + max(take.get(r, 0), skip.get(r, 0))
        take[node] = node.val + skip.get(l, 0) + skip.get(r, 0)
    return max(take[root], skip[root])
```
4. **环形（LC 213）**：断开首尾，分别对「去掉首」「去掉尾」两条链做线性打家劫舍，取较大值。

**Python 提醒**：返回元组再 `max(go(root))` 是在「两个状态里取较大」，别写成 `max(go(root)[0], ...)` 漏掉另一个状态。
