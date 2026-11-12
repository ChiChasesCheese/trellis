---
slug: populating-next-right-pointers-in-each-node-ii
---
## Q
**LC 117 填充每个节点的下一个右侧节点指针 II**｜Medium

给任意二叉树，让每个节点的 `next` 指向同层右侧相邻节点，没有则为 `NULL`。

## A
**一句话。** 逐层处理：同层相邻节点连 `next`，再展开出下一层。

```python
def connect(root):
    level = [root] if root else []
    while level:
        for a, b in pairwise(level):
            a.next = b                 # 最右节点的 next 保持 None
        level = [c for node in level
                 for c in (node.left, node.right) if c]
    return root
```

**复杂度。** 时间 `O(n)`，空间 `O(w)`。

**易错点。**
- 套用完美二叉树的 `node.right.next = node.next.left`：`3` 没有左孩子，`5.next` 会变 `None` 而不是 `7`。
- 把 `None` 孩子放进下一层：`pairwise` 会给 `None` 设 `next`，抛 `AttributeError`。

**追问。**
- 要 `O(1)` 额外空间？：用已连好的 `next` 当队列，一个哨兵头串起下一层，逐层向右走。
- 完美二叉树（LC 116）有何不同？：左右孩子位置固定，`node.right.next = node.next.left` 即可。

**同模式。** LC 116 填充每个节点的下一个右侧节点指针、LC 102 二叉树的层序遍历、LC 199 二叉树的右视图、LC 637 二叉树的层平均值
