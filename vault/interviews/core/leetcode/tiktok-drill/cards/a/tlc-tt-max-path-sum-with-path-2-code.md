---
id: tlc-tt-max-path-sum-with-path-2-code
node: a.tt-max-path-sum-with-path
type: qa
step: 2
---
## Q
**二叉树最大路径和（并输出路径）**｜写出 Python 实现

写 `max_path_sum(root)`：二叉树节点 `TreeNode`（`val`、`left`、`right`），`1 <= n <= 3 * 10^4`，`-1000 <= val <= 1000`，可能退化成链。路径是相连的节点序列，不要求过根或叶，每个节点至多出现一次。返回 `(最大路径和, 路径上的节点列表)`，路径从一端按顺序走到另一端。

## A
**思路。** 先序遍历（根、右、左）记录访问顺序，倒着处理就是孩子先于父亲。每个节点算 `gain`（向下单链最大和，负分支当 `0`），记录 `down`（单链走向），在 `val + 左 + 右` 刷新最优时记下拐点 `peak`。最后从拐点向左、向右沿 `down` 展开两条臂，左臂反转后拼接。

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

运行：`-10 -> (9, 20 -> (15, 7))` → `(42, [15, 20, 7])`；`1 -> (2, 3)` → `(6, [2, 1, 3])`；单个 `-3` → `(-3, [-3])`；`-3 -> (-1, -2)` → `(-1, [-1])`；`1 -> (-5, 3)` → `(4, [1, 3])`；`1 -> (2 -> (3, 3))` → `(8, [3, 2, 3])`；`3 * 10^4` 层的左链 → `(30001, 路径长度 30001)`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**写法要点。**
- 以节点对象作为 `dict` 的键：`TreeNode` 默认按身份哈希，值相同的不同节点不会混淆；不用给每个节点加额外字段。
- 先序入表再 `reversed`：不写递归也能得到「孩子先于父亲」的处理顺序；栈里先压左后压右，只影响访问顺序，不影响正确性。
- 链式条件表达式 `A if c1 else B if c2 else None` 从左到右判断：左分支有正贡献且不小于右分支就选左，否则右分支有正贡献选右，都没有就是 `None`（单链到此为止）。
- 内层函数 `arm` 只沿 `down` 走链，不递归；左臂从上往下收集，最后 `[::-1]` 使整条路径连贯。
