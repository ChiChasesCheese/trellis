---
id: tlc-binary-tree-level-order-traversal-ii-2-code
node: p5.binary-tree-level-order-traversal-ii
type: qa
step: 2
---
## Q
**LC 107 二叉树的层序遍历 II**｜写出 Python 实现

二叉树根结点 `root`（结点数 `0` 到 `2000`，`TreeNode` 有 `val`、`left`、`right`）。返回自底向上的层序遍历：最底层在最前，每层内从左到右。空树返回 `[]`。

## A
**思路。** `level` 保存当前层的所有结点（初始为 `[root]`，空树则为空）。每轮：把这一层的值收集成一个列表，再用这一层所有结点的非空孩子生成下一层。循环结束后整体反转。

```python
def level_order_bottom(root: TreeNode | None) -> list[list[int]]:
    ans: list[list[int]] = []
    level = [root] if root else []
    while level:
        ans.append([node.val for node in level])              # 这一层的值，从左到右
        level = [child for node in level for child in (node.left, node.right) if child]   # 下一层
    return ans[::-1]                                          # 自顶向下收集，最后整体反转
```

运行：`[3,9,20,null,null,15,7]` → `[[15, 7], [9, 20], [3]]`，`[1]` → `[[1]]`，`[]` → `[]`，`[1,2,3,4,null,null,5]` → `[[4, 5], [2, 3], [1]]`；2000 个结点的单链树 → 2000 层。

**复杂度。** 时间 `O(n)`：每个结点在 `level` 里出现一次；空间 `O(n)`：答案占 `n`，`level` 最多是最宽的一层。

**写法要点。** 用「整层列表」代替队列加 `size`，不需要 `deque` 和 `popleft`，层边界天然清晰；`[child for node in level for child in (node.left, node.right) if child]` 的嵌套顺序是「外层循环在前、内层在后」，与两层 `for` 的书写顺序一致，`if child` 过滤 `None`；`ans[::-1]` 返回反转后的新列表，原地反转用 `ans.reverse()`；若队列用 `list.pop(0)`，每次是 `O(n)`，要避免。
