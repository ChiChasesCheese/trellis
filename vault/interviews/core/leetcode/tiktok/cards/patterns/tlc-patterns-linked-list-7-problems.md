---
id: tlc-patterns-linked-list-7-problems
node: patterns.linked-list
type: qa
step: 7
---
## Q
**链表技巧（Linked List）｜本组用到链表技巧的题**

按变形分类，这个题组里哪些题属于链表技巧？

## A
**反转**
- LC 206 反转链表
- LC 92 反转链表 II
- LC 25 K 个一组翻转链表

**快慢指针 / 双指针**
- LC 142 环形链表 II
- LC 160 相交链表
- LC 143 重排链表（中点 + 反转 + 交替合并）

**合并 / 排序**
- LC 23 合并 K 个升序链表（堆）
- LC 148 排序链表（归并）

**逐位运算 / 前缀和**
- LC 2 两数相加
- LC 1171 从链表中删去总和值为零的连续节点

**链表 + 哈希 / 设计**
- LC 146 LRU 缓存（哈希 + 双向链表）
- LC 432 全 O(1) 的数据结构（哈希 + 双向链表）
- LC 426 将二叉搜索树转化为排序的双向链表（中序遍历中接指针）

提示：先问有没有可能删头或换头（哑节点）、是否要 `O(1)` 空间（只改指针）、是否涉及中点 / 环（快慢指针）。

**例题：** LC 206 反转链表

反转单链表并返回新的头节点。结点数 `0..5000`。

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

**例题：** LC 92 反转链表 II

反转单链表中从第 `left` 个到第 `right` 个节点（从 `1` 数起），返回头节点。`1 <= n <= 500`，`1 <= left <= right <= n`，最好一趟扫描。

```python
def reverse_between(head: ListNode | None, left: int, right: int) -> ListNode | None:
    dummy = ListNode(0, head)           # 哑节点：left = 1 时也有"前一个节点"
    pre = dummy
    for _ in range(left - 1):           # pre 停在第 left - 1 个节点
        pre = pre.next
    cur = pre.next                      # cur 始终是区间里原来的第一个节点，会被一步步挤到后面
    for _ in range(right - left):       # 头插法：把 cur 后面的节点依次插到 pre 后面
        nxt = cur.next
        cur.next = nxt.next
        nxt.next = pre.next
        pre.next = nxt
    return dummy.next
```

**例题：** LC 25 K 个一组翻转链表

每 `k` 个节点一组翻转链表，不足 `k` 个的尾部保持原样，必须真正交换节点。`1 <= k <= n <= 5000`。

```python
def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    dummy = ListNode(0, head)
    group_prev = dummy                       # 本组前一个节点（上一组翻转后的尾）
    while True:
        kth: ListNode | None = group_prev
        for _ in range(k):                   # 往后数 k 个；不够 k 个就结束，余下原样保留
            kth = kth.next
            if kth is None:
                return dummy.next
        group_next = kth.next                # 下一组的头
        prev, cur = group_next, group_prev.next      # prev 先指向下一组：翻完后本组尾巴自动接上
        while cur is not group_next:
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        tail = group_prev.next               # 翻转前的头，现在是本组的尾
        group_prev.next = kth                # 前一段接上新的头（kth）
        group_prev = tail
```

**例题：** LC 142 环形链表 II

返回链表入环的第一个节点，无环返回 `null`；不能修改链表，最好 `O(1)` 空间。结点数 `0..10^4`。

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

**例题：** LC 160 相交链表

两个单链表的头节点，返回相交的起始节点（同一个节点对象），不相交返回 `null`；`O(m + n)` 时间、`O(1)` 额外空间，不能破坏原结构。`m, n <= 3 * 10^4`。

```python
def get_intersection_node(head_a: ListNode | None, head_b: ListNode | None) -> ListNode | None:
    a, b = head_a, head_b
    while a is not b:                   # 比的是节点本身（地址），不是值
        a = a.next if a else head_b     # 走到头就换到另一条链表的表头
        b = b.next if b else head_a
    return a                            # 相交节点；不相交时 a、b 同时为 None
```

**例题：** LC 143 重排链表

把 `L0 → L1 → … → Ln` 原地重排成 `L0 → Ln → L1 → Ln-1 → …`，必须改指针而不是改值。结点数 `1..5 * 10^4`。

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

**例题：** LC 23 合并 K 个升序链表

`k` 个升序链表合并成一个升序链表。`0 <= k <= 10^4`，链表总长度不超过 `10^4`。

```python
import heapq
def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    # 堆里放 (值, 链表编号, 节点)：值相同时比编号，永远不会去比较 ListNode
    heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
    heapq.heapify(heap)
    dummy = tail = ListNode()
    while heap:
        _, i, node = heap[0]            # 堆顶就是当前最小的队头
        tail.next = node
        tail = node
        if node.next:                   # 该链表还有后继：原地替换堆顶，只做一次下沉
            heapq.heapreplace(heap, (node.next.val, i, node.next))
        else:
            heapq.heappop(heap)
    return dummy.next
```

**例题：** LC 148 排序链表

把链表按升序排序，要求 `O(n log n)` 时间。结点数 `0..5 * 10^4`，`-10^5 <= val <= 10^5`。

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
    slow, fast = head, head.next        # fast 先走一步：偶数长度时 slow 停在前半段末尾
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    mid, slow.next = slow.next, None    # 断开成两半
    return merge(sort_list(head), sort_list(mid))
