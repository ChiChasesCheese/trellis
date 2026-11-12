---
slug: minimum-absolute-difference-in-bst
---
## Q
**LC 530 二叉搜索树的最小绝对差**｜Easy

二叉搜索树中，任意两个不同节点值之差的最小绝对值。

## A
**一句话。** 中序遍历是升序，最小差只在相邻值之间，记住上一个值边走边比。

```python
def get_minimum_difference(root):
    best, prev = float("inf"), None   # prev：中序上一个值

    def inorder(node):
        nonlocal best, prev
        if not node:
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
- 只比父子：`[10,4,null,null,9]` 中 `10` 与 `9` 差 `1`，只比父子得 `5`。
- `prev` 初值写 `0`：`[1,null,100000]` 多算一对 `1-0`，得 `1`，应为 `99999`。

**追问。**
- 想省递归栈？：Morris 中序，借空右指针临时连回后继，`O(1)` 空间。
- 不是 BST 呢？：取出全部值排序比相邻，`O(n log n)`。

**同模式。** LC 783 二叉搜索树节点最小距离、LC 98 验证二叉搜索树、LC 230 二叉搜索树中第 K 小的元素、LC 501 二叉搜索树中的众数
