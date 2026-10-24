---
id: tlc-binary-tree-longest-consecutive-sequence-0-whole
node: b.binary-tree-longest-consecutive-sequence
type: qa
---
## Q
**LC 298 二叉树最长连续序列**｜Medium · TikTok 高频

给二叉树根节点 `root`，求其中**最长连续序列路径**的长度。连续序列路径是依次递增 `1` 的路径，可以从任意节点开始，沿「父 → 子」方向向下走，不能反向。节点数在 `[1, 3 * 10^4]`，`-3 * 10^4 <= Node.val <= 3 * 10^4`。例：`[1,null,3,2,4,null,null,null,5]` → `3`（`3-4-5`）；`[2,null,3,2,null,1]` → `2`（`2-3`；`3-2-1` 是递减，不算）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 自顶向下遍历，把「以当前节点结尾的连续序列长度」顺着往下传：子节点值恰好是父节点值加一就把长度加一，否则从 `1` 重新开始；全程取最大值。`O(n)`；用显式栈避免深树的递归爆栈。

**识别。** 「树上的路径 + 方向固定（父到子）+ 条件只和相邻两个节点有关」= 树的 DFS，状态就是「到这个节点为止的连续长度」，一个整数自顶向下传递即可。`n = 3 · 10^4` 且树可能退化成链：Python 的默认递归深度是 `1000`，递归写法会 `RecursionError`。

**推导。** 暴力：以每个节点为起点向下找最长连续路径，退化成链时 `O(n^2)` → 观察：以节点 `v` 结尾的连续序列长度只取决于父节点的长度和 `v.val == parent.val + 1`，不用重复向下找 → 自顶向下传递 `length`：子节点值 `== 父值 + 1` 则 `length + 1`，否则重置为 `1`，每个节点只处理一次 → 把递归改成显式栈 `(节点, 长度)`，深度不再受限。

```python
def longest_consecutive(root: TreeNode | None) -> int:
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

运行：`[1,null,3,2,4,null,null,null,5]` → `3`，`[2,null,3,2,null,1]` → `2`，单节点 `[7]` → `1`；节点数 `30000` 的右斜链（值 `1..30000`）→ `30000`，不抛 `RecursionError`。

**复杂度。** 时间 `O(n)`；空间 `O(h)`，`h` 是树高（栈中最多同时有 `O(h)` 个待处理节点，链状树为 `O(n)`）。

**易错点。**
- 把条件写成 `abs(child.val - node.val) == 1`：把递减也算进去。`[2,null,3,2,null,1]` 得 `4`，正确是 `2`。
- 子节点不满足条件时忘了把长度重置为 `1`：长度会一直累加，答案偏大。
- 用递归实现：`30000` 层的链会抛 `RecursionError`（默认上限约 `1000`）。

**追问。**
- 路径可递增也可递减，还可以先上后下拐弯（LC 549）：后序遍历，每个节点返回（向下最长递增链，向下最长递减链），拐点处合并 `inc + dec - 1`。
- N 叉树 / 图：同样思路，遍历 `children`。
- 返回路径本身：栈里多带「起点节点」，更新 `best` 时记下起点和终点。

**同模式。** LC 549 二叉树中最长的连续序列、LC 124 二叉树中的最大路径和、LC 687 最长同值路径、LC 543 二叉树的直径。
