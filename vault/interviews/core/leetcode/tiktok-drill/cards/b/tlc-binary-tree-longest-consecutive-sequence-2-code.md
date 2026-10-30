---
id: tlc-binary-tree-longest-consecutive-sequence-2-code
node: b.binary-tree-longest-consecutive-sequence
type: qa
step: 2
---
## Q
**LC 298 二叉树最长连续序列**｜写出 Python 实现

二叉树节点数 `1` 到 `3 * 10^4`，值在 `[-3 * 10^4, 3 * 10^4]`。求最长的、每步恰好加一且只能向下走的路径包含的节点数，路径起点任意。

## A
**思路。** 自顶向下递归 `dfs(node, length)`，`length` 是以 `node` 结尾的连续长度，根的长度是 `1`。进入节点先更新答案；对每个孩子，若它的值恰好比当前节点大 `1`，长度加一，否则重置为 `1`，再递归。

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

运行：`[1,null,3,2,4,null,null,null,5]` → `3`，`[2,null,3,2,null,1]` → `2`，`[7]` → `1`；`30000` 个节点的右斜链（值 `1..30000`），调高递归上限后 → `30000`，默认上限下抛 `RecursionError`。

**复杂度。** 时间 `O(n)`：每个节点访问一次；空间 `O(h)`：递归栈深度等于树高，链状树是 `O(n)`。

**写法要点。** `nonlocal best` 让内层函数更新外层的全局最大值；`length` 作为参数往下传，每个节点自带上下文；`length + 1 if cond else 1` 是条件表达式，一次决定「延续或重置」；先更新答案再递归，叶子也会被统计到；深度超过约 `1000` 要 `sys.setrecursionlimit`，或用「追问」卡的显式栈版本。
