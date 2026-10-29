---
id: tlc-palindrome-linked-list-2-code
node: b.palindrome-linked-list
type: qa
step: 2
---
## Q
**LC 234 回文链表**｜写出 Python 实现

单链表节点数在 `[1, 10^5]`，值在 `[0, 9]`。判断是否回文，要求 `O(n)` 时间、`O(1)` 额外空间，并且函数返回后链表保持原样。

## A
**思路。** 快慢指针找到后半段起点 `slow`；原地反转后半段得到 `tail`；`left` 从 `head` 出发、`right` 从 `tail` 出发，一起前进比较，以后半段走完为止；最后把后半段再反转回去。

```python
def is_palindrome(head: ListNode | None) -> bool:
    def reverse(node: ListNode | None) -> ListNode | None:
        prev = None
        while node:
            nxt = node.next
            node.next = prev
            prev, node = node, nxt
        return prev

    slow = fast = head
    while fast and fast.next:          # 快指针走两步，慢指针走一步
        slow, fast = slow.next, fast.next.next
    tail = reverse(slow)               # slow 是后半段的起点：偶数长度时是第 n/2+1 个，奇数长度时是正中间
    left, right = head, tail
    result = True
    while right:                       # 后半段不长于前半段，以它为准
        if left.val != right.val:
            result = False
            break
        left, right = left.next, right.next
    reverse(tail)                      # 还原链表，不改动调用方的数据
    return result
```

运行：`[1,2,2,1]` → `True`，`[1,2]` → `False`，`[1]` → `True`，`[1,2,3,2,1]` → `True`，`[1,2,3,1]` → `False`；每次调用之后链表仍是原来的值；`10^5` 个节点的回文 → `True`。

**复杂度。** 时间 `O(n)`；空间 `O(1)`，只有几个指针。

**写法要点。** `slow = fast = head` 链式赋值指向同一个对象，之后分别移动没有问题；`slow, fast = slow.next, fast.next.next` 用元组赋值同时前进，避免先改一个影响另一个；`reverse` 里 `prev, node = node, nxt` 把「搬指针」写成一行，`nxt` 要先保存；`reverse(tail)` 返回新头，调用两次互为逆操作；用 `result` 变量代替提前 `return`，保证还原那一步一定执行。
