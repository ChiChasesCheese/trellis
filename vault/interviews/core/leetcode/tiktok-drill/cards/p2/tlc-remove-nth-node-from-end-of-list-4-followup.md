---
id: tlc-remove-nth-node-from-end-of-list-4-followup
node: p2.remove-nth-node-from-end-of-list
type: qa
step: 4
---
## Q
**LC 19 删除链表的倒数第 N 个节点**｜追问

面试官接着问：（1）`n` 可能大于链表长度时怎么处理？（2）能不能不用双指针，用递归？（3）要求返回被删除的结点值，或者“倒数第 `n` 个”改成“倒数第 `k` 个节点”只读不删？

## A
1. **`n` 超过长度。** 先走的 `n` 步里，`fast` 一旦变成 `None` 就说明 `n > sz`，直接返回原链表：
```python
def remove_nth_safe(head: ListNode | None, n: int) -> ListNode | None:
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next
        if fast is None:                    # 链表不够长：不删除
            return head
    while fast.next:
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next
    return dummy.next
```
2. **递归。** 递归到尾部，回溯时每层把计数加一；计数等于 `n` 的那一层说明当前结点就是倒数第 `n` 个，让上一层把 `next` 指向它的下一个。时间 `O(sz)`，但递归栈 `O(sz)`，不如双指针。
3. **读取而非删除。** 倒数第 `k` 个节点（剑指 Offer 22）：同样先走 `k` 步，再同速走到 `fast` 为 `None`，`slow` 就是答案，不需要哑结点和前驱。返回被删值：删除前先取 `target = slow.next`，返回 `target.val`。

**Python 提醒**：`fast.next` 在 `fast` 为 `None` 时会抛 `AttributeError`，Python 没有 `?.` 链式安全访问；循环里先判断 `fast is None` 再访问，别依赖异常处理来控制流程。
