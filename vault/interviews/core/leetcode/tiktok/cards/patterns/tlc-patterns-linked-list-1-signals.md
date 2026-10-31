---
id: tlc-patterns-linked-list-1-signals
node: patterns.linked-list
type: qa
step: 1
---
## Q
**链表技巧（Linked List）｜信号**

什么样的题面该想到哑节点、快慢指针、原地反转？链表题和数组题在思路上最大的区别是什么？

## A
链表题考的是**指针操作的严谨**：每一步都要想清楚「改谁的 `next`、先改哪个」。

**信号与对应技巧：**
- 可能要**删除头节点**或在头部插入、结果的头不确定（合并、删除、分段）→ **哑节点（dummy node）**：`dummy = ListNode(0, head)`，最后返回 `dummy.next`，统一处理头节点（例：LC 82 删除排序链表中的重复元素 II）。
- 「**中间节点**」「**倒数第 k 个**」「**是否有环**」「**环的入口**」→ **快慢指针**（LC 142）（例：LC 142 环形链表 II）。
- 「**反转**整个链表 / 一段 / 每 k 个一组」→ 原地反转（LC 206、92、25）（例：LC 206 反转链表）。
- 「**两个链表相交**」→ 双指针各走完自己再走对方（LC 160）（例：LC 160 相交链表）。
- 「**合并**有序链表」「**排序**链表」→ 归并（LC 23、148）（例：LC 21 合并两个有序链表）。
- 「**重排** `L0, Ln, L1, Ln-1...`」→ 找中点 + 反转后半 + 交替合并（LC 143）（例：LC 143 重排链表）。
- 「删除**连续**和为 0 的节点」→ 前缀和 + 哈希（LC 1171）（例：LC 1171 从链表中删去总和值为零的连续节点）。
- 「逆序存储的大数相加」→ 逐位加法带进位（LC 2）（例：LC 2 两数相加）。

**要求 `O(1)` 空间** → 只允许改指针，不能把节点值倒进数组再重建（这是面试官最常追加的限制）（例：LC 234 回文链表）。

**近似信号：**
- 需要随机访问第 `i` 个元素 → 先转数组（若允许）（例：LC 445 两数相加 II）。
- 需要在链表里 `O(1)` 删除任意节点并快速定位 → 哈希 + 双向链表（LRU，见设计题）（例：LC 146 LRU 缓存）。

**例题：** LC 82 删除排序链表中的重复元素 II

已排序链表（节点数 `0..300`，`-100 <= val <= 100`），删除所有出现重复的数字对应的全部节点，只保留只出现一次的数字。

```python
def delete_duplicates(head: ListNode | None) -> ListNode | None:
    dummy = ListNode(0, head)          # 头结点也可能被删，所以需要哑结点
    prev, cur = dummy, head            # prev：最后一个确认保留的结点
    while cur:
        if cur.next and cur.next.val == cur.val:
            dup = cur.val
            while cur and cur.val == dup:   # 整段重复值一个不留
                cur = cur.next
            prev.next = cur            # 接到段后面；prev 不前进，cur 可能又是新一段的开头
        else:
            prev, cur = cur, cur.next  # cur 是唯一值：确认保留
    return dummy.next
```

**例题：** LC 142 环形链表 II

给定链表头 `head`（节点数 `0..10^4`），返回开始入环的第一个节点，无环返回 `null`；不能修改链表，进阶要求 `O(1)` 空间。

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

**例题：** LC 206 反转链表

反转单链表（节点数 `0..5000`），返回反转后的头节点。

```python
def reverse_list(head: ListNode | None) -> ListNode | None:
    prev: ListNode | None = None
    cur = head
    while cur:
        nxt = cur.next            # 先存下后继，否则改完指针就丢了
        cur.next = prev           # 翻转这一条边
        prev, cur = cur, nxt      # 两个指针一起前进
    return prev
```

**例题：** LC 160 相交链表

给定两个无环单链表的头节点 `headA`、`headB`，返回它们相交的起始节点，不相交返回 `null`；链表结构必须保持不变。

