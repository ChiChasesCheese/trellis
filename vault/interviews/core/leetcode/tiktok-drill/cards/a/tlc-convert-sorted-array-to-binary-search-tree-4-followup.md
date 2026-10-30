---
id: tlc-convert-sorted-array-to-binary-search-tree-4-followup
node: a.convert-sorted-array-to-binary-search-tree
type: qa
step: 4
---
## Q
**LC 108 将有序数组转换为二叉搜索树**｜追问

面试官接着问：（1）输入改成有序**链表**（LC 109）怎么做？（2）怎样验证得到的树确实平衡？（3）数组中间会有重复值怎么办？

## A
1. **有序链表**：链表不能随机访问，每次找中点要 `O(n)`，总计 `O(n log n)`。改成**中序模拟**：先数出长度 `n`，再按中序位置 `[lo, hi)` 递归，递归顺序恰好是升序，用一个外部指针 `cur` 顺着链表推进，`O(n)`：

```python
def sorted_list_to_bst(head: ListNode | None) -> TreeNode | None:
    n, node = 0, head
    while node:
        n += 1
        node = node.next
    cur = head

    def build(lo: int, hi: int) -> TreeNode | None:    # 按中序位置 [lo, hi) 建树
        nonlocal cur
        if lo >= hi:
            return None
        mid = (lo + hi) // 2
        left = build(lo, mid)
        root = TreeNode(cur.val)                       # 此时 cur 恰好是第 mid 个结点
        cur = cur.next
        root.left = left
        root.right = build(mid + 1, hi)
        return root

    return build(0, n)
```
   运行：`[-10,-3,0,5,9]` 的链表 → 层序 `[0,-3,9,-10,None,5]`，与数组版相同。
2. **验证平衡**：后序递归，每个结点返回高度；左右高度差大于 `1` 就标记失败。这也是 LC 110 的标准解。
3. **有重复值**：BST 对重复值的放置需要先约定（都放左或都放右），中点法仍可用，但「左边都小于、右边都大于」要改成「左边 `<=`」或「右边 `>=`」，并保证重复值不被拆到两侧。

**Python 提醒**：嵌套函数里要给外层变量重新赋值（如 `cur = cur.next`）必须写 `nonlocal`；只读取或修改其内容（如 `ans.append`）则不需要。
