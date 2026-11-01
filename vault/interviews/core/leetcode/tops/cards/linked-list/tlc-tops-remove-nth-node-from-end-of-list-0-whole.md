---
id: tlc-tops-remove-nth-node-from-end-of-list-0-whole
node: linked-list.remove-nth-node-from-end-of-list
type: qa
---
## Q
**LC 19 删除链表的倒数第 N 个结点**｜Medium · 全公司热度第 192 名 · Blind 75、NeetCode 150、Hot 100、Top Interview 150

给你一个链表，删除链表的倒数第 `n` 个结点，并且返回链表的头结点。链表中结点的数目为 `sz`，`1 <= sz <= 30`，`0 <= Node.val <= 100`，`1 <= n <= sz`。进阶：你能尝试使用一趟扫描实现吗？

例：`head = [1,2,3,4,5]`，`n = 2` → `[1,2,3,5]`；`head = [1]`，`n = 1` → `[]`；`head = [1,2]`，`n = 1` → `[1]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 快慢指针保持固定间距（gap = n）+ 哑结点（dummy node）处理删除头结点。

**一句话。** 让 `fast` 先走 `n` 步，再让 `fast`、`slow` 同速前进；`fast` 到最后一个结点时，`slow` 恰好停在待删结点的前一个。

**识别。** 「倒数第 `n` 个」在单链表里无法直接定位；「一趟扫描」要求用间距代替长度。「删除」要前驱结点，头结点没有前驱，所以要哑结点。`sz <= 30`，怎么写都不慢，考的是指针技巧。

**推导。** 先数出长度 `L` 再走 `L - n` 步，要两趟。第一趟的作用只是求 `L`，用间距就能省掉：两个指针相距 `n`，前一个到尾时后一个离尾也是 `n`，位置就是倒数第 `n`。为了停在待删结点的前一个，起点放在哑结点，`fast` 停在最后一个结点（`fast.next` 为空）。

**简单解法。** 两趟扫描：第一趟数长度，第二趟走到第 `L - n` 个结点（从哑结点数起）删除它的下一个。
```python
def remove_nth_two_pass(head: ListNode | None, n: int) -> ListNode | None:
    dummy = ListNode(0, head)
    length = 0
    while head:
        length += 1
        head = head.next
    cur = dummy
    for _ in range(length - n):     # 走到待删结点的前一个
        cur = cur.next
    cur.next = cur.next.next
    return dummy.next
```

**最优解：** 一趟扫描，保持间距。

```python
def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    dummy = ListNode(0, head)       # 哑结点：删头结点时也有前驱，不用特判
    fast = slow = dummy
    for _ in range(n):              # fast 先走 n 步，和 slow 拉开 n 的间距
        fast = fast.next
    while fast.next:                # fast 停在最后一个结点时，slow 在待删结点的前一个
        fast, slow = fast.next, slow.next
    slow.next = slow.next.next      # 跳过待删结点
    return dummy.next               # 头结点可能被删，不能返回 head
```

**运行。** `[1,2,3,4,5]`、`n = 2` → `[1, 2, 3, 5]`；`[1]`、`n = 1` → `[]`；`[1,2]`、`n = 1` → `[1]`；`[1,2]`、`n = 2`（删头）→ `[2]`。

**复杂度。** 时间 `O(sz)`，一趟；空间 `O(1)`。

**拓展优化。**
- 递归写法：回溯时计数，计到 `n` 的那层删除，空间 `O(sz)` 栈。
- 同样的固定间距：链表的中间结点（快指针每次两步）、旋转链表（LC 61）。

**易错点。**
- 没有哑结点：`[1]`、`n = 1` 时 `fast` 走完 `n` 步变成 `None`，随后 `fast.next` 抛 `AttributeError`。
- 间距、起点、停止条件必须成套：起点哑结点、先走 `n` 步、条件 `while fast.next`，改任何一个都会偏一位，如 `[1,2,3,4,5]`、`n = 2` 会删到 `3` 或 `5`。
- 返回 `head` 而不是 `dummy.next`：`[1,2]`、`n = 2` 删头后，旧 `head` 仍指向值为 `1` 的结点，返回的是 `[1, 2]`，等于没删。

**同模式。** LC 876 链表的中间结点、LC 61 旋转链表、LC 141 环形链表、LC 160 相交链表。
