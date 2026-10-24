---
id: tlc-reverse-nodes-in-k-group-2-code
node: a.reverse-nodes-in-k-group
type: qa
step: 2
---
## Q
**LC 25 K 个一组翻转链表**｜写出 Python 实现

单链表头节点 `head`（节点数 `n` 为 `1` 到 `5000`，值在 `[0, 1000]`）和整数 `k`（`1 <= k <= n`）。每 `k` 个节点一组翻转，最后不足 `k` 个的节点保持原样。必须真正交换节点（不能只改值），额外空间 `O(1)`。

## A
**思路。** 用哑节点作为第一组的前驱。每轮：从 `group_prev` 往后数 `k` 个得到 `kth`，数不够就返回；记下 `group_next`；用 `prev = group_next` 起步反转 `group_prev.next .. kth`；最后把 `group_prev.next` 指向 `kth`，`group_prev` 换成原来的组头（现在的组尾）。

```python
def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    dummy = ListNode(0, head)
    group_prev = dummy                       # 本组前一个节点（上一组翻转后的尾）
    while True:
        kth: ListNode | None = group_prev
        for _ in range(k):                   # 往后数 k 个；不够 k 个就结束，余下原样保留
            kth = kth.next
            if kth is None:
                return dummy.next
        group_next = kth.next                # 下一组的头
        prev, cur = group_next, group_prev.next      # prev 先指向下一组：翻完后本组尾巴自动接上
        while cur is not group_next:
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        tail = group_prev.next               # 翻转前的头，现在是本组的尾
        group_prev.next = kth                # 前一段接上新的头（kth）
        group_prev = tail
```

运行：`([1,2,3,4,5], 2)` → `[2, 1, 4, 3, 5]`，`([1,2,3,4,5], 3)` → `[3, 2, 1, 4, 5]`，`([1], 1)` → `[1]`，`([1,2,3], 3)` → `[3, 2, 1]`，`([1,2,3,4,5,6,7], 3)` → `[3, 2, 1, 6, 5, 4, 7]`；`5000` 个节点、`k = 2` 直接通过。

**复杂度。** 时间 `O(n)`：每个节点被数一次、翻一次；空间 `O(1)`：只有几个指针。

**写法要点。** `dummy = ListNode(0, head)` 一次构造哑节点并接上头；`for _ in range(k)` 里一边前进一边判空，数不够就直接 `return`，不需要单独的计数；`while True` 配合内部的 `return` 表达「直到不足一组」；反转内层的终止条件是 `cur is not group_next`，用身份比较而不是 `!=`；`prev` 的初值取 `group_next`，是整段代码最关键的一行，它让组尾自动连上后面，省掉一次事后接线。
