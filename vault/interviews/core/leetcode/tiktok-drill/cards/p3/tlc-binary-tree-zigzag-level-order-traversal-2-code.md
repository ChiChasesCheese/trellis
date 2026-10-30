---
id: tlc-binary-tree-zigzag-level-order-traversal-2-code
node: p3.binary-tree-zigzag-level-order-traversal
type: qa
step: 2
---
## Q
**LC 103 二叉树的锯齿形层序遍历**｜写出 Python 实现

二叉树根节点 `root`，节点数 `[0, 2000]`，节点值 `-100 <= Node.val <= 100`。返回锯齿形层序遍历：第一层从左往右，第二层从右往左，交替进行。

## A
**思路。** 用列表 `level` 存当前层的节点，始终按从左到右排列。每轮先取出这一层的值，奇数层反转后再写进答案；然后用推导式生成下一层。遍历方向从不改变，只有输出被反转。

```python
def zigzag_level_order(root: TreeNode | None) -> list[list[int]]:
    if root is None:
        return []
    res: list[list[int]] = []
    level = [root]                      # 当前层的节点，始终按从左到右存放
    left_to_right = True
    while level:
        vals = [node.val for node in level]
        res.append(vals if left_to_right else vals[::-1])   # 只在输出时反转
        level = [child for node in level
                 for child in (node.left, node.right) if child]
        left_to_right = not left_to_right
    return res
```

运行：`[3,9,20,null,null,15,7]` → `[[3], [20, 9], [15, 7]]`，`[1]` → `[[1]]`，`[]` → `[]`，`[1,2,3,4,null,null,5]` → `[[1], [3, 2], [4, 5]]`，2000 个节点的单链树 → 2000 层。

**复杂度。** 时间 `O(n)`：每个节点进 `level` 一次、被反转至多一次；空间 `O(w)`，`w` 是最宽一层的节点数。

**写法要点。** 用「当前层列表 + 推导式生成下一层」代替 `deque`：不需要 `len(queue)` 快照，层的边界天然清楚。推导式里两个 `for` 的顺序是「先遍历节点，再遍历它的两个孩子」，写反会报错；`if child` 过滤掉 `None`。`vals[::-1]` 新建反转后的副本，原 `vals` 不变；`left_to_right = not left_to_right` 比用层号取模更直白。
