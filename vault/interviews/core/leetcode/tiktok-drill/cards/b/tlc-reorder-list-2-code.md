---
id: tlc-reorder-list-2-code
node: b.reorder-list
type: qa
step: 2
---
## Q
**LC 143 重排链表**｜写出 Python 实现

单链表 `head`（长度 `[1, 5 * 10^4]`），原地重排成 `L0 → Ln → L1 → Ln-1 → L2 → …`，只能改指针，不能改节点值，不返回。

## A
**思路。** 先用快慢指针找中点，在中点处把链表断成两半。把后半段翻转。再用两个指针交替取前半段和后半段的节点，拼成最终顺序。前半段不短于后半段，拼接循环以后半段走完为止，前半段多出的最后一个节点自然留在末尾。

```python
def reorder_list(head: ListNode | None) -> None:
    if not head or not head.next:
        return
    slow = fast = head                          # 1. 快慢指针找中点
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    second, slow.next = slow.next, None         # 在中点处断开：前半段不短于后半段

    prev: ListNode | None = None                # 2. 翻转后半段
    while second:
        nxt = second.next
        second.next = prev
        prev, second = second, nxt
    second = prev

    first = head                                # 3. 两段交替拼接
    while second:
        nxt1, nxt2 = first.next, second.next
        first.next = second
        second.next = nxt1
        first, second = nxt1, nxt2
```

运行：`[1,2,3,4]` → `[1, 4, 2, 3]`，`[1,2,3,4,5]` → `[1, 5, 2, 4, 3]`，`[1]` → `[1]`，`[1,2]` → `[1, 2]`，`[1,2,3]` → `[1, 3, 2]`，`5 * 10^4` 个节点的链表也能正确处理。

**复杂度。** 时间 `O(n)`：三个阶段各扫一遍；空间 `O(1)`。

**写法要点。** `second, slow.next = slow.next, None` 是一条元组赋值：右边两个值先求出（旧的 `slow.next` 和 `None`），再依次赋给左边，所以同时完成「取出后半段的头」和「断开」；`slow = fast = head` 链式赋值对对象引用是安全的，两个名字指向同一个节点；翻转循环里 `prev, second = second, nxt` 一次移动两个指针；三个阶段写在同一个函数里，用注释分段，比拆成三个函数少传参数；函数返回 `None`，只修改链表。
