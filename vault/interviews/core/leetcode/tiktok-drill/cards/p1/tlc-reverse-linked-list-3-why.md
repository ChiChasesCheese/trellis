---
id: tlc-reverse-linked-list-3-why
node: p1.reverse-linked-list
type: qa
step: 3
---
## Q
**LC 206 反转链表**｜正确性

迭代反转里，为什么要先保存 `nxt = cur.next`，再改 `cur.next = prev`？循环的不变量是什么？给出一个顺序写错的输入和结果。

## A
**不变量。** 每轮开始时，`prev` 指向的链表是原链表前缀 `[head, ..., cur 之前一个]` 反转后的结果，`cur` 指向原链表剩下的部分，两段互不相交，合起来用到了全部节点。每轮把 `cur` 从剩余部分摘下、挂到 `prev` 的前面，不变量保持；`cur` 变空时，`prev` 就是整个反转后的链表。

**为什么要先存 `nxt`。** `cur.next = prev` 会覆盖原来的 `cur.next`，原来指向的剩余链表从此无法通过 `cur` 到达。必须先把它保存起来。

**反例：顺序写错。**
```python
def reverse_list_wrong(head: ListNode | None) -> ListNode | None:
    prev: ListNode | None = None
    cur = head
    while cur:
        cur.next = prev                # 先改了指针
        prev, cur = cur, cur.next      # 此时 cur.next 已经是 prev，后继丢了
    return prev
```
- `[1,2,3]`：第一轮 `1.next = None`，然后 `prev = 1`，`cur = cur.next`——此时 `cur.next` 已是 `None`（刚刚被改成了 `prev`），所以 `cur = None`，循环结束。
- 返回 `prev`，得到只有一个节点的 `[1]`；节点 `2`、`3` 被丢失。
- 正确答案是 `[3, 2, 1]`。

另一个等价的隐患是 `prev` 的初值：必须是 `None`。若初值写成 `head` 之类，原头节点的 `next` 会指向自己或别的节点，形成环。
