---
id: tlc-lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof-4-followup
node: a.lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof
type: qa
step: 4
---
## Q
**剑指 Offer 22 链表中倒数第k个节点**｜追问

面试官接着问：（1）删除倒数第 `n` 个节点（LC 19）怎么写？（2）找链表的中间节点？（3）链表可能有环呢？

## A
1. **删除倒数第 `n` 个。** 删除需要前驱，且可能删掉头节点，所以加哨兵，`fast` 先走 `n` 步，之后同步走到 `fast` 是最后一个节点，`slow` 就是前驱：

```python
def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    dummy = ListNode(0, head)                    # 哨兵：删的可能是头节点
    fast = slow = dummy
    for _ in range(n):                           # fast 先走 n 步
        fast = fast.next
    while fast.next:                             # fast 停在最后一个节点时，slow 恰好是被删节点的前驱
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next
    return dummy.next
```

2. **中间节点（LC 876）。** `slow` 每次一步，`fast` 每次两步，`fast` 到末尾时 `slow` 在中间；偶数个节点时落在后一个中间节点。
3. **有环。** 先用快慢指针判环（LC 141），有环时"倒数第几个"没有意义，要先和面试官确认题目保证无环。

**Python 提醒**：`ListNode(0, head)` 的第二个位置参数是 `next`；`fast, slow = fast.next, slow.next` 右边先整体求值，所以不会出现"先改 `fast` 再用它"的错误。
