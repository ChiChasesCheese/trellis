---
slug: reorder-list
---
## Q
**LC 143 重排链表**｜Medium

把链表 `L0→L1→…→Ln` 原地重排成 `L0→Ln→L1→Ln-1→…`，必须改指针，不能改值。

## A
**一句话。** 快慢指针找中点切开，反转后半段，再和前半段交替穿插。

```python
def reorder_list(head):
    slow = fast = head
    while fast.next and fast.next.next:   # slow 停在前半段末尾
        slow, fast = slow.next, fast.next.next
    second, slow.next = slow.next, None   # 必须断开
    prev = None
    while second:                         # 反转后半段
        nxt = second.next
        second.next, prev, second = prev, second, nxt
    first, second = head, prev
    while second:                         # 交替穿插
        n1, n2 = first.next, second.next
        first.next, second.next = second, n1
        first, second = n1, n2
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 没断开前半段：`[1,2,3,4]` 里 `2.next` 仍指着 `3`，合并后成环，遍历不终止。
- 反转完还用 `second`：此时它已是 `None`，要用 `prev`（后半段新头）。

**追问。**
- 面试先怎么答？：先说放数组、双指针重连，`O(n)` 空间；再优化成找中点加反转加穿插。
- 奇数长度怎么收尾？：中点归前半段，`second` 先耗尽，`[1,2,3]` 得 `[1,3,2]`。

**同模式。** LC 234 回文链表、LC 206 反转链表、LC 21 合并两个有序链表、LC 876 链表的中间结点
