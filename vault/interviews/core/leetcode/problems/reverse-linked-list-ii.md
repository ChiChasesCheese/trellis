---
slug: reverse-linked-list-ii
---
## Q
**LC 92 反转链表 II**｜Medium

反转单链表中从位置 `left` 到 `right`（从 1 起）的节点，一趟扫描完成。

## A
**一句话。** 哑节点加头插法：`pre` 停在 `left-1`，把 `cur` 后面的节点依次摘下来插到 `pre` 后面。

```python
def reverse_between(head, left, right):
    dummy = ListNode(0, head)     # left = 1 时也有前驱
    pre = dummy
    for _ in range(left - 1):
        pre = pre.next
    cur = pre.next                # 区间原来的第一个，会被挤到后面
    for _ in range(right - left):
        nxt = cur.next
        cur.next = nxt.next
        nxt.next = pre.next
        pre.next = nxt
    return dummy.next
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 不用哑节点：`left=1` 没有 `pre`，`[1,2,3,4,5]` 反转 `1..3` 得 `[1,4,3,2,5]`，应为 `[3,2,1,4,5]`。
- 反转后忘了接回尾巴：`2..4` 得 `[1,4,3,2]`，丢了 `5`。
- 循环次数写成 `right-left+1`：`cur` 本身不动，要挪的是它后面的 `right-left` 个。

**追问。**
- 每 `k` 个一组反转（LC 25）？：对每组做一次头插法，不足 `k` 个的最后一组不动。
- 整条反转（LC 206）？：`left=1`、`right=n` 的特例，`prev, cur` 两指针更短。

**同模式。** LC 206 反转链表、LC 25 K 个一组翻转链表、LC 24 两两交换链表中的节点、LC 143 重排链表
