---
slug: split-linked-list-in-parts
---
## Q
**LC 725 分隔链表**｜Medium

把单链表 `head` 分成 `k` 个连续的部分：任意两部分长度相差不超过 1，靠前的部分不短于靠后的部分，不足的部分用 `None` 补。返回这 `k` 个链表头。

## A
**一句话。** 先数长度 `n`，每部分至少 `n // k` 个，前 `n % k` 部分多 1 个；按这个长度走并在末尾断链。

```python
def split_list_to_parts(head, k):
    n, cur = 0, head
    while cur:
        n += 1
        cur = cur.next
    size, extra = divmod(n, k)
    parts, cur = [], head
    for i in range(k):
        parts.append(cur)
        for _ in range(size + (i < extra) - 1):
            cur = cur.next         # 走到本部分最后一个结点
        if cur:
            cur.next, cur = None, cur.next   # 断开并前进
    return parts
```

**复杂度。** 时间 `O(n + k)`，空间 `O(1)`（不计返回的列表）。

**易错点。**
- `n < k` 时 `size = 0`：多出来的部分长度为 0，直接放 `None`，不能去取 `cur.next`。
- 断链顺序错：先 `cur.next = None` 会丢掉后半段，需要同时赋值或先存 `nxt`。
- 已经走到链尾还断链：`cur` 为 `None` 时要跳过 `cur.next` 的赋值。

**追问。**
- 为什么前 `n % k` 部分多 1 个？：均分后余数要分给靠前的部分，题目也要求前面的不短于后面的。
- 不先数长度行吗？：不数就不知道每份多长，只能先遍历一次，所以是两遍扫描。

**同模式。** LC 328 奇偶链表、LC 86 分隔链表、LC 61 旋转链表、LC 876 链表的中间结点
