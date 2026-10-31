---
id: tlc-reorder-list-0-whole
node: b.reorder-list
type: qa
---
## Q
**LC 143 重排链表**｜Medium · LC TikTok 全时段热度 62/100 · 近一年被问：美国 0 次、国内 1 次 · CodeTop 国内累计 91 次 · 最近 2026-07-21（国内面试记录）

给单链表 `L` 的头节点 `head`，表示为 `L0 → L1 → … → Ln-1 → Ln`。把它重排成 `L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …`。不能只改节点里的值，必须真正地交换节点（改指针）。链表长度在 `[1, 5 * 10^4]` 内，`1 <= node.val <= 1000`。例：`head = [1,2,3,4]` → `[1,4,2,3]`；`head = [1,2,3,4,5]` → `[1,5,2,4,3]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 三步：快慢指针找到中点并**断开**；把后半段**翻转**；前半段和翻转后的后半段**交替拼接**。`O(n)` 时间，`O(1)` 空间。

**识别。** 目标顺序是「头、尾、头、尾……」，需要从**尾部**往前取节点，而单链表没有前驱指针，无法倒着走。把后半段翻转，「从尾往前」就变成了「从头往后」。于是它是三个链表基本操作的组合：找中点（LC 876）、翻转（LC 206）、交替合并（类似 LC 21）。

**推导。** 暴力：把所有节点放进数组，用左右两个下标交替取节点重新连接，`O(n)` 时间但 `O(n)` 额外空间。递归也能做（利用回溯从尾部返回），但链表长 `5 * 10^4`，递归深度会超过 Python 默认上限 1000。洞察：只需要后半段倒过来读一遍，所以翻转后半段就能省掉数组；翻转前必须先在中点断开，否则前半段的尾部还指着后半段，会和翻转后的指针缠成环。

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

运行：`[1,2,3,4]` → `[1, 4, 2, 3]`，`[1,2,3,4,5]` → `[1, 5, 2, 4, 3]`，`[1]` → `[1]`，`[1,2]` → `[1, 2]`，`[1,2,3]` → `[1, 3, 2]`，`5 * 10^4` 个节点的链表也能正确处理。

**复杂度。** 时间 `O(n)`：找中点、翻转、拼接各扫一遍；空间 `O(1)`。

**易错点。**
- 中点处不断开：前半段的尾巴仍指向后半段原来的位置。`[1,2,3,4]` 拼接后节点 `3` 的 `next` 指向它自己，遍历永远不会结束，前 8 个值是 `[1, 4, 2, 3, 3, 3, 3, 3]`。
- 先把 `slow.next = None` 再写 `second = slow.next`：此时 `second` 已是 `None`，后半段丢了。要用元组赋值 `second, slow.next = slow.next, None`，或先取 `second` 再断开。
- 翻转循环结束时 `second` 已经是 `None`，翻转后的新头在 `prev` 里。漏掉 `second = prev`，拼接循环一次都不执行，`[1,2,3,4]` 只剩前半段 `[1, 2]`。
- 拼接时先写 `first.next = second` 再去读 `first.next`：读到的已不是原来的后继。要先把两个后继都存下来。

**追问。**
- 允许 `O(n)` 额外空间时：把节点放进数组，用左右下标交替连接，或用 `deque` 交替 `popleft` / `pop`，代码更短，但不满足进阶的原地要求。
- 回文链表（LC 234）用同样的「找中点 + 翻转后半段」，再逐个比较；复原链表时可以再翻转一次后半段接回去。
- 找中点时 `fast.next and fast.next.next` 使偶数长度的两半恰好等长；写成 `fast and fast.next` 时偶数长度的前半段会比后半段多 2 个节点，拼接结果仍然正确，只是不再等分。

**同模式。** LC 876 链表的中间结点、LC 206 反转链表、LC 21 合并两个有序链表、LC 234 回文链表、LC 148 排序链表。
