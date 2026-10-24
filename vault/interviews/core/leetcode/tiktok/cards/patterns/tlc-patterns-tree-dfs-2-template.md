---
id: tlc-patterns-tree-dfs-2-template
node: patterns.tree-dfs
type: qa
step: 2
---
## Q
**二叉树 DFS（Tree DFS）｜模板：后序返回单侧收益，全局记录拐点（最大路径和 LC 124）**

写出「返回值」与「全局最优」分开的模板，说明每个节点向父节点返回什么、更新全局时用什么。

## A
```python
import math
def max_path_sum(root: TreeNode | None) -> int:
    best = -math.inf
    def gain(node: TreeNode | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left = max(gain(node.left), 0)     # 负收益的子树直接不要
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)   # 以 node 为最高点（拐点）的路径
        return node.val + max(left, right)          # 向父节点只能延伸一侧
    gain(root)
    return best
```

建树 `[1,2,3]` → `6`；`[-10,9,20,null,null,15,7]` → `42`；`[-3]` → `-3`；`[-2,-1]` → `-1`。时间 `O(n)`，空间 `O(h)`（`h` 为树高）。

通用三步：
1. **定义返回值**：`gain(node)` = 以 `node` 为起点、**向下延伸一侧**的最大路径和。
2. **用子树信息更新全局**：经过 `node` 的完整路径 = 值 + 左收益 + 右收益。
3. **向上返回时只带一侧**：父节点把 `node` 接在路径中间，不能再分叉。

同一个模板可以做：
- 直径 LC 543：`depth` 返回高度，`best = max(best, left + right)`。
- 最长同值路径、最长连续序列：把「值是否连续」变成延伸条件。

- `-math.inf` 初值：全负树的答案是单个节点的最大值，初值取 `0` 会错。
- 深度 `5000` 的单链树会触发 `RecursionError`（默认上限 `1000`）；LC 124 的树节点数最多 `3 * 10^4`，必要时改迭代后序。
