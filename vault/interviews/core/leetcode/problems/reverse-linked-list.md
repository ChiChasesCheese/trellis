---
slug: reverse-linked-list
---
## Q
**LC 206 反转链表**｜Easy

反转单链表，返回新的头节点。

## A
**一句话。** 迭代三指针：先存后继，再把 `cur.next` 指向 `prev`，两个指针一起前进。

```python
def reverse_list(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next       # 先存后继，否则改完就丢了
        cur.next = prev
        prev, cur = cur, nxt
    return prev
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 没先存后继：先写 `cur.next = prev` 再 `cur = cur.next`，`[1,2,3]` 只剩 `[1]`。
- 返回 `cur`：循环结束时它是 `None`，应返回 `prev`。
- 链式赋值顺序写错：`cur, cur.next = ...` 先改了 `cur` 再写 `cur.next`，抛 `AttributeError`。

**追问。**
- 只反转第 `m` 到 `n` 个节点（LC 92）？：用哑节点，反转这一段后接回两端。
- 递归怎么写？：递归反转 `head.next` 之后的部分，再让 `head.next.next = head`、`head.next = None`。

**同模式。** LC 92 反转链表 II、LC 25 K 个一组翻转链表、LC 234 回文链表、LC 24 两两交换链表中的节点
