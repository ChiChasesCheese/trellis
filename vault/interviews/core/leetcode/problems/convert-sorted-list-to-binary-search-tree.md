---
slug: convert-sorted-list-to-binary-search-tree
---
## Q
**LC 109 有序链表转换二叉搜索树**｜Medium

把升序单链表转成高度平衡的二叉搜索树。

## A
**一句话。** 中序模拟：先数出长度，按下标区间 `[lo, hi)` 递归，左子树建完时链表指针正好走到中点，拿它建根。

```python
def sorted_list_to_bst(head):
    n, p = 0, head
    while p:
        n, p = n + 1, p.next
    cur = head

    def build(lo, hi):          # 建 [lo, hi)，按中序消费链表
        nonlocal cur
        if lo == hi:
            return None
        mid = (lo + hi) // 2
        left = build(lo, mid)
        root = TreeNode(cur.val)   # 左边建完，cur 到了中点
        cur = cur.next
        root.left = left
        root.right = build(mid + 1, hi)
        return root

    return build(0, n)
```

**复杂度。** 时间 `O(n)`，空间 `O(log n)`。

**易错点。**
- 先建根再建左子树：此时 `cur` 还在区间开头，根的值会错。
- 每层用快慢指针找中点：每层 `O(n)`，总 `O(n log n)`；能接受但不是最优。

**追问。**
- 简单写法？：先把链表转成数组，再按 LC 108 取中点递归，`O(n)` 时间但多 `O(n)` 空间。
- 为什么平衡？：每次对半分，左右子树大小差不超过 1。

**同模式。** LC 108 将有序数组转换为二叉搜索树、LC 1382 将二叉搜索树变平衡、LC 876 链表的中间结点
