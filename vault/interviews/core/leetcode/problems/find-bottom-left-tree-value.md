---
slug: find-bottom-left-tree-value
---
## Q
**LC 513 找树左下角的值**｜Medium

给二叉树根结点，返回最后一层（最深层）最左边结点的值。

## A
**一句话。** 层序时每层先入右孩子再入左孩子，整个队列最后弹出的结点就是左下角。

```python
def find_bottom_left_value(root):
    q = deque([root])
    while q:
        node = q.popleft()
        if node.right:           # 先右后左
            q.append(node.right)
        if node.left:
            q.append(node.left)
    return node.val              # 最后弹出的是最后一层最左
```

**复杂度。** 时间 `O(n)`，空间 `O(w)`（`w` 为最宽一层）。

**易错点。**
- 先左后右：最后弹出的变成最右结点。
- 取「最深的叶子」：最深层的最左结点不一定是左孩子，也可能是某个结点的右孩子。

**追问。**
- DFS 怎么做？：先左后右前序遍历，记录最大深度，只有严格更深时才更新答案，这样同深度保留最左。
- 想少用空间？：DFS 只用 `O(h)`，BFS 要 `O(w)`。

**同模式。** LC 1302 层数最深叶子节点的和、LC 102 二叉树的层序遍历、LC 199 二叉树的右视图、LC 662 二叉树最大宽度
