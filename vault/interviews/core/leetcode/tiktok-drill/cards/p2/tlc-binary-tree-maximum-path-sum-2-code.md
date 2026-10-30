---
id: tlc-binary-tree-maximum-path-sum-2-code
node: p2.binary-tree-maximum-path-sum
type: qa
step: 2
---
## Q
**LC 124 二叉树中的最大路径和**｜写出 Python 实现

二叉树根节点 `root`（节点数 `1` 到 `3×10^4`，节点值在 `[-1000, 1000]`），路径是相邻节点有边的节点序列、每个节点至多出现一次、至少含一个节点、不必经过根。返回最大路径和。要求不因树深而栈溢出。

## A
**思路。** 先用显式栈按「根、右、左」的顺序收集节点，倒过来遍历就是孩子先于父亲。对每个节点：左右增益取 `max(…, 0)`；以它为最高点的路径和刷新全局最大值；向上返回的增益只选较大的一侧。

```python
def max_path_sum(root: TreeNode | None) -> int:
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

运行：`[1,2,3]` → `6`，`[-10,9,20,null,null,15,7]` → `42`，`[-3]` → `-3`，`[2,-1]` → `2`，`[-2,-1]` → `-1`；3×10^4 个节点的链 → `30000`，不会 `RecursionError`。

**复杂度。** 时间 `O(n)`：收集一遍、倒序处理一遍；空间 `O(n)`：`order` 与 `gain` 字典。

**写法要点。** 先序的变体（根、右、左）倒过来就是一种后序，不需要「已访问」标记；`gain.get(node.left, 0)` 对 `None` 键返回默认值 `0`，省掉 `if node.left` 分支；`TreeNode` 默认按对象身份哈希，可以直接做字典的键；`best` 用 `root.val` 初始化，保证全负树也对。需要最简洁时写成递归。
