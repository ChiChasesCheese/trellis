---
slug: reverse-nodes-in-k-group
---
## Q
**LC 25 K 个一组翻转链表**｜Hard

链表每 `k` 个节点一组翻转，最后不足 `k` 个的保持原序；必须真正交换节点，不能改值。

## A
**一句话。** 哑节点加迭代：先数够 `k` 个，再用反转链表翻这一段，`prev` 初值取下一组的头，翻完自动连上后面。

```python
def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    gp = dummy                   # 本组前一个节点
    while True:
        kth = gp
        for _ in range(k):       # 数够 k 个，否则原样保留
            kth = kth.next
            if not kth:
                return dummy.next
        nxt_group = kth.next
        prev, cur = nxt_group, gp.next   # prev 先指向下一组
        while cur is not nxt_group:
            cur.next, prev, cur = prev, cur, cur.next
        tail = gp.next           # 原来的头，现在是组尾
        gp.next = kth            # 上一组接新头
        gp = tail
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 不先数够 `k` 个：末尾不足的一组也被翻，`[1,2,3,4,5]`、`k=3` 得 `[3,2,1,5,4]`。
- `prev` 初值写成 `None`：组尾指向空，后面全丢，`k=2` 只剩 `[2,1]`。
- 忘记先存原来的头：它翻完是组尾，下一轮找不到起点。

**追问。**
- 不足的一组放在头部（从尾部分组）？：先整体反转，分组翻完再整体反转回来。
- 允许 `O(k)` 额外空间？：`k` 个节点入栈，弹出时顺次连接。

**同模式。** LC 206 反转链表、LC 92 反转链表 II、LC 24 两两交换链表中的节点、LC 61 旋转链表
