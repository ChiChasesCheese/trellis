---
slug: lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof
---
## Q
**剑指 Offer 22 链表中倒数第k个节点**｜Easy

给单链表头节点 `head` 和 `cnt`（`1 <= cnt <=` 链表长度），返回倒数第 `cnt` 个节点。

## A
**一句话。** 快慢指针，`fast` 先走 `cnt` 步，再一起走到 `fast` 为空，`slow` 就是答案。

```python
def training_plan(head, cnt):
    fast = slow = head
    for _ in range(cnt):         # 拉开 cnt 的间距
        fast = fast.next
    while fast:
        fast, slow = fast.next, slow.next
    return slow
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 间距差一：先走 `cnt` 步却配 `while fast.next`，会停在倒数第 `cnt+1` 个，`[2,4,7,8], cnt=1` 得 `7`，应为 `8`。
- 返回节点而不是值：`8` 指从它开始的链表 `[8]`。

**追问。**
- `cnt` 可能超过长度怎么办？：先走的循环里遇到 `fast` 为空就返回 `None`。
- 删除倒数第 `n` 个节点？：加哨兵，让 `slow` 停在前驱，再 `slow.next = slow.next.next`。

**同模式。** LC 19 删除链表的倒数第 N 个结点、LC 876 链表的中间结点、LC 141 环形链表
