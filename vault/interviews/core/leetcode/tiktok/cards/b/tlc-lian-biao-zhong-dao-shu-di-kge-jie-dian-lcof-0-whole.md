---
id: tlc-lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof-0-whole
node: b.lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof
type: qa
---
## Q
**剑指 Offer 22 链表中倒数第k个节点**｜Easy · CodeTop 国内累计 40 次 · 最近 2026-08-04（国内 CodeTop）

给定头节点为 `head` 的单链表，记录一系列训练项目编号，请查找并返回倒数第 `cnt` 个训练项目编号对应的节点。`1 <= head.length <= 100`，`0 <= head[i] <= 100`，`1 <= cnt <= head.length`。例：`head = [2,4,7,8], cnt = 1` → 返回值为 `8` 的节点（从它开始的链表是 `[8]`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 快慢指针：`fast` 先走 `cnt` 步，再让 `fast`、`slow` 同步前进，`fast` 走出链表（变成 `None`）时，`slow` 恰好指向倒数第 `cnt` 个节点。一遍扫描，`O(n)` 时间，`O(1)` 空间。

**识别。** 单链表只能从头往后走，不知道总长，「倒数第 `k`」是快慢指针保持固定间距的经典信号。倒数第 `cnt` 个节点就是「距离链表末尾（`None`）恰好 `cnt` 步」的节点，所以让两个指针之间始终隔 `cnt` 步，快的到终点时慢的就在目标上。

**推导。** 暴力：先遍历一遍数出长度 `n`，再从头走 `n - cnt` 步，两遍扫描，也是 `O(n)`。浪费：为了知道总长多走了一遍。洞察：不需要知道 `n`，只需要保持间距：`fast` 领先 `slow` 恰好 `cnt` 步，同步走到 `fast` 为 `None`，`slow` 就是要找的节点。

```python
def training_plan(head: ListNode | None, cnt: int) -> ListNode | None:
    fast = slow = head
    for _ in range(cnt):                         # fast 先走 cnt 步，与 slow 拉开 cnt 的间距
        if fast is None:                         # cnt 比链表还长：不存在倒数第 cnt 个
            return None
        fast = fast.next
    while fast:                                  # 同步前进，fast 走出链表时 slow 恰在倒数第 cnt 个
        fast, slow = fast.next, slow.next
    return slow
```

**运行。** `[2,4,7,8], cnt = 1` → 值为 `8` 的节点；`cnt = 4` → 值为 `2` 的头节点（`[2,4,7,8]`）；`[5], cnt = 1` → 值为 `5` 的节点；`[1,2], cnt = 3` → `None`（超过长度，防御性处理）。

**复杂度。** 时间 `O(n)`，`fast` 走 `n` 步，`slow` 走 `n - cnt` 步；空间 `O(1)`。

**易错点。**
- 间距差一：先走 `cnt` 步后用 `while fast.next` 判断，会停在倒数第 `cnt + 1` 个。`[2,4,7,8], cnt = 1` 返回 `7`，正确是 `8`。要么先走 `cnt` 步配 `while fast`，要么先走 `cnt - 1` 步配 `while fast.next`。
- `cnt` 超过链表长度时，`fast` 变成 `None` 后继续 `.next` 会抛 `AttributeError`；题目保证合法，但面试时要说出来并加判断。
- 返回的是节点，不是值：题面里的输出 `8` 表示该节点（从它开始的链表是 `[8]`）。

**追问。**
- 删除倒数第 `n` 个节点（LC 19）：加哨兵，让 `slow` 停在被删节点的前驱，`fast.next` 为 `None` 时结束，再 `slow.next = slow.next.next`。
- 找链表中间节点（LC 876）：`slow` 一次一步、`fast` 一次两步，`fast` 到末尾时 `slow` 在中间。
- 链表可能有环：先用快慢指针判环（LC 141 / 142），再谈倒数；有环时"倒数"没有意义。

**同模式。** LC 19 删除链表的倒数第 N 个结点、LC 876 链表的中间结点、LC 141 环形链表、LC 142 环形链表 II、LC 160 相交链表。
