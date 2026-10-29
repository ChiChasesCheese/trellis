---
id: tlc-house-robber-iii-2-code
node: a.house-robber-iii
type: qa
step: 2
---
## Q
**LC 337 打家劫舍 III**｜写出 Python 实现

二叉树 `root`（`1 <= 节点数 <= 10^4`，`0 <= Node.val <= 10^4`），父子节点不能同时被偷，返回能偷到的最大金额。要求不因树退化成链而递归过深。

## A
**思路。** 先用栈做一遍先序，把节点按「父在子前」的顺序存进 `order`。再倒序遍历：每个节点用孩子的 `take / skip` 算出自己的两个值，字典里查不到的孩子（`None`）按 `0` 处理。

```python
def rob(root: TreeNode | None) -> int:
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

运行：`[3,2,3,null,3,null,1]` → `7`；`[3,4,5,1,3,null,1]` → `9`；`None` → `0`；`[5]` → `5`；`10^4` 个节点的斜链 → `5000`，没有 `RecursionError`。

**复杂度。** 时间 `O(n)`：每个节点入栈出栈各一次，倒序遍历一次；空间 `O(n)`。

**写法要点。** `dict.get(None, 0)` 把「空孩子」自然处理成 `0`，省去 `if l` 之类的分支；节点对象本身可作字典键（默认按对象身份哈希），不需要给节点编号；倒序遍历先序结果代替递归后序，深度再大也安全。
