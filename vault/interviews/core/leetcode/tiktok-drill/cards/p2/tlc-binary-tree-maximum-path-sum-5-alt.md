---
id: tlc-binary-tree-maximum-path-sum-5-alt
node: p2.binary-tree-maximum-path-sum
type: qa
step: 5
---
## Q
**LC 124 二叉树中的最大路径和**｜另一种解法

不用递归（避免 `3×10^4` 深的链触发 `RecursionError`），用显式栈怎么写？它和递归版本相比，什么时候该选哪个？

## A
**思路。** 先用显式栈按「根、右、左」的顺序收集节点，倒过来遍历就是孩子先于父亲；用字典 `gain` 记每个节点「向下走的最大单链和」，处理每个节点时刷新「以它为最高点」的路径和。

```python
def max_path_sum_stack(root: TreeNode | None) -> int:
    order: list[TreeNode] = []
    stack = [root]
    while stack:                                   # 先序（根右左）收集节点：孩子总排在父亲后面
        node = stack.pop()
        order.append(node)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    gain: dict[TreeNode, int] = {}                 # gain[node]：从 node 向下走的最大单链和
    best = root.val
    for node in reversed(order):                   # 倒过来 = 孩子先于父亲
        left = max(gain.get(node.left, 0), 0)      # 负收益的子树直接不要；None 不在字典里，取 0
        right = max(gain.get(node.right, 0), 0)
        best = max(best, node.val + left + right)  # 以 node 为最高点的路径
        gain[node] = node.val + max(left, right)   # 往父亲返回时只能选一边
    return best
```

运行：`[1,2,3]` → `6`，`[-10,9,20,null,null,15,7]` → `42`，`[-3]` → `-3`，`[2,-1]` → `2`；`3×10^4` 个节点的链 → `30000`，不会 `RecursionError`。

**复杂度。** 时间 `O(n)`：收集一遍、倒序处理一遍；空间 `O(n)`：`order` 与 `gain`。

**什么时候选哪个。**
- 面试白板/限时：递归版只有七八行，思路一眼可见，先写它。
- 树很深：题目允许 `3×10^4` 个节点连成一条链，Python 默认递归上限约 `1000`，递归版在这种链上会 `RecursionError`。要么改用本卡的显式栈版本，要么在递归版开头 `sys.setrecursionlimit(100000)`（Python 3.12+ 纯 Python 递归不再占 C 栈，设为 `100000` 后可通过 `3×10^4` 深的链；旧版本还要用线程放大栈）。
- 需要极限稳定的线上代码：用显式栈，不依赖解释器的递归配置。

**补充。** 两个版本共享同一个不变量：`best` 只在「以该节点为最高点」时用两侧之和刷新，向上返回只用较大的一侧。
