---
id: tlc-tt-max-path-sum-with-path-2-code
node: p3.tt-max-path-sum-with-path
type: qa
step: 2
---
## Q
**二叉树最大路径和（并输出路径）**｜写出 Python 实现

写 `max_path_sum(root)`：二叉树节点 `TreeNode`（`val`、`left`、`right`），`1 <= n <= 3 * 10^4`，`-1000 <= val <= 1000`，可能退化成一条链。路径是相连的节点序列，不要求过根或叶，每个节点至多出现一次。返回 `(最大路径和, 路径上的节点列表)`，路径从一端按顺序走到另一端。

## A
**思路。** 后序递归：`dfs(node)` 返回「从 `node` 向下的单链最大和」`gain`，负分支当 `0`。在每个节点用 `val + 左 + 右` 刷新全局最优并记下拐点 `peak`，同时记录每个节点的最优单链走向 `down`。最后从拐点向左、向右沿 `down` 展开两条臂，左臂反转后拼接。

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def max_path_sum(root: TreeNode) -> tuple[int, list[TreeNode]]:
    gain: dict[TreeNode, int] = {}                 # gain[v]：从 v 出发向下走的单链最大和（至少含 v）
    down: dict[TreeNode, TreeNode | None] = {}     # down[v]：这条最优单链在 v 之后走向哪个孩子
    best, peak = root.val, root                    # peak：全局最优路径的「拐点」，路径在这里左右分叉

    def dfs(node: TreeNode | None) -> int:
        nonlocal best, peak
        if node is None:
            return 0
        left, right = max(dfs(node.left), 0), max(dfs(node.right), 0)   # 负贡献的分支直接不要
        down[node] = node.left if left and left >= right else node.right if right else None
        gain[node] = node.val + max(left, right)
        if node.val + left + right > best:         # 经过 node、两边都可以延伸的路径
            best, peak = node.val + left + right, node
        return gain[node]

    dfs(root)

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

运行：`-10 -> (9, 20 -> (15, 7))` → `(42, [15, 20, 7])`；`1 -> (2, 3)` → `(6, [2, 1, 3])`；单个 `-3` → `(-3, [-3])`；`-3 -> (-1, -2)` → `(-1, [-1])`；`1 -> (-5, 3)` → `(4, [1, 3])`；`1 -> (2 -> (3, 3))` → `(8, [3, 2, 3])`；`3 * 10^4` 层的左链：默认递归上限下抛 `RecursionError`，调高上限后 → `(30000, 路径长度 30000)`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`（两个字典；递归栈深度是树高）。

**写法要点。**
- 以节点对象作为 `dict` 的键：`TreeNode` 默认按身份哈希，值相同的不同节点不会混淆；不用给每个节点加额外字段。
- `nonlocal best, peak` 让内层递归函数更新外层的全局最优，不必把它们当返回值层层传递。
- `max(dfs(node.left), 0)`：空节点返回 `0`，负贡献的分支也当 `0`，一个 `max` 同时处理两件事。
- 链式条件表达式 `A if c1 else B if c2 else None` 从左到右判断：左分支有正贡献且不小于右分支就选左，否则右分支有正贡献选右，都没有就是 `None`（单链到此为止）。
- 内层函数 `arm` 只沿 `down` 走链，不递归；左臂从上往下收集，最后 `[::-1]` 使整条路径连贯。
- 深链上递归会超过约 `1000` 层的默认上限：调高 `sys.setrecursionlimit`，或用 「另一种解法」卡的显式栈版本。
