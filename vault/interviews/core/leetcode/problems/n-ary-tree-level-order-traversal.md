---
slug: n-ary-tree-level-order-traversal
---
## Q
**LC 429 N 叉树的层序遍历**｜Medium

给 N 叉树（每个节点有 `val` 和 `children` 列表），返回其节点值的层序遍历，每层一个列表。

## A
**一句话。** 用一层的节点列表作队列：先收集本层的值，再把所有孩子拼成下一层。

```python
def level_order(root):
    if not root:
        return []
    ans, level = [], [root]
    while level:
        ans.append([n.val for n in level])   # 本层的值
        level = [c for n in level for c in n.children]
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 空树直接访问 `root.val`：先判空，返回 `[]`。
- 层与层混在一起：要按层分开，不能只用一个队列弹出元素而不记层大小。
- 孩子列表为 `None`：题目里叶子的 `children` 是空列表，若来自别处要先判。

**追问。**
- 用队列的写法？：每轮先记 `len(q)`，循环这么多次，弹出节点并把孩子入队。
- 想要之字形或自底向上？：同样的层序，之字形对奇数层反转，自底向上最后整体反转。

**同模式。** LC 102 二叉树的层序遍历、LC 107 二叉树的层序遍历 II、LC 559 N 叉树的最大深度
