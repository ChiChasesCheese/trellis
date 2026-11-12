---
slug: recover-binary-search-tree
---
## Q
**LC 99 恢复二叉搜索树**｜Medium

BST 中恰好两个节点的值被交换了，不改结构，把它恢复。

## A
**一句话。** 中序遍历应严格升序，记前驱找逆序对：第一处逆序取较大者，最后一处逆序取较小者，交换两值。

```python
def recover_tree(root):
    prev = first = second = None
    def inorder(node):
        nonlocal prev, first, second
        if not node:
            return
        inorder(node.left)
        if prev and prev.val > node.val:   # 一处逆序
            if not first:
                first = prev     # 第一处：取较大者
            second = node        # 最后一处：取较小者
        prev = node
        inorder(node.right)
    inorder(root)
    first.val, second.val = second.val, first.val
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- `second` 只在第一处逆序时赋值：不相邻互换会漏掉第二处，中序 `3,2,1` 只换 `3,2`。
- 每处逆序都刷新 `first`：中序 `1,5,3,4,2,6` 会错换 `4,2`，应换 `5,2`。

**追问。**
- 进阶要 `O(1)` 空间？：Morris 中序遍历，逆序检测不变。
- 链状树深 1000 会爆栈吗？：会，要调大递归上限或改用显式栈做迭代中序。

**同模式。** LC 98 验证二叉搜索树、LC 230 BST 中第 K 小的元素、LC 530 BST 的最小绝对差、LC 501 BST 中的众数
