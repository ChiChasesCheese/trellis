---
id: tlc-linked-list-cycle-ii-2-code
node: a.linked-list-cycle-ii
type: qa
step: 2
---
## Q
**LC 142 环形链表 II**｜写出 Python 实现

单链表 `head`（结点数 `0..10^4`），可能在某个结点处成环。返回入环的第一个结点，无环返回 `None`。不得修改链表，额外空间 `O(1)`。

## A
**思路。** 快慢指针从表头出发，慢一步、快两步。若快指针走到末尾，无环。若两者相遇，说明有环，把慢指针放回表头，之后两个指针都每次走一步，再次相遇的结点就是入环点。

```python
def detect_cycle(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next               # 慢指针一步
        fast = fast.next.next          # 快指针两步
        if slow is fast:               # 在环内相遇：还不知道入环点
            slow = head                # 慢指针回表头，两个指针都改成每次一步
            while slow is not fast:
                slow, fast = slow.next, fast.next
            return slow                # 再次相遇的位置就是入环点
    return None                        # 快指针走到尽头：无环
```

运行：`head=[3,2,0,-4], pos=1 → 返回的结点值` → `2`，`head=[1,2], pos=0 → 返回的结点值` → `1`，`head=[1], pos=-1` → `None`，`head=[1], pos=0（自环）→ 返回的结点值` → `1`，`head=[]` → `None`，`10^4 个结点，pos=0 → 返回结点是否就是 head` → `True`。

**复杂度。** 时间 `O(n)`：第一阶段快慢指针至多走 `O(n)` 步相遇，第二阶段两个指针各走 `a` 步（`a` 为表头到入环点的距离）；空间 `O(1)`。

**写法要点。** `slow = fast = head` 链式赋值（结点是不可变引用语义，两个变量指向同一对象没问题）；`while fast and fast.next` 同时防止偶数长度和奇数长度的无环链走出尽头；比较用 `is` 而不是 `==`，比较的是结点身份而不是值；`slow, fast = slow.next, fast.next` 元组赋值同时前进；函数有两个阶段，第二阶段直接 `return slow`，不需要额外的标志变量。
