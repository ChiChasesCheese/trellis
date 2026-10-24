---
id: tlc-codetop-supp-1-4-followup
node: b.codetop-supp-1
type: qa
step: 4
---
## Q
**补充题 1 排序奇升偶降链表**｜追问

面试官接着问：（1）如果链表不满足奇升偶降，只是任意链表，怎么在 `O(1)` 额外空间（不算递归栈）里排序？（2）如果要求稳定（相同的值保持原来的相对顺序）？（3）链表非常长，一遍扫描能不能都完成？

## A
1. **一般链表排序**：链表归并排序（merge sort）。快慢指针找中点，断开，递归排序两半，用同样的合并函数合并。时间 `O(n log n)`，递归栈 `O(log n)`；自底向上迭代版可以做到真正的 `O(1)` 空间：

```python
def merge(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    tail = dummy = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


def sort_list(head: ListNode | None) -> ListNode | None:
    if not head or not head.next:
        return head
    slow, fast = head, head.next               # 快慢指针找中点，slow 停在前半段末尾
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    mid, slow.next = slow.next, None           # 断成两半
    return merge(sort_list(head), sort_list(mid))
```

2. **稳定性**：合并时用 `a.val <= b.val`，相等取前一条链表的结点，保持相对顺序。奇升偶降这个题里，相等值来自奇链还是偶链，本来就没有「谁先谁后」的语义，不涉及稳定性问题。
3. **一遍扫描**：拆分与反转合成一趟；合并是第二趟。合并必须等偶链整条反转完才能开始（偶链的最小值是原链表里最后一个偶数位结点），所以两趟合计 `O(n)`，不必强求并成一趟。

**Python 提醒**：`mid, slow.next = slow.next, None` 右边先整体求值，`mid` 拿到旧的 `slow.next`，再把 `slow.next` 置空，断在正确的位置；元组赋值的左边从左到右依次赋值，所以 `slow, slow.next = slow.next, None` 会先把 `slow` 换成后一个结点，再给后一个结点的 `next` 置空，断错了地方。
