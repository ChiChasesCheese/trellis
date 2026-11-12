---
slug: minimum-distance-between-bst-nodes
---
## Q
**LC 783 二叉搜索树节点最小距离**｜Easy

二叉搜索树，返回任意两个不同节点值之差的最小值。

## A
**一句话。** 中序遍历是升序，最小差只会在相邻两个值之间，边走边和前一个值比。

```python
def min_diff_in_bst(root):
    best, prev = float("inf"), None   # prev：中序上一个值

    def inorder(node):
        nonlocal best, prev
        if node is None:
            return
        inorder(node.left)
        if prev is not None:
            best = min(best, node.val - prev)
        prev = node.val
        inorder(node.right)

    inorder(root)
    return best
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 只比父子：`[5,1,null,null,4]` 中 `5` 和 `4` 隔代，答案是 `1`，只比父子得 `3`。
- `prev` 初值写 `0`：`[1,null,10]` 第一个节点也会和 `0` 比，得 `1`，应为 `9`。

**追问。**
- 不用递归？：用栈模拟中序，一路压左孩子，弹出访问再转右孩子。
- 不是 BST 怎么办？：取出所有值排序后比相邻，`O(n log n)`。

**同模式。** LC 530 二叉搜索树的最小绝对差、LC 98 验证二叉搜索树、LC 230 二叉搜索树中第 K 小的元素、LC 501 二叉搜索树中的众数
