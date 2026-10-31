---
id: tlc-house-robber-iii-0-whole
node: b.house-robber-iii
type: qa
---
## Q
**LC 337 打家劫舍 III**｜Medium · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 3 次 · 最近 2022-04-17（国内 CodeTop）

房屋排成一棵二叉树，`root` 是入口。如果**两个直接相连（父子）的房子在同一晚被偷**，就会报警。给定二叉树的 `root`，返回不触发警报时能偷到的最高金额。树的节点数在 `[1, 10^4]`，`0 <= Node.val <= 10^4`。例：`[3,2,3,null,3,null,1]` → `7`（`3 + 3 + 1`）；`[3,4,5,1,3,null,1]` → `9`（`4 + 5`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 树形 DP：每个节点算两个值——`take[v] = v.val + skip[左] + skip[右]`（偷它，孩子必须不偷），`skip[v] = max(take, skip)[左] + max(take, skip)[右]`（不偷它，孩子随意）；答案是 `max(take[root], skip[root])`，每个节点只算一次，`O(n)`。

**识别。** 「树 + 父子不能同时选 + 求最大和」就是树上的打家劫舍：每个节点只有「选 / 不选」两个状态，约束只在父子之间，可以自底向上合并。后序递归最直观；节点数到 `10^4` 意味着树可能退化成链，递归深度见易错点。

**推导。** 暴力递归：偷根则加上孙子们的最优，不偷根则累加两个孩子的最优，取最大 → 孙子被「偷根」和「不偷根」两条路各算一遍，子问题大量重复 → 每个子树其实只要两个数（偷根 / 不偷根）就够了，后序一次算完，父亲直接读孩子的两个数 → `O(n)`：递归函数返回 `(偷, 不偷)` 二元组，孩子先于父亲。

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

运行：`[3,2,3,null,3,null,1]` → `7`；`[3,4,5,1,3,null,1]` → `9`；`None` → `0`；`[5]` → `5`；`10^4` 个节点的左斜链（每个值为 `1`）→ `5000`（调大递归上限后；默认上限下抛 `RecursionError`）。

**复杂度。** 时间 `O(n)`，每个节点访问一次；空间 `O(h)`（递归栈），`h` 为树高，最坏 `O(n)`。

**易错点。**
- 「不偷根」写成 `skip[l] + skip[r]`（以为孩子也必须不偷）：`[3,4,5,1,3,null,1]` 得到 `3`，正确是 `9`。不偷当前节点时孩子可偷可不偷，要取 `max`。
- 按层奇偶性贪心（偷奇数层或偶数层）：`[2,1,3,null,4]` 给出 `6`，正确是 `7`（`3 + 4`，分属不同的层）。
- 递归深度：`10^4` 个节点的链，递归深度 `10^4`，超过 CPython 默认递归上限约 `1000`，抛 `RecursionError`；要 `sys.setrecursionlimit` 调大，或改成迭代（见追问）。

**追问。**
- 返回具体偷了哪些房子：记录每个节点的决策，从根出发自顶向下回溯；偷了父亲，孩子就走 `skip` 分支。
- 不想动递归上限：先用栈做一遍先序得到 `order`，倒序遍历（孩子先于父亲），两个状态存字典：
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
- 推广到多叉树：两个状态不变，`take[v] = v.val + Σ skip[c]`，`skip[v] = Σ max(take[c], skip[c])`。
- 房子围成环（LC 213）：断环，分别算「不含首」与「不含尾」两条链，取较大者。

**同模式。** LC 198 / 213 打家劫舍 I / II、LC 124 二叉树中的最大路径和、LC 968 监控二叉树、LC 1372 二叉树中的最长交错路径。
