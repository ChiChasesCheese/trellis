---
id: tlc-core-reverse-linked-list
node: p1.reverse-linked-list
type: qa
---
## Q
**LC 206 反转链表**｜Easy · LC TikTok 近 6 个月热度 53/100（全时段 62） · 近一年被问：美国 1 次、国内 9 次 · CodeTop 国内累计 243 次 · 最近 2026-10-28（国内面试记录） · 也在：Amazon、LeetCode Hot 100、Blind 75、NeetCode 150

给单链表的头节点 `head`，反转链表，并返回反转后的链表。链表中节点的数目范围是 `[0, 5000]`，`-5000 <= Node.val <= 5000`。例：`head = [1,2,3,4,5]` → `[5,4,3,2,1]`；`head = [1,2]` → `[2,1]`；`head = []` → `[]`。进阶：链表可以选用迭代或递归方式完成反转，你能否用两种方法解决这个问题？

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 迭代，三个指针：`prev`（已反转部分的头）、`cur`（当前节点）、`nxt`（先存下的后继）；每步把 `cur.next` 指向 `prev`，然后两个指针一起前进。`O(n)` 时间、`O(1)` 空间。

**识别。** 「单链表反转」只改指针方向，不改节点值；单链表没有前驱指针，所以处理到某个节点时必须带着「它的前一个节点」。节点数至多 `5000`，递归写法的深度也是 `5000`，超过 Python 默认递归上限，迭代更稳。

**推导。** 暴力：把所有节点的值读进数组，反向写回 → 浪费：`O(n)` 额外空间，且题目的重点是改指针 → 边走边反转，只改指针方向。

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

运行：`[1,2,3,4,5]` → `[5, 4, 3, 2, 1]`，`[1,2]` → `[2, 1]`，`[]` → `[]`，`[7]` → `[7]`。

**复杂度。** 时间 `O(n)`；空间 `O(1)`。

**拓展优化。**
- 递归版（题面进阶的第二种写法）：空间 `O(n)`；链表最长 `5000`，会超过 CPython 默认递归上限约 `1000`，所以面试里先写迭代版。

```python
def reverse_list(head: ListNode | None) -> ListNode | None:
    if head is None or head.next is None:
        return head                    # 空链表或单个节点：自己就是新头
    new_head = reverse_list(head.next)  # 后面整段先翻好，head.next 现在是它的尾
    head.next.next = head              # 让后半段的尾指回 head
    head.next = None                   # head 成为整条链表的新尾
    return new_head
```

**易错点。**
- 忘记先保存后继：先写 `cur.next = prev`，再写 `cur = cur.next`，此时 `cur.next` 已经是 `prev`，`[1,2,3]` 会在第一步之后只剩 `[1]`。
- 返回 `prev` 而不是 `cur`：循环结束时 `cur` 是 `None`；空链表直接返回 `prev = None`，`[]` 无需特判。
- 元组赋值的顺序：`head.next, prev, head = prev, head, head.next` 可行（右边先全部求值，再从左到右赋值），但换成 `head, head.next, prev = ...` 会先改 `head`，`head.next` 随即指向错误的节点，在 `[1,2,3]` 上抛 `AttributeError`。

**追问。**
- 只反转第 `m` 到第 `n` 个节点（LC 92）：找到第 `m-1` 个节点，反转这一段后接回两端，用哑节点避免 `m = 1` 的特判。
- 每 `k` 个一组反转（LC 25）：对每一组做同样的反转，再把组与组接起来。

**同模式。** LC 92 反转链表 II、LC 25 K 个一组翻转链表、LC 234 回文链表、LC 24 两两交换链表中的节点。
