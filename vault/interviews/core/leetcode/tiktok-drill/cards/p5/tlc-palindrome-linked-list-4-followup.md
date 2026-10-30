---
id: tlc-palindrome-linked-list-4-followup
node: p5.palindrome-linked-list
type: qa
step: 4
---
## Q
**LC 234 回文链表**｜追问

面试官接着问：（1）如果不允许修改链表怎么办？（2）能不能用递归，代价是什么？（3）为什么要把反转的后半段还原？

## A
1. **不改链表**：把值复制进数组再双指针，或直接比较 `vals == vals[::-1]`，时间 `O(n)`、空间 `O(n)`。因为 `0 <= Node.val <= 9`，也可以把整条链表拼成一个字符串比较，本质一样。

```python
def is_palindrome_copy(head: ListNode | None) -> bool:
    vals: list[int] = []
    while head:
        vals.append(head.val)
        head = head.next
    return vals == vals[::-1]
```

`[1,2,2,1]` → `True`，`[1,2,3,1]` → `False`。
2. **递归**：递归到链表尾，回溯时拿一个从 `head` 出发的指针逐个比较，等价于「同时从两端向内走」。代码短，但栈深 `n`，`10^5` 个节点在 Python 里会 `RecursionError`，且空间 `O(n)`。
3. **还原**：反转破坏了链表，调用方或并发的读者可能还在用它；还原只多一次 `O(n)` 遍历。在面试里主动说"我会还原"是加分项。

**Python 提醒**：`vals == vals[::-1]` 先复制整个列表再逐元素比较，写起来最短；列表比较遇到第一个不等就停。`vals[::-1]` 创建新列表，空间翻倍，这是它与 `O(1)` 空间解法的差别。
