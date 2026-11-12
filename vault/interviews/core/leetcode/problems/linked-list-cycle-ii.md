---
slug: linked-list-cycle-ii
---
## Q
**LC 142 环形链表 II**｜Medium

返回链表开始入环的第一个节点，无环返回 `null`，不许修改链表。

## A
**一句话。** 快慢指针相遇后，一个回到 `head`，两个指针同速前进，再次相遇处就是入口。

```python
def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:              # 先走再比较
            while head is not slow:   # a = kL - b，同速会合
                head, slow = head.next, slow.next
            return head
    return None
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 把相遇点当入口：`[3,2,0,-4]`、`pos=1` 在 `-4` 相遇，入口是 `2`。
- 先比较再走：`slow = fast = head` 一开始就相等，无环的 `[1]` 会被当成有环。
- 阶段二仍让一个指针走两步：距离关系要求两者同速。

**追问。**
- 快指针为什么不会跳过慢指针？：进环后两者距离每步缩小 `1`，一定会重合。
- 允许 `O(n)` 空间？：用集合记录访问过的节点，最直观，面试可作第一版。

**同模式。** LC 141 环形链表、LC 287 寻找重复数、LC 202 快乐数、LC 160 相交链表