```

**例题：** LC 2 两数相加

两个非空链表，各按逆序存一个非负整数（每个结点一位），返回它们的和，同样按逆序存成链表。每个链表结点数 `1..100`，`0 <= val <= 9`，无前导零。

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

**例题：** LC 1171 从链表中删去总和值为零的连续节点

反复删去链表中和为 `0` 的连续节点序列，直到没有为止，返回头节点（答案不唯一，任一满足即可）。结点数 `1..1000`，`-1000 <= val <= 1000`。

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

**例题：** LC 146 LRU 缓存

设计 `LRUCache(capacity)`：`get(key)` 命中返回值、否则返回 `-1`；`put(key, value)` 写入或更新，写入后键数超过 `capacity` 就逐出最久未使用的键。两个操作平均 `O(1)`。`1 <= capacity <= 3000`，最多调用 `2 * 10^5` 次。

```python
class Node:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key: int = 0, val: int = 0) -> None:
        self.key, self.val = key, val
        self.prev: Node | None = None
        self.next: Node | None = None
class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.map: dict[int, Node] = {}
        self.head, self.tail = Node(), Node()      # 哨兵：head.next 是最近使用，tail.prev 是最久未使用
        self.head.next, self.tail.prev = self.tail, self.head
    def _unlink(self, node: Node) -> None:
        node.prev.next, node.next.prev = node.next, node.prev
    def _push_front(self, node: Node) -> None:
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node
    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._unlink(node)                         # 摘下来再放到最前面 = 标记为刚用过
        self._push_front(node)
        return node.val
    def put(self, key: int, value: int) -> None:
        if key in self.map:
            node = self.map[key]
            node.val = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self.map) == self.cap:              # 满了：逐出链表尾部（最久未使用）
            lru = self.tail.prev
            self._unlink(lru)
            del self.map[lru.key]
        node = self.map[key] = Node(key, value)
        self._push_front(node)
```

**例题：** LC 432 全 O(1) 的数据结构

实现 `AllOne`：`inc(key)` 计数加 `1`（不存在则以 `1` 插入），`dec(key)` 计数减 `1`（减到 `0` 就删除），`getMaxKey()` / `getMinKey()` 返回计数最大 / 最小的任意一个键（没有则返回 `""`）。每个操作平均 `O(1)`，键长 `1..10`，最多调用 `5 * 10^4` 次。

```python
class Bucket:
    __slots__ = ("cnt", "keys", "prev", "next")
    def __init__(self, cnt: int = 0) -> None:
        self.cnt = cnt
        self.keys: set[str] = set()
        self.prev: Bucket | None = None
        self.next: Bucket | None = None
class AllOne:
    def __init__(self) -> None:
        self.head, self.tail = Bucket(0), Bucket(-1)   # 哨兵：head.next 是最小计数桶，tail.prev 是最大
        self.head.next, self.tail.prev = self.tail, self.head
        self.where: dict[str, Bucket] = {}              # key -> 它当前所在的桶
    def _insert_after(self, node: Bucket, cnt: int) -> Bucket:
        new = Bucket(cnt)
        new.prev, new.next = node, node.next
        node.next.prev = new
        node.next = new
        return new
    def _remove(self, node: Bucket) -> None:
        node.prev.next, node.next.prev = node.next, node.prev
    def inc(self, key: str) -> None:
        cur = self.where.get(key)
        anchor = self.head if cur is None else cur      # 新桶（计数 +1）该插在 anchor 后面
        target = anchor.next
        new_cnt = anchor.cnt + 1
        if target.cnt != new_cnt:                       # 相邻桶不是 cnt + 1 就新建一个
            target = self._insert_after(anchor, new_cnt)
        target.keys.add(key)
        self.where[key] = target
        if cur is not None:
            cur.keys.discard(key)
            if not cur.keys:
                self._remove(cur)                       # 空桶要摘掉，否则 getMinKey 会读到空集合
    def dec(self, key: str) -> None:
        cur = self.where[key]
        if cur.cnt == 1:
            del self.where[key]                         # 计数归零：key 彻底删除
        else:
            target = cur.prev
            if target.cnt != cur.cnt - 1:
                target = self._insert_after(cur.prev, cur.cnt - 1)
            target.keys.add(key)
            self.where[key] = target
        cur.keys.discard(key)
        if not cur.keys:
            self._remove(cur)
    def getMaxKey(self) -> str:
        if self.tail.prev is self.head:
            return ""
        return next(iter(self.tail.prev.keys))          # 任取一个即可
    def getMinKey(self) -> str:
        if self.head.next is self.tail:
            return ""
        return next(iter(self.head.next.keys))
```

**例题：** LC 426 将二叉搜索树转化为排序的双向链表

把二叉搜索树原地转成已排序的循环双向链表（`left` 当前驱、`right` 当后继，首尾相连），返回最小节点。结点数 `0..2000`，值互不相同。

```python
def tree_to_doubly_list(root: Node | None) -> Node | None:
    if root is None:
        return None
    first = prev = None
    def inorder(node: Node | None) -> None:    # 中序：左 -> 根 -> 右
        nonlocal first, prev
        if node is None:
            return
        inorder(node.left)
        if prev:
            prev.right, node.left = node, prev # 把上一个节点和当前节点互相连上
        else:
            first = node                       # 中序第一个节点就是最小值
        prev = node
        inorder(node.right)                    # 此时 node.right 还没被改过
    inorder(root)
    first.left, prev.right = prev, first       # 首尾相连成环
    return first
```
