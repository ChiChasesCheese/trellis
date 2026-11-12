---
slug: binary-tree-zigzag-level-order-traversal
---
## Q
**LC 103 二叉树的锯齿形层序遍历**｜Medium

返回二叉树的层序遍历，第一层从左往右，第二层从右往左，交替进行。

## A
**一句话。** 照常 BFS，每层始终按从左到右存放，只在写入答案时按层号奇偶反转。

```python
def zigzag_level_order(root):
    if root is None:
        return []
    res = []
    level = [root]              # 始终从左到右
    ltr = True
    while level:
        vals = [node.val for node in level]
        res.append(vals if ltr else vals[::-1])   # 只在输出时反转
        level = [c for node in level
                 for c in (node.left, node.right) if c]
        ltr = not ltr
    return res
```

**复杂度。** 时间 `O(n)`，空间 `O(w)`。

**易错点。**
- 反转遍历用的 `level`：下一层左右顺序乱掉，第 3 层会得 `[6,7,4,5]` 而非 `[4,5,6,7]`。
- 开关初值写反：第 0 层是正序，`[3,9,20,null,null,15,7]` 会得 `[[3],[9,20],…]`。
- 空树返回 `[[]]`：应为 `[]`。

**追问。**
- 自底向上层序（LC 107）？：最后 `res.reverse()`。
- 只要每层最右的节点（LC 199）？：每层取 `level[-1]`。

**同模式。** LC 102 二叉树的层序遍历、LC 107 层序遍历 II、LC 199 二叉树的右视图、LC 637 二叉树的层平均值
