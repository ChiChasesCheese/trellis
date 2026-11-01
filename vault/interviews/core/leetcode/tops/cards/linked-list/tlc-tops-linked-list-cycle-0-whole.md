---
id: tlc-tops-linked-list-cycle-0-whole
node: linked-list.linked-list-cycle
type: qa
---
## Q
**LC 141 环形链表**｜Easy · 全公司热度第 92 名 · Blind 75、NeetCode 150、Hot 100、Top Interview 150

给你一个链表的头节点 `head`，判断链表中是否有环。如果链表中有某个节点，可以通过连续跟踪 `next` 指针再次到达，则链表中存在环。评测系统内部用整数 `pos` 表示链表尾连接到链表中的位置（索引从 0 开始，`-1` 表示无环），`pos` 不作为参数传入。有环返回 `true`，否则返回 `false`。链表中节点数目范围是 `[0, 10^4]`，`-10^5 <= Node.val <= 10^5`，`pos` 为 `-1` 或链表中的一个有效索引。进阶：你能用 `O(1)` 内存解决吗？

例：`head = [3,2,0,-4]`，`pos = 1` → `true`（尾部连回第二个节点）；`head = [1,2]`，`pos = 0` → `true`；`head = [1]`，`pos = -1` → `false`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 快慢指针（Floyd 判圈，tortoise and hare）；环检测的 `O(1)` 空间解法，LC 142、202 的基础。

**一句话。** 慢指针每次走 1 步、快指针每次走 2 步；有环则快指针终会在环内追上慢指针，无环则快指针先走到 `None`。

**识别。** 「判断有环」「`O(1)` 内存」「不能改链表」三者同时出现，就是快慢指针。`n <= 10^4`，线性即可。

**推导。** 最直接的想法是边走边记录访问过的结点，再次遇到就说明有环，`O(n)` 时间、`O(n)` 空间。要省掉这份记录：进环以后，快指针相对慢指针每步多走 1 格，环长为 `L` 时两者的距离每步缩小 1，最多 `L` 步必然相遇；而无环时快指针只会走到尽头。

**简单解法。** 同样的思路，只是用集合记住走过的结点本身（不是值，值会重复）：
```python
def has_cycle_set(head: ListNode | None) -> bool:
    seen: set[ListNode] = set()
    while head:
        if head in seen:        # 再次回到走过的结点：有环
            return True
        seen.add(head)
        head = head.next
    return False
```
空间 `O(n)`，面试里先说这个再改进也完全可以。

**最优解：** 快慢指针。

```python
def has_cycle(head: ListNode | None) -> bool:
    slow = fast = head
    while fast and fast.next:       # 快指针先到尽头，说明无环；fast.next 也要判，否则 fast.next.next 会越界
        slow = slow.next            # 慢指针一步
        fast = fast.next.next       # 快指针两步；进环后每轮把距离缩小 1，必定相遇
        if slow is fast:            # 用 is 比较结点身份，不能比较 val（值可以重复）
            return True
    return False
```

**运行。** `[3,2,0,-4]`、`pos = 1` → `True`；`[1,2]`、`pos = 0` → `True`；`[1]`、`pos = -1` → `False`；`[]` → `False`。

**复杂度。** 时间 `O(n)`（相遇时慢指针走了不到 `n` 步），空间 `O(1)`。

**拓展优化。**
- 求入环的第一个结点（LC 142）：相遇后让一个指针回到 `head`，两个都改为每次一步，再次相遇处就是入口。
- 判断「快乐数」（LC 202）、数组里的重复数（LC 287）：把「下一个状态」看成 `next`，同样是判圈。

**易错点。**
- 用 `slow.val == fast.val` 判断相遇：`[1,1,1]`（无环）会误报有环。必须用 `is` 比较结点本身。
- 循环条件只写 `while fast`：`fast.next` 为 `None` 时 `fast.next.next` 抛 `AttributeError`，如 `[1]`。
- 起点错开：`slow = head`、`fast = head.next` 再用 `while slow != fast` 时，空链表 `head = None` 会在取 `head.next` 时崩溃，需要先判空。

**同模式。** LC 142 环形链表 II、LC 202 快乐数、LC 287 寻找重复数、LC 876 链表的中间结点。
