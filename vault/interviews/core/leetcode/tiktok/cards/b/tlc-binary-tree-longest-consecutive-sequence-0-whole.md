---
id: tlc-binary-tree-longest-consecutive-sequence-0-whole
node: b.binary-tree-longest-consecutive-sequence
type: qa
---
## Q
**LC 298 二叉树最长连续序列**｜Medium · LC TikTok 热度 50/100 · CodeTop 国内累计 2 次 · 最近 2025-03-13（CodeTop）

给二叉树根节点 `root`，求其中**最长连续序列路径**的长度。连续序列路径是依次递增 `1` 的路径，可以从任意节点开始，沿「父 → 子」方向向下走，不能反向。节点数在 `[1, 3 * 10^4]`，`-3 * 10^4 <= Node.val <= 3 * 10^4`。例：`[1,null,3,2,4,null,null,null,5]` → `3`（`3-4-5`）；`[2,null,3,2,null,1]` → `2`（`2-3`；`3-2-1` 是递减，不算）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 自顶向下遍历，把「以当前节点结尾的连续序列长度」顺着往下传：子节点值恰好是父节点值加一就把长度加一，否则从 `1` 重新开始；全程取最大值。递归实现，`O(n)`。

**识别。** 「树上的路径 + 方向固定（父到子）+ 条件只和相邻两个节点有关」= 树的 DFS，状态就是「到这个节点为止的连续长度」，一个整数自顶向下传递即可。递归最直观：`dfs(node, length)` 把长度带给孩子；`n = 3 · 10^4` 且树可能退化成链时递归深度超过 CPython 默认上限约 `1000`，见易错点和追问。

**推导。** 暴力：以每个节点为起点向下找最长连续路径，退化成链时 `O(n^2)` → 观察：以节点 `v` 结尾的连续序列长度只取决于父节点的长度和 `v.val == parent.val + 1`，不用重复向下找 → 自顶向下传递 `length`：子节点值 `== 父值 + 1` 则 `length + 1`，否则重置为 `1`，每个节点只处理一次 → 写成 `dfs(node, length)`，进入节点时更新答案、再带着新长度递归两个孩子。

```python
def longest_consecutive(root: TreeNode | None) -> int:
    best = 0

    def dfs(node: TreeNode, length: int) -> None:
        nonlocal best
        best = max(best, length)                 # length：以 node 结尾的连续递增路径长度
        for child in (node.left, node.right):
            if child:
                dfs(child, length + 1 if child.val == node.val + 1 else 1)

    if root:
        dfs(root, 1)
    return best
```

运行：`[1,null,3,2,4,null,null,null,5]` → `3`，`[2,null,3,2,null,1]` → `2`，单节点 `[7]` → `1`；节点数 `30000` 的右斜链（值 `1..30000`），调高递归上限后 → `30000`；默认上限下抛 `RecursionError`。

**复杂度。** 时间 `O(n)`；空间 `O(h)`，`h` 是树高（递归栈），链状树为 `O(n)`。

**易错点。**
- 把条件写成 `abs(child.val - node.val) == 1`：把递减也算进去。`[2,null,3,2,null,1]` 得 `4`，正确是 `2`。
- 子节点不满足条件时忘了把长度重置为 `1`：长度会一直累加，答案偏大。
- 递归深度：链状树有 `30000` 层，CPython 默认递归上限约 `1000`，会抛 `RecursionError`；要么 `sys.setrecursionlimit` 调高，要么改成显式栈（见追问）。

**追问。**
- 树很深、递归会超限：显式栈，栈里放 `(节点, 以它结尾的长度)`，弹出时更新答案，带着新长度把孩子压栈，`O(n)` 时间，深度不受限。

```python
def longest_consecutive_iter(root: TreeNode | None) -> int:
    best = 0
    stack = [(root, 1)] if root else []          # (节点, 以它结尾的连续递增路径长度)
    while stack:
        node, length = stack.pop()
        best = max(best, length)
        for child in (node.left, node.right):
            if child:
                stack.append((child, length + 1 if child.val == node.val + 1 else 1))
    return best
```

- 路径可递增也可递减，还可以先上后下拐弯（LC 549）：后序遍历，每个节点返回（向下最长递增链，向下最长递减链），拐点处合并 `inc + dec - 1`。
- N 叉树 / 图：同样思路，遍历 `children`。
- 返回路径本身：递归时多带「起点节点」，更新 `best` 时记下起点和终点。

**同模式。** LC 549 二叉树中最长的连续序列、LC 124 二叉树中的最大路径和、LC 687 最长同值路径、LC 543 二叉树的直径。
