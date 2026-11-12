---
slug: populating-next-right-pointers-in-each-node
---
## Q
**LC 116 填充每个节点的下一个右侧节点指针**｜Medium

完美二叉树的每个节点多一个 `next` 指针，令其指向同层右边紧邻的节点（最右的为 `None`），要求常量额外空间。

## A
**一句话。** 利用上一层已连好的 `next` 链在本层横着走，给下一层连线。

```python
def connect(root):
    left = root                      # 每层的最左节点
    while left and left.left:
        node = left
        while node:
            node.left.next = node.right          # 同一个父亲
            if node.next:
                node.right.next = node.next.left # 跨父亲
            node = node.next
        left = left.left
    return root
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 漏了跨父亲的连线：`[1,2,3,4,5,6,7]` 里 `5.next` 是 `None`，应为 `6`。
- 外层写成 `while left:`：到叶子层 `node.left` 为 `None`，`AttributeError`。

**追问。**
- 不是完美二叉树（LC 117）？：孩子可能缺失，边走本层边用哑节点把下一层孩子串成链。
- 空间 `O(n)` 的做法？：BFS 层序遍历，每层内相邻节点互连。

**同模式。** LC 117 填充每个节点的下一个右侧节点指针 II、LC 102 二叉树的层序遍历、LC 199 二叉树的右视图
