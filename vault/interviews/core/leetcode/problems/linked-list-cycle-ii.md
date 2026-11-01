---
slug: linked-list-cycle-ii
---
## Q
**LC 142 环形链表 II**｜Medium

给定一个链表的头节点 `head`，返回链表开始入环的第一个节点；如果链表无环，则返回 `null`。评测系统内部用整数 `pos` 表示链表尾连接到链表中的位置（索引从 0 开始，`-1` 表示无环），`pos` 不作为参数传入。不允许修改链表。链表中节点的数目范围在 `[0, 10^4]` 内，`-10^5 <= Node.val <= 10^5`，`pos` 为 `-1` 或链表中的一个有效索引。进阶：是否可以使用 `O(1)` 空间解决？

例：`head = [3,2,0,-4]`，`pos = 1` → 返回下标 1 的节点（值 `2`）；`head = [1,2]`，`pos = 0` → 返回下标 0 的节点；`head = [1]`，`pos = -1` → `null`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** Floyd 判圈算法的第二阶段（找环入口）；环相关距离的代数关系。

**一句话。** 快慢指针相遇后，让一个指针回到 `head`，两个指针都改为每次一步，再次相遇的结点就是环入口。

**识别。** 「返回入环的第一个结点」比 LC 141 多一步，且「不许改链表」「`O(1)` 空间」要求用快慢指针而不是标记。`n <= 10^4`，线性。

**推导。** 记入口前有 `a` 个结点，入口到相遇点沿环走了 `b`，环长 `L`。相遇时慢指针走了 `a + b`，快指针走了 `2(a + b)`，快比慢多走了整数圈：`2(a + b) = a + b + kL`，所以 `a + b = kL`，即 `a = kL - b`。含义是：从相遇点再走 `a` 步，恰好绕若干圈回到入口。所以一个指针从 `head` 出发、一个指针从相遇点出发，同速前进 `a` 步后在入口会合。

**简单解法。** 用集合记住走过的结点，第一个重复出现的结点就是入口：
```python
def detect_cycle_set(head: ListNode | None) -> ListNode | None:
    seen: set[ListNode] = set()
    while head:
        if head in seen:
            return head
        seen.add(head)
        head = head.next
    return None
```
空间 `O(n)`。

**最优解：** Floyd 两阶段。

```python
def detect_cycle(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:                    # 阶段一：先移动再比较，相遇说明有环
            # 阶段二：a = kL - b，head 与相遇点同速前进，会在入口会合
            while head is not slow:
                head, slow = head.next, slow.next
            return head
    return None                             # 快指针走到尽头：无环
```

**运行。** `[3,2,0,-4]`、`pos = 1` → 值为 `2` 的节点（下标 1）；`[1,2]`、`pos = 0` → 值为 `1` 的节点（下标 0）；`[1]`、`pos = -1` → `None`；`[1]`、`pos = 0`（自环）→ 该节点本身。

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**拓展优化。**
- 环长：相遇后固定一个指针，另一个绕一圈数步数。
- 把「下一个位置」当 `next` 同样适用：LC 287 寻找重复数，数组下标到值就是一条链，环入口就是重复数。

**易错点。**
- 把相遇点当入口：`[3,2,0,-4]`、`pos = 1` 时两个指针在值为 `-4` 的结点相遇，入口是值为 `2` 的结点；返回相遇点得到 `-4`。
- 把 `while slow is not fast` 当阶段一的循环条件：`slow = fast = head` 一开始就相等，循环一次不进，无环的 `[1]` 会被当成相遇并返回 `1`。必须先走一步再比较。
- 阶段二里让其中一个指针仍走两步：距离关系 `a = kL - b` 要求两者同速，走两步会错过入口。

**同模式。** LC 141 环形链表、LC 287 寻找重复数、LC 202 快乐数、LC 160 相交链表。
