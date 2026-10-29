---
id: tlc-convert-binary-search-tree-to-sorted-doubly-linked-list-2-code
node: a.convert-binary-search-tree-to-sorted-doubly-linked-list
type: qa
step: 2
---
## Q
**LC 426 将二叉搜索树转化为排序的双向链表**｜写出 Python 实现

`Node` 有 `val`、`left`、`right`。给定二叉搜索树的根（节点数 `0` 到 `2000`，值互不相同），原地把它转成排序的循环双向链表：`left` 为前驱，`right` 为后继，最小节点的前驱是最大节点，最大节点的后继是最小节点。返回最小节点；空树返回 `None`。

## A
**思路。** 迭代中序遍历：先一路向左入栈，弹出一个节点就是下一个最小的。若 `prev` 非空，让 `prev.right = node`、`node.left = prev`；否则它是第一个节点，记为 `first`。然后转向右子树。遍历完成后把 `first` 和 `prev`（最后一个）互相连上。

```python
def tree_to_doubly_list(root: Node | None) -> Node | None:
    if root is None:
        return None
    first = prev = None
    stack: list[Node] = []
    node = root
    while stack or node:                       # 迭代中序遍历：左 -> 根 -> 右
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if prev:
            prev.right, node.left = node, prev # 把上一个节点和当前节点互相连上
        else:
            first = node                       # 中序第一个节点就是最小值
        prev = node
        node = node.right
    first.left, prev.right = prev, first       # 首尾相连成环
    return first
```

运行：`[4,2,5,1,3]` → 沿后继 `1,2,3,4,5`，沿前驱 `1,5,4,3,2`；`[2,1,3]` → `1,2,3` 与 `1,3,2`；单节点 → 自己的 `left`、`right` 都是自己；空树 → `None`；`2000` 个节点的右斜链 → 最小节点的前驱是值 `1999` 的节点。

**复杂度。** 时间 `O(n)`：每个节点入栈、出栈一次；空间 `O(h)`：栈深度等于树高，退化成链时为 `O(n)`。

**写法要点。** `while stack or node` 是迭代中序的标准循环条件；`prev.right, node.left = node, prev` 用元组同时赋值，一行连好双向链接；`first = prev = None` 让两个变量同时从「空」开始；改写 `node.left` 安全，因为左子树已经处理完；最后一行同样用元组赋值闭合环。
