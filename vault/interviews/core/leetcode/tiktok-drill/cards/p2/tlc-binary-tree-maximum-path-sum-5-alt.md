---
id: tlc-binary-tree-maximum-path-sum-5-alt
node: p2.binary-tree-maximum-path-sum
type: qa
step: 5
---
## Q
**LC 124 二叉树中的最大路径和**｜另一种解法

用递归（后序 DFS）写这个问题，核心几行是什么？它和显式栈版本相比，什么时候该选哪个？

## A
**思路。** `dfs(node)` 返回「从 `node` 向下走的最大单链和」，空节点返回 `0`；在函数里顺便用 `nonlocal best` 刷新「以 `node` 为最高点」的路径和。

```python
def max_path_sum_rec(root: TreeNode | None) -> int:
    best = root.val
    def dfs(node: TreeNode | None) -> int:
        nonlocal best
        if node is None:
            return 0
        left = max(dfs(node.left), 0)              # 负增益不要
        right = max(dfs(node.right), 0)
        best = max(best, node.val + left + right)  # 以 node 为最高点
        return node.val + max(left, right)         # 往上只能带一边
    dfs(root)
    return best
```

运行：`[1,2,3]` → `6`，`[-10,9,20,null,null,15,7]` → `42`，`[-3]` → `-3`，`[2,-1]` → `2`。

**复杂度。** 时间 `O(n)`；空间 `O(h)`，`h` 是树高（调用栈），链状树时 `O(n)`。

**什么时候选哪个。**
- 面试白板/限时：递归版只有七八行，思路一眼可见，先写它。
- 树很深：题目允许 `3×10^4` 个节点连成一条链，Python 默认递归上限约 `1000`，递归版在 `3×10^4` 深的链上会 `RecursionError`。要么改用显式栈版本，要么在函数开头 `sys.setrecursionlimit(100000)`（Python 3.12+ 纯 Python 递归不再占 C 栈，设为 `100000` 后可通过 `3×10^4` 深的链；旧版本还要用线程放大栈）。
- 需要极限稳定的线上代码：用显式栈，不依赖解释器的递归配置。

**补充。** 两个版本共享同一个不变量：`best` 只在「以该节点为最高点」时用两侧之和刷新，向上返回只用较大的一侧。
