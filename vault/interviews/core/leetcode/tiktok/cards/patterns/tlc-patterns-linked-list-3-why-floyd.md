---
id: tlc-patterns-linked-list-3-why-floyd
node: patterns.linked-list
type: qa
step: 3
---
## Q
**链表技巧（Linked List）｜正确性：快慢指针为什么能找到环的入口**

LC 142：快慢指针相遇之后，为什么把一个指针放回头节点、两个指针每次各走一步，会在入口相遇？相遇点本身是入口吗？

## A
设头到入口距离 `a`，入口到相遇点距离 `b`，环长 `c`。相遇时慢指针走了 `a + b`，快指针走了 `2(a + b)`；快指针比慢指针多走整数圈：`2(a + b) = a + b + k·c`，即 **`a + b = k·c`**，所以 `a = k·c - b = (k - 1)·c + (c - b)`。

`c - b` 正是相遇点沿环走回入口的距离。所以：一个指针从**头**出发、一个从**相遇点**出发，各走 `a` 步——前者到达入口，后者先绕 `k - 1` 圈再走 `c - b`，也在入口。两者必然在入口相遇。

```python
def detect_cycle(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:                   # 相遇：存在环
            slow = head
            while slow is not fast:        # 从头和相遇点同速前进，会在入口相遇
                slow, fast = slow.next, fast.next
            return slow
    return None
```

**相遇点不是入口的反例**：链表 `3 → 2 → 0 → -4`，尾部 `-4` 连回值为 `2` 的节点。快慢指针第一次相遇在值为 `-4` 的节点，而入口是值为 `2` 的节点。直接返回相遇点会给出 `-4`，正确答案是 `2`。

- 判环用 `slow is fast`（同一个节点），不要比较 `.val`（值可以重复）。
- 空间 `O(1)`，时间 `O(n)`；哈希集合存已访问节点也能做，空间 `O(n)`。