```python
def get_intersection_node(head_a: ListNode | None, head_b: ListNode | None) -> ListNode | None:
    a, b = head_a, head_b
    while a is not b:                   # 比的是节点本身（地址），不是值
        a = a.next if a else head_b     # 走到头就换到另一条链表的表头
        b = b.next if b else head_a
    return a                            # 相交节点；不相交时 a、b 同时为 None
```

**例题：** LC 21 合并两个有序链表

把两个升序链表（节点数各 `0..50`，`-100 <= val <= 100`）拼接成一个新的升序链表并返回。

```python
def merge_two_lists(list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
    dummy = tail = ListNode()           # 哑节点：省掉"第一个节点怎么接"的特判
    while list1 and list2:
        if list1.val <= list2.val:      # 相等时取 list1，保持稳定
            tail.next, list1 = list1, list1.next
        else:
            tail.next, list2 = list2, list2.next
        tail = tail.next
    tail.next = list1 or list2          # 至多一条还有剩，整段直接挂上
    return dummy.next
```

**例题：** LC 143 重排链表

单链表 `L0 → L1 → … → Ln`（节点数 `1..5 * 10^4`），原地重排成 `L0 → Ln → L1 → Ln-1 → …`，必须真正移动节点，不能只改值。

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

**例题：** LC 1171 从链表中删去总和值为零的连续节点

链表有 `1..1000` 个节点（`-1000 <= val <= 1000`），反复删去和为 0 的连续节点序列，返回最终链表的头，答案不唯一时返回任意一个。

```python
def remove_zero_sum_sublists(head: ListNode | None) -> ListNode | None:
    dummy = ListNode(0, head)                    # 哨兵：整条链表都被删光时也有地方挂
    last: dict[int, ListNode] = {}               # 前缀和 -> 最后一个取到这个前缀和的节点
    s, node = 0, dummy
    while node:                                  # 第一遍：同一前缀和后出现的覆盖先出现的
        s += node.val
        last[s] = node
        node = node.next
    s, node = 0, dummy
    while node:                                  # 第二遍：从 node 直接跳到同前缀和的最后一个节点之后
        s += node.val
        node.next = last[s].next                 # (node, last[s]] 这一段总和为 0，整段删掉
        node = node.next
    return dummy.next
```

**例题：** LC 2 两数相加

两个非空链表（节点数 `1..100`，每个节点一位 `0..9`）按逆序存储两个非负整数，返回它们的和，同样按逆序存成链表。

```python
def add_two_numbers(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    dummy = tail = ListNode()          # 哑结点：头结点不用特判
    carry = 0
    while l1 or l2 or carry:           # 两条链都走完后，还要看有没有进位
        if l1:
            carry += l1.val
            l1 = l1.next
        if l2:
            carry += l2.val
            l2 = l2.next
        carry, digit = divmod(carry, 10)   # 商是新的进位，余数是当前位
        tail.next = ListNode(digit)
        tail = tail.next
    return dummy.next
```

**例题：** LC 234 回文链表

单链表（节点数 `1..10^5`，`0 <= val <= 9`），判断是否为回文；进阶要求 `O(n)` 时间、`O(1)` 空间。

```python
def is_palindrome(head: ListNode | None) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    prev = None
    while slow:
        slow.next, prev, slow = prev, slow, slow.next
    left, right = head, prev
    while right:
        if left.val != right.val:
            return False
        left, right = left.next, right.next
    return True
```

**例题：** LC 445 两数相加 II

两个非空链表（长度 `1..100`，每节点一位 `0..9`）按高位在前存储两个非负整数，返回它们的和（同样高位在前）；进阶：不能反转输入链表。

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

**例题：** LC 146 LRU 缓存

设计容量为 `capacity` 的 LRU 缓存（`1 <= capacity <= 3000`）：`get(key)` 命中返回值、否则 `-1`；`put(key, value)` 写入，超出容量时淘汰最久未使用的键；两个操作都要 `O(1)`。

```python
from collections import OrderedDict
class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.store: OrderedDict[int, int] = OrderedDict()  # 队首最旧，队尾最新
    def get(self, key: int) -> int:
        if key not in self.store:
            return -1
        self.store.move_to_end(key)
        return self.store[key]
    def put(self, key: int, value: int) -> None:
        self.store.pop(key, None)
        self.store[key] = value
        if len(self.store) > self.capacity:
            self.store.popitem(last=False)
```
