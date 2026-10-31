---
id: tlc-patterns-linked-list-5-more-variants
node: patterns.linked-list
type: qa
step: 5
---
## Q
**链表技巧（Linked List）｜其他变形：重排、两数相加、归并排序、相交、前缀和删节点**

这些题各自的核心一步是什么？

## A
- **重排**：找中点 → 反转后半 → 交替合并。偶数个时 `slow` 停在前半的最后一个，先断开再反转（例：LC 143 重排链表）。
- **逐位相加**：`carry, digit = divmod(carry, 10)`；循环条件包含 `carry`，这样最后的进位也会生成节点：`[9,9,9,9,9,9,9] + [9,9,9,9]` → `[8,9,9,9,0,0,0,1]`（例：LC 2 两数相加；高频：LC 445 两数相加 II）。
- **归并排序**：快指针从 `head.next` 出发，保证偶数个时 `slow` 停在前半末尾；先断开再递归，最后合并两个有序链表。时间 `O(n log n)`，递归深度 `O(log n)`，不会爆栈（例：LC 148 排序链表）。
- **相交**：`p`、`q` 各走完自己的链再换到对方的头，走过的总长相同，要么同时到交点，要么同时为 `None`；用 `is` 比较节点（例：LC 160 相交链表）。
- **前缀和删节点**：前缀和 + 字典，同一个前缀和出现两次，中间整段和为 0；字典同一前缀和覆盖，保留最后一次，第二遍遍历时跳过两次相同前缀和之间的整段。`[1,2,-3,3,1]` → `[3,1]`；`[1,2,3,-3,4]` → `[1,2,4]`；`[1,2,3,-3,-2]` → `[1]`（例：LC 1171 从链表中删去总和值为零的连续节点）。

**例题：** LC 143 重排链表

把 `L0 → L1 → … → Ln` 原地重排为 `L0 → Ln → L1 → Ln-1 → …`，不能只改节点的值，长度 `[1, 5 * 10^4]`。

```python
def reorder_list(head: ListNode | None) -> None:
    if not head or not head.next:
        return
    slow = fast = head
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    second, slow.next = slow.next, None
    prev: ListNode | None = None
    while second:
        nxt = second.next
        second.next = prev
        prev, second = second, nxt
    second = prev
    first = head
    while second:
        nxt1, nxt2 = first.next, second.next
        first.next = second
        second.next = nxt1
        first, second = nxt1, nxt2
```

**例题：** LC 2 两数相加

两个非空链表按**逆序**存储非负整数的各位数字，返回它们的和（同样的链表形式），每个链表节点数 `[1, 100]`，每个节点值 `0..9`。

```python
def add_two_numbers(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    dummy = tail = ListNode()
    carry = 0
    while l1 or l2 or carry:
        if l1:
            carry += l1.val
            l1 = l1.next
        if l2:
            carry += l2.val
            l2 = l2.next
        carry, digit = divmod(carry, 10)
        tail.next = ListNode(digit)
        tail = tail.next
    return dummy.next
```

**例题：** LC 148 排序链表

把链表按升序排序，节点数 `[0, 5 * 10^4]`；进阶要求 `O(n log n)` 时间。

```python
def sort_list(head: ListNode | None) -> ListNode | None:
    def merge(a: ListNode | None, b: ListNode | None) -> ListNode | None:
        dummy = tail = ListNode()
        while a and b:
            if a.val <= b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a or b
        return dummy.next
    if not head or not head.next:
        return head
    slow, fast = head, head.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    mid, slow.next = slow.next, None
    return merge(sort_list(head), sort_list(mid))
```

**例题：** LC 160 相交链表

返回两个单链表相交的起始节点，不相交返回 `None`，两个链表都无环，长度 `<= 3 * 10^4`；进阶要求 `O(m + n)` 时间、`O(1)` 空间。

```python
def get_intersection_node(head_a: ListNode | None, head_b: ListNode | None) -> ListNode | None:
    a, b = head_a, head_b
    while a is not b:
        a = a.next if a else head_b
        b = b.next if b else head_a
    return a
```

**例题：** LC 1171 从链表中删去总和值为零的连续节点

反复删去链表中总和为 0 的连续节点序列，直到不存在，返回最终链表的头，节点数 `1..1000`，值 `-1000..1000`。

```python
def remove_zero_sum_sublists(head: ListNode | None) -> ListNode | None:
    dummy = ListNode(0, head)
    last: dict[int, ListNode] = {}
    s, node = 0, dummy
    while node:
        s += node.val
        last[s] = node
        node = node.next
    s, node = 0, dummy
    while node:
        s += node.val
        node.next = last[s].next
        node = node.next
    return dummy.next
```

**例题：** LC 445 两数相加 II

给两个**非空**链表，各表示一个非负整数，数字**高位在前**（最高位在链表头），每个结点存一位数字（`0 <= node.val <= 9`，链表长度 `1` 到 `100`）。把两数相加，以同样形式返回和的链表。除了数字 `0` 本身，两个数都没有前导零。进阶：不能翻转输入链表。

```python
def add_two_numbers(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    s1: list[int] = []
    s2: list[int] = []
    while l1:                              # 压栈：栈顶就是个位
        s1.append(l1.val)
        l1 = l1.next
    while l2:
        s2.append(l2.val)
        l2 = l2.next
    head: ListNode | None = None
    carry = 0
    while s1 or s2 or carry:               # 最后一个进位也要处理
        carry += (s1.pop() if s1 else 0) + (s2.pop() if s2 else 0)
        carry, digit = divmod(carry, 10)
        head = ListNode(digit, head)       # 头插法：新结点接在已有结果前面
    return head
```
