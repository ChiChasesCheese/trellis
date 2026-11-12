---
slug: palindrome-linked-list
---
## Q
**LC 234 回文链表**｜Easy

判断单链表是否为回文，要求 `O(n)` 时间、`O(1)` 空间。

## A
**一句话。** 快慢指针找中点，反转后半段，再从两端向中间逐个比较。

```python
def is_palindrome(head):
    slow = fast = head      # slow 停在前半段最后一个节点
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    prev, cur = None, slow.next   # 反转后半段
    while cur:
        cur.next, prev, cur = prev, cur, cur.next
    p, q = head, prev       # 后半段不更长，以它为界
    while q:
        if p.val != q.val:
            return False
        p, q = p.next, q.next
    return True
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 中点停错一格：用 `while fast and fast.next` 再从 `slow.next` 反转，`[1,2,3,1]` 后半段只剩 `[1]`，误判 `True`。
- 比较节点而不是值：`p == q` 对不同对象恒假，`[1,2,2,1]` 得 `False`。

**追问。**
- 不允许改链表？：把值读进数组再双指针比较，空间 `O(n)`；或比完再把后半段反转回去。
- 为什么奇数长时中间节点不用管？：它归前半段，后半段更短，循环以后半段为界。

**同模式。** LC 206 反转链表、LC 876 链表的中间结点、LC 143 重排链表、LC 125 验证回文串
