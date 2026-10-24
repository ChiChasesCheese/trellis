---
id: tlc-maximum-width-of-binary-tree-2-code
node: a.maximum-width-of-binary-tree
type: qa
step: 2
---
## Q
**LC 662 二叉树最大宽度**｜写出 Python 实现

二叉树节点数在 `[1, 3000]`。每层的宽度是该层最左与最右非空节点之间的长度，两端点之间的空节点也计入。返回各层宽度的最大值。要求 `O(n)`，且中间编号不能随深度指数增长。

## A
**思路。** 层序遍历，队列里存 `(节点, 编号)`。每层先取最左编号 `base`，宽度是 `level[-1][1] - base + 1`；生成下一层时用相对编号 `idx - base`，孩子是 `2 * idx` 和 `2 * idx + 1`。

```python
def width_of_binary_tree(root: TreeNode | None) -> int:
    if root is None:
        return 0
    best = 0
    level: list[tuple[TreeNode, int]] = [(root, 0)]      # (节点, 它在满二叉树该层里的编号)
    while level:
        base = level[0][1]                               # 本层最左编号，用来归零
        best = max(best, level[-1][1] - base + 1)
        nxt: list[tuple[TreeNode, int]] = []
        for node, idx in level:
            idx -= base                                  # 归零后编号不会随深度指数膨胀
            if node.left:
                nxt.append((node.left, 2 * idx))
            if node.right:
                nxt.append((node.right, 2 * idx + 1))
        level = nxt
    return best
```

运行：`[1,3,2,5,3,null,9]` → `4`，`[1,3,2,5,null,null,9,6,null,7]` → `7`，`[1,3,2,5]` → `2`，`[1]` → `1`，3000 个节点的右链 → `1`。

**复杂度。** 时间 `O(n)`：每个节点进出各一次；空间 `O(w)`：一层的节点和编号，`w` 为最大层宽（最多 `n`）。

**写法要点。**
- 按层处理用「当前层列表 + 下一层列表」，不用 `deque` 加 `for _ in range(len(q))`：层的首尾元素可以直接用 `level[0]`、`level[-1]` 取，不用记下标。
- 元组 `(node, idx)` 在 `for node, idx in level` 里直接解包。
- `idx -= base` 放在生成孩子之前：孩子编号基于归零后的值，宽度仍由未归零的首尾差计算（它们同减 `base`，差不变）。
- `if node.left:` 对节点对象做真值判断是安全的（节点对象永远为真），不会被节点值 `0` 干扰。
