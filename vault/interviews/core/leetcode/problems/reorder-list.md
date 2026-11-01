---
slug: reorder-list
---
## Q
**LC 143 重排链表**｜Medium

给定一个单链表 `L` 的头节点 `head`，单链表 `L` 表示为 `L0 → L1 → … → Ln-1 → Ln`。请将其重新排列后变为 `L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …`。不能只是单纯地改变节点内部的值，而是需要实际地进行节点交换。函数原地修改链表，不需要返回值。链表的长度范围为 `[1, 5 * 10^4]`，`1 <= node.val <= 1000`。

例：`head = [1,2,3,4]` → `[1,4,2,3]`；`head = [1,2,3,4,5]` → `[1,5,2,4,3]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 链表三件套组合：快慢指针找中点 + 反转后半段 + 交错合并（merge alternately）。

**一句话。** 把链表从中间切成两半，后半段反转，然后两段交替取结点串起来。

**识别。** 新顺序是「头、尾、头、尾……」，也就是前半段和反转后的后半段交替；单链表没法从尾部往前取，所以必须反转后半段。`n <= 5 * 10^4`，线性。

**推导。** 如果能随机访问就简单了：下标 `i` 与 `n-1-i` 交替。链表不行。把前半段 `L0..Lm` 看成正序序列，后半段 `Lm+1..Ln` 反转成 `Ln..Lm+1`，两个序列轮流各取一个就是答案。所以只需要三个已经会的子程序。

**简单解法。** 把所有结点放进数组，用下标双指针重连（空间 `O(n)`）：
```python
def reorder_list_array(head: ListNode | None) -> None:
    nodes: list[ListNode] = []
    while head:
        nodes.append(head)
        head = head.next
    i, j = 0, len(nodes) - 1
    while i < j:
        nodes[i].next = nodes[j]    # 头接尾
        i += 1
        if i == j:
            break
        nodes[j].next = nodes[i]    # 尾接下一个头
        j -= 1
    nodes[i].next = None            # 收尾，防止成环
```

**最优解：** 找中点、反转、交错，空间 `O(1)`。

```python
def reorder_list(head: ListNode | None) -> None:
    if not head or not head.next:
        return
    # 1. 快慢指针：slow 停在前半段最后一个结点（奇数长时中间结点归前半段）
    slow = fast = head
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    # 2. 断开两半，并反转后半段
    second, slow.next = slow.next, None     # 必须断开，否则前半段尾巴还连着后半段
    prev = None
    while second:
        second.next, prev, second = prev, second, second.next
    second = prev                           # 反转后的后半段，从原来的尾开始
    # 3. 交错合并：first 取一个，second 取一个
    first = head
    while second:
        nxt1, nxt2 = first.next, second.next
        first.next = second
        second.next = nxt1
        first, second = nxt1, nxt2
```

**运行。** `[1,2,3,4]` → `[1, 4, 2, 3]`；`[1,2,3,4,5]` → `[1, 5, 2, 4, 3]`；`[1]` → `[1]`；`[1,2]` → `[1, 2]`。

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**拓展优化。**
- 递归写法：用递归栈当「从尾部往前取」的工具，回溯到第 `i` 层时取出对应的尾部结点，空间 `O(n)`，深度会触到 CPython 约 1000 的递归上限。

**易错点。**
- 没有断开前半段：`[1,2,3,4]` 中 `2.next` 仍指向 `3`，合并最后一步又把 `3.next` 接回 `3`，形成自环，遍历永远不结束。
- 反转完直接用 `second`：循环结束时 `second` 已是 `None`，合并循环一次不进，`[1,2,3,4]` 原样输出；要用 `prev`（后半段新头）。

**同模式。** LC 234 回文链表、LC 206 反转链表、LC 21 合并两个有序链表、LC 876 链表的中间结点。
