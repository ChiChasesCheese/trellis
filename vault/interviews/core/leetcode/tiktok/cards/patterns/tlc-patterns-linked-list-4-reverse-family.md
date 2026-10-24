---
id: tlc-patterns-linked-list-4-reverse-family
node: patterns.linked-list
type: qa
step: 4
---
## Q
**链表技巧（Linked List）｜反转的两个变形：反转一段（LC 92）和每 k 个一组（LC 25）**

怎样在不动头节点的前提下只反转第 `left` 到 `right` 个节点？K 个一组反转为什么要先确认后面还有 `k` 个节点？

## A
**LC 92：头插法。** `pre` 停在第 `left` 个节点的前一个；`cur` 是要被推到后面的节点；每一步把 `cur` 后面的那个节点插到 `pre` 的后面。

```python
def reverse_between(head: ListNode | None, left: int, right: int) -> ListNode | None:
    dummy = ListNode(0, head)
    pre = dummy
    for _ in range(left - 1):
        pre = pre.next
    cur = pre.next
    for _ in range(right - left):
        nxt = cur.next
        cur.next = nxt.next                # 把 nxt 摘下来
        nxt.next = pre.next                # 插到 pre 后面
        pre.next = nxt
    return dummy.next
```

运行：`[1,2,3,4,5], 2, 4` → `[1,4,3,2,5]`；`[5], 1, 1` → `[5]`。

**LC 25：先数够 `k` 个再反转。**

```python
def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    dummy = ListNode(0, head)
    group_prev = dummy
    while True:
        kth = group_prev
        for _ in range(k):                 # 确认后面还有 k 个节点
            kth = kth.next
            if not kth:
                return dummy.next
        group_next = kth.next
        prev, cur = group_next, group_prev.next
        while cur is not group_next:       # 反转这一组，尾部接到下一组的头
            cur.next, prev, cur = prev, cur, cur.next
        tail = group_prev.next             # 反转前的第一个节点，现在是这一组的尾
        group_prev.next = kth
        group_prev = tail
```

运行：`[1,2,3,4,5], k=2` → `[2,1,4,3,5]`；`k=3` → `[3,2,1,4,5]`；`[1], k=1` → `[1]`。

- 不先数够就反转：`[1,2,3,4,5], k=3` 会把剩下的 `4,5` 也反转，得到 `[3,2,1,5,4]`，正确是 `[3,2,1,4,5]`。
- 反转的初始 `prev` 设为 `group_next`，反转完这一组的尾自动接上下一组的头。
- 时间 `O(n)`，空间 `O(1)`。
