---
id: tlc-patterns-linked-list-5-more-variants
node: patterns.linked-list
type: qa
step: 5
---
## Q
**链表技巧（Linked List）｜其他变形：重排、两数相加、归并排序、相交、前缀和删节点**

这些题各自的核心一步是什么？

## A
**LC 143 重排链表**：找中点 → 反转后半 → 交替合并。

```python
def reorder_list(head: ListNode | None) -> None:
    if not head or not head.next:
        return
    slow, fast = head, head
    while fast.next and fast.next.next:    # 偶数个时 slow 停在前半的最后一个
        slow, fast = slow.next, fast.next.next
    prev, cur = None, slow.next
    slow.next = None                       # 断开前半
    while cur:                             # 原地反转后半
        cur.next, prev, cur = prev, cur, cur.next
    second, first = prev, head
    while second:
        first.next, first = second, first.next
        second.next, second = first, second.next
```

`[1,2,3,4]` → `[1,4,2,3]`；`[1,2,3,4,5]` → `[1,5,2,4,3]`。

**LC 2 两数相加**：逐位相加，`carry, digit = divmod(carry, 10)`；循环条件包含 `carry`，这样最后的进位也会生成节点：`[9,9,9,9,9,9,9] + [9,9,9,9]` → `[8,9,9,9,0,0,0,1]`。

**LC 148 排序链表**：归并排序，快指针从 `head.next` 出发，保证偶数个时 `slow` 停在前半末尾；先断开再递归，最后 `merge_two`。时间 `O(n log n)`，递归深度 `O(log n)`，不会爆栈。

**LC 160 相交链表**：`p`、`q` 各走完自己的链再换到对方的头，走过的总长相同，要么同时到交点，要么同时为 `None`；用 `is` 比较节点。

**LC 1171 删除和为 0 的连续节点**：前缀和 + 字典，同一个前缀和出现两次，中间整段和为 0：

```python
def remove_zero_sum_sublists(head: ListNode | None) -> ListNode | None:
    dummy = ListNode(0, head)
    seen: dict[int, ListNode] = {}         # 前缀和 -> 最后一个拥有该前缀和的节点
    pre = 0
    node: ListNode | None = dummy
    while node:
        pre += node.val
        seen[pre] = node                   # 同一前缀和覆盖，保留最后一次
        node = node.next
    pre = 0
    node = dummy
    while node:
        pre += node.val
        node.next = seen[pre].next         # 跳过两次相同前缀和之间的整段
        node = node.next
    return dummy.next
```

`[1,2,-3,3,1]` → `[3,1]`；`[1,2,3,-3,4]` → `[1,2,4]`；`[1,2,3,-3,-2]` → `[1]`。
