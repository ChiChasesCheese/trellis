---
slug: flatten-binary-tree-to-linked-list
---
## Q
**LC 114 二叉树展开为链表**｜Medium

把二叉树原地展开成单链表：沿 `right` 指针串联，`left` 全为 `null`，顺序同先序遍历。

## A
**一句话。** 按「右、左、根」倒着遍历，把每个节点接到上一个处理的节点前面。

```python
def flatten(root):
    prev = None
    def dfs(node):              # 右、左、根：倒着把链表接起来
        nonlocal prev
        if not node:
            return
        dfs(node.right)
        dfs(node.left)
        node.right, node.left = prev, None
        prev = node
    dfs(root)
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 正着先序边走边改：先写 `node.right = node.left` 会丢掉原右子树，`[1,2,5,3,4,null,6]` 只剩 `1,2,3,4`。
- 忘了把 `left` 置空：每个节点仍带着左子树，结果不是链表。

**追问。**
- 要 `O(1)` 额外空间？：对每个有左子树的节点，把右子树接到左子树的最右节点后，再把左子树移到右边，然后右移一步。
- 为什么倒着走？：先处理右、再处理左，轮到一个节点时，它后面的链已经建好，直接接上即可。

**同模式。** LC 116 填充每个节点的下一个右侧节点指针、LC 430 扁平化多级双向链表、LC 897 递增顺序搜索树、LC 426 BST 转双向链表
