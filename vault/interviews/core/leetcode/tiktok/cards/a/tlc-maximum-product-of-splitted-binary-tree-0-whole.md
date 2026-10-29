---
id: tlc-maximum-product-of-splitted-binary-tree-0-whole
node: a.maximum-product-of-splitted-binary-tree
type: qa
---
## Q
**LC 1339 分裂二叉树的最大乘积**｜Medium · CodeTop 国内累计 2 次 · 最近 2026-03-10（CodeTop）

给一棵二叉树的根 `root`，删除**一条边**使它分裂成两棵子树，求两棵子树**节点值之和的乘积**的最大值。答案可能很大，返回对 `10^9 + 7` 取模后的结果。每棵树最多 `50000` 个节点，至少 `2` 个；节点值在 `[1, 10000]`。例：`root = [1,2,3,4,5,6]` → `110`（和为 `11` 和 `10`）；`root = [1,null,2,3,4,null,null,5,6]` → `90`；`root = [1,1]` → `1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 删一条边 = 把某个非根节点的子树切下来，另一半的和是 `total - s`；先求出每个子树的和 `s`，再对所有非根节点取 `max(s * (total - s))`，**最后**才取模。用迭代求子树和，避免 `50000` 层递归。`O(n)`。

**识别。** 「删一条边得到两部分、与两部分的和有关」→ 每条边对应唯一一个非根节点（切掉它与父亲的边），一部分的和就是**以它为根的子树和**，另一部分是 `total - s`；这是树上**后序累加**（子树和）的标准问题。`n = 50000` 意味着要 `O(n)`，且树可能是链，递归深度会爆。

**推导。** 暴力：对每条边实际断开，分别遍历两部分求和，`O(n^2)`。浪费：两部分的和互补，`total - s` 不需要再遍历；而所有子树和一次后序遍历就能全部得到。洞察：先得到整棵树的和 `total`，每个子树和 `s` 对应一种切法，乘积是 `s * (total - s)`；这是关于 `s` 的开口向下抛物线，越接近 `total/2` 越大，但直接枚举所有 `s` 取最大即可，不必找最接近的。最优：一次遍历求出所有子树和，再枚举，`O(n)` 时间 `O(n)` 空间。取模放在最后：先模再比较大小会选错。

```python
def max_product(root: TreeNode | None) -> int:
    MOD = 10**9 + 7
    order: list[TreeNode] = []                  # 先序（父在子前）
    parent: list[int] = []                      # parent[i]：order[i] 的父结点在 order 里的下标
    stack: list[tuple[TreeNode, int]] = [(root, -1)]
    while stack:
        node, p = stack.pop()
        idx = len(order)
        order.append(node)
        parent.append(p)
        for child in (node.left, node.right):
            if child:
                stack.append((child, idx))
    sums = [node.val for node in order]         # sums[i]：以 order[i] 为根的子树和
    for i in range(len(order) - 1, 0, -1):      # 倒着走：子一定先于父，累加到父上
        sums[parent[i]] += sums[i]
    total = sums[0]
    # 先在精确整数上取最大，最后才取模
    return max(s * (total - s) for s in sums[1:]) % MOD
```

运行：`[1,2,3,4,5,6]` → `110`，`[1,null,2,3,4,null,null,5,6]` → `90`，`[2,3,9,10,7,8,6,5,4,11,1]` → `1025`，`[1,1]` → `1`，`10 个节点的链，值都是 10000` → `499999986`。

**复杂度。** 时间 `O(n)`：每个节点入栈出栈一次，倒序累加一遍，再枚举一遍；空间 `O(n)`（`order`、`parent`、`sums`、栈）。

**易错点。**
- 先取模再比较：`s * (total - s) % MOD` 放进 `max`。10 个节点、值都是 `10000` 的链：真实最大乘积 `2500000000`，取模后 `499999986`；先模再比较会选中 `900000000`（`s = 10000` 那一种），输出 `900000000`，错。Python 整数不会溢出，所以可以放心用精确值比较，最后再 `% MOD`。
- 递归求子树和：链形树深度 `50000`，Python 默认递归深度 `1000`，直接 `RecursionError`；要么改迭代，要么 `sys.setrecursionlimit`（不推荐，可能段错误）。
- 把根节点也算进候选：根的子树和是 `total`，`total * 0 = 0`，不影响最大值，但枚举 `sums[1:]` 更清楚；要注意树至少有 2 个节点，所以候选非空。

**追问。**
- 返回应该删的是哪条边（或哪个子树）：枚举时用 `max(range(1, n), key=...)` 取下标，再回到 `order[i]`。
- 不是二叉树而是 N 叉树，或直接给 `parent[]` 数组：同样的倒序累加，父下标小于子下标时根本不需要建树。
- 递归写法：面试可先写递归（后序返回子树和），说明会爆栈，再改成本解的迭代。

**同模式。** LC 508 出现次数最多的子树元素和、LC 563 二叉树的坡度、LC 543 二叉树的直径、LC 337 打家劫舍 III、LC 124 二叉树中的最大路径和。
