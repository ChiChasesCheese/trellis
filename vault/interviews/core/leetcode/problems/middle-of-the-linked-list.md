---
slug: middle-of-the-linked-list
---
## Q
**LC 876 链表的中间结点**｜Easy

返回单链表的中间结点，有两个中间结点时返回第二个。

## A
**一句话。** 快慢指针，快的一次走两步，快的到末尾时慢的恰在中间。

```python
def middle_node(head):
    slow = fast = head
    while fast and fast.next:   # 偶数个 fast 先变 None
        slow = slow.next
        fast = fast.next.next
    return slow     # 偶数个时是第二个中点
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 条件写成 `while fast.next`：偶数个结点时 `fast` 先变 `None`，下一次判断抛 `AttributeError`。
- 条件写成 `fast.next and fast.next.next`：`[1,2,3,4,5,6]` 得 `[3,4,5,6]`，应为 `[4,5,6]`。

**追问。**
- 要第一个中点怎么改？：循环条件改成 `fast.next and fast.next.next`。
- 为什么偶数个返回第二个？：`fast` 走到 `None` 时 `slow` 已前进 `n/2` 步，正好落在后半段起点。

**同模式。** LC 141 环形链表、LC 142 环形链表 II、LC 234 回文链表、LC 143 重排链表
