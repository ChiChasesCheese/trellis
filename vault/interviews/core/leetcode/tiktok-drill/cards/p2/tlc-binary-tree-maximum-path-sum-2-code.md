---
id: tlc-binary-tree-maximum-path-sum-2-code
node: p2.binary-tree-maximum-path-sum
type: qa
step: 2
---
## Q
**LC 124 二叉树中的最大路径和**｜写出 Python 实现

二叉树根节点 `root`（节点数 `1` 到 `3×10^4`，节点值在 `[-1000, 1000]`），路径是相邻节点有边的节点序列、每个节点至多出现一次、至少含一个节点、不必经过根。返回最大路径和。

## A
**思路。** 后序递归：`gain(node)` 返回从 `node` 向下的最大单链和。对每个节点：左右增益取 `max(…, 0)`；以它为最高点的路径和刷新全局最大值；向上返回的增益只选较大的一侧。

```python
def max_path_sum(root: TreeNode | None) -> int:
    best = root.val                                # 初值不能是 0：全负树的答案是负数

    def gain(node: TreeNode | None) -> int:        # 从 node 向下走的最大单链和；空节点贡献 0
        nonlocal best
        if node is None:
            return 0
        left = max(gain(node.left), 0)             # 负收益的子树直接不要
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)  # 以 node 为最高点的路径：两侧都可以带
        return node.val + max(left, right)         # 往父亲返回时只能选一边

    gain(root)
    return best
```

运行：`[1,2,3]` → `6`，`[-10,9,20,null,null,15,7]` → `42`，`[-3]` → `-3`，`[2,-1]` → `2`，`[-2,-1]` → `-1`；3×10^4 个节点的链在默认递归上限下抛 `RecursionError`，把上限调到 100000 后 → `30000`。

**复杂度。** 时间 `O(n)`：每个节点访问一次；空间 `O(h)`：递归栈，`h` 是树高，链状树时 `O(n)`（默认递归上限约 1000，3×10^4 深的链会 `RecursionError`）。

**写法要点。** 空节点返回 `0`，省掉 `if node.left` 的分支；`nonlocal best` 让内层函数改外层变量，不用全局变量也不用传引用；`best` 用 `root.val` 初始化，保证全负树也对；左右增益先各自取 `max(…, 0)` 再相加，负子树自动舍弃。
