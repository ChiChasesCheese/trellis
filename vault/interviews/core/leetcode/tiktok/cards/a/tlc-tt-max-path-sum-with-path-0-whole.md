---
id: tlc-tt-max-path-sum-with-path-0-whole
node: a.tt-max-path-sum-with-path
type: qa
---
## Q
**二叉树最大路径和（并输出路径）**｜Hard · TikTok 高频

二叉树的每个节点有整数值（可以为负）。路径是树中一条相连的节点序列，每个节点至多出现一次，不要求经过根或叶子；路径和是路径上节点值之和。求路径和的最大值，**并返回取得最大和的那条路径**（节点序列）。节点数 `1 <= n <= 3 * 10^4`，`-1000 <= val <= 1000`，树可能退化成一条链。例：`-10 -> (9, 20 -> (15, 7))` → `42`，路径 `[15, 20, 7]`；`1 -> (2, 3)` → `6`，路径 `[2, 1, 3]`；单个节点 `-3` → `-3`，路径 `[-3]`；`-3 -> (-1, -2)` → `-1`，路径 `[-1]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 后序遍历：每个节点计算「从它出发向下走的单链最大和」`gain`（负的分支直接放弃，当作 `0`）；经过该节点、左右都可延伸的路径和是 `val + 左分支 + 右分支`，用它更新全局最优，并记下「拐点」`peak`；同时记下每个节点的最优单链在它之后走向哪个孩子（`down`）。最后从拐点出发，向左、向右沿 `down` 各展开一条臂，拼起来就是路径。显式栈，`O(n)` 时间。

**识别。** 「任意两节点之间的路径、不要求过根」是树形 DP：路径有一个最高点（拐点），两条臂向下延伸。每个节点向父亲提供的只能是**一条**向下的链（因为路径不能分叉再回头）；而在节点处统计答案时，可以用两条臂。「输出路径」要求不只是数值，要在 DP 的同时记录选择。节点数 `3 * 10^4` 的链状树会让 Python 递归超限，用显式栈。

**推导。** 暴力：枚举所有节点对，求路径和，`O(n^2)` 到 `O(n^3)`。浪费：路径和是可分解的——以某节点为拐点的最优路径 = 自己 + 左边最好的单链 + 右边最好的单链，各子树的最好单链只需算一次。洞察：`gain[v] = val + max(0, gain[左], gain[右])` 自底向上算；答案是 `max(val + max(0, gain[左]) + max(0, gain[右]))`；每次更新答案时记下拐点，每个节点记下选了哪边，路径就能还原。

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def max_path_sum(root: TreeNode) -> tuple[int, list[TreeNode]]:
    """返回 (最大路径和, 取得最大和的路径上的节点序列)。后序遍历用显式栈，树再深也不会 RecursionError。"""
    order: list[TreeNode] = []
    stack = [root]
    while stack:                                   # 先序（根、右、左）入表，倒过来就是「孩子先于父亲」
        node = stack.pop()
        order.append(node)
        stack.extend(child for child in (node.left, node.right) if child)
    gain: dict[TreeNode, int] = {}                 # gain[v]：从 v 出发向下走的单链最大和（至少含 v）
    down: dict[TreeNode, TreeNode | None] = {}     # down[v]：这条最优单链在 v 之后走向哪个孩子
    best, peak = root.val, root                    # peak：全局最优路径的「拐点」，路径在这里左右分叉
    for node in reversed(order):
        left = gain[node.left] if node.left and gain[node.left] > 0 else 0       # 负贡献的分支直接不要
        right = gain[node.right] if node.right and gain[node.right] > 0 else 0
        down[node] = node.left if left and left >= right else node.right if right else None
        gain[node] = node.val + max(left, right)
        if node.val + left + right > best:         # 经过 node、两边都可以延伸的路径
            best, peak = node.val + left + right, node
    def arm(child: TreeNode | None) -> list[TreeNode]:
        chain = []
        while child:
            chain.append(child)
            child = down[child]
        return chain
    left_arm = arm(peak.left) if peak.left and gain[peak.left] > 0 else []
    right_arm = arm(peak.right) if peak.right and gain[peak.right] > 0 else []
    return best, left_arm[::-1] + [peak] + right_arm
```

运行：`-10 -> (9, 20 -> (15, 7))` → `(42, [15, 20, 7])`；`1 -> (2, 3)` → `(6, [2, 1, 3])`；单个 `-3` → `(-3, [-3])`；`-3 -> (-1, -2)` → `(-1, [-1])`；`1 -> (-5, 3)` → `(4, [1, 3])`；`1 -> (2 -> (3, 3))` → `(8, [3, 2, 3])`；`3 * 10^4` 层的左链（全 `1`）→ `(30001, 路径长度 30001)`，没有 `RecursionError`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`（遍历表和两个字典）。

**易错点。**
- 不放弃负贡献的分支：`1 -> (-5, 3)` 不 `max(0, …)` 得到 `3`，正确是 `4`（路径 `1 -> 3`，不要 `-5`）。
- 向父亲返回两条臂：`gain` 必须只带一条链，`1 -> (2 -> (3, 3))` 若把 `val + 左 + 右` 返回给父亲，会得到非法的 `9`（路径折回去再走一次），正确是 `8`。
- 答案初值取 `0`：全负的树 `-3` 得到 `0`（空路径），`-3 -> (-1, -2)` 也得到 `0`，正确是 `-3` 和 `-1`；初值取根的值（或负无穷）。
- 还原路径时左臂要反转：左臂是从拐点往下展开的，拼接时要倒过来，使整条路径从一端走到另一端。

**追问。**
- 只要数值：去掉 `down` 和 `arm`，`O(n)` 时间、`O(h)` 额外空间（递归）。
- 路径必须经过根 / 必须从根到叶：改成只在根处统计 / 只统计到叶子的单链。
- 多条路径并列最大：返回任意一条即可，要全部就收集所有等于 `best` 的拐点分别展开。

**同模式。** LC 124 二叉树中的最大路径和、LC 543 二叉树的直径、LC 687 最长同值路径、LC 1372 二叉树中的最长交错路径。
