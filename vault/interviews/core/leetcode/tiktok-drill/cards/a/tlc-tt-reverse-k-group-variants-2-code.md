---
id: tlc-tt-reverse-k-group-variants-2-code
node: a.tt-reverse-k-group-variants
type: qa
step: 2
---
## Q
**K 个一组翻转链表的变体**｜写出 Python 实现

写 `reverse_k_group(head, k, *, from_tail=False, reverse_partial=False)`：每 `k` 个节点一组翻转，改指针不改值，额外空间 `O(1)`。`from_tail` 为真时从链表尾部开始分组（头部不足 `k` 个的那一组是余数组）；`reverse_partial` 为真时不足 `k` 个的那一组也翻转，否则保持原样。节点数 `1 <= n <= 10^5`，`k >= 1`，`k` 可以大于 `n`。

## A
**思路。** 先量出长度 `n`，用 `divmod(n, k)` 得到满组个数和余数；大小序列是「满组在前、余数组在后」，从尾分组则余数组在最前。随后用哑节点逐组处理：满组（或允许翻转的余数组）原地翻转并接线，其他组直接跳过。

```python
from itertools import chain, repeat


def reverse_k_group(head: ListNode | None, k: int, *, from_tail: bool = False,
                    reverse_partial: bool = False) -> ListNode | None:
    """每 k 个节点一组翻转。from_tail：从尾部开始分组；reverse_partial：不足 k 个的那一组也翻转。"""
    n, node = 0, head
    while node:
        n, node = n + 1, node.next
    full, rest = divmod(n, k)
    partial = (rest,) if rest else ()
    sizes = chain(partial, repeat(k, full)) if from_tail else chain(repeat(k, full), partial)

    dummy = ListNode(0, head)
    group_prev = dummy                                # 本组前一个节点
    for size in sizes:
        first = group_prev.next                       # 本组的头，翻转后变成本组的尾
        if size == k or reverse_partial:
            prev, cur = None, first
            for _ in range(size):
                cur.next, prev, cur = prev, cur, cur.next     # 标准的一步翻转
            group_prev.next = prev                    # 前一组接上新的组头
            first.next = cur                          # 本组的尾接上下一组的头
            group_prev = first
        else:                                         # 这一组保持原样：整组跳过
            for _ in range(size):
                group_prev = group_prev.next
    return dummy.next
```

运行：`[1,2,3,4,5,6,7,8]`、`k = 3`：默认 `[3, 2, 1, 6, 5, 4, 7, 8]`，`reverse_partial=True` → `[3, 2, 1, 6, 5, 4, 8, 7]`，`from_tail=True` → `[1, 2, 5, 4, 3, 8, 7, 6]`，两个都开 → `[2, 1, 5, 4, 3, 8, 7, 6]`；`[1,2,3,4,5]`、`k = 3`：默认 `[3, 2, 1, 4, 5]`，`reverse_partial=True` → `[3, 2, 1, 5, 4]`，`from_tail=True` → `[1, 2, 5, 4, 3]`；`k = 1` → 原链表；`[1,2]`、`k = 5`：默认 `[1, 2]`，`reverse_partial=True` → `[2, 1]`。

**复杂度。** 时间 `O(n)`：量长度一遍，分组处理一遍，每个节点至多被翻转一次；空间 `O(1)`。

**写法要点。**
- `cur.next, prev, cur = prev, cur, cur.next`：元组赋值先把右边三项都算好，再从左到右赋值，一行完成「反接、前移」，不需要临时变量 `nxt`；这个写法里 `cur.next` 必须排在最前，因为它依赖旧的 `cur`。
- `divmod(n, k)` 一次得到满组数和余数；`chain(repeat(k, full), partial)` 惰性拼出大小序列，不建列表，保持 `O(1)` 额外空间。
- 仅关键字参数（`*` 之后的 `from_tail`、`reverse_partial`）：调用处必须写名字，`reverse_k_group(head, 3, True, False)` 这种看不懂的布尔位置参数会被拒绝。
- 哑节点 `dummy` 让第一组和后面的组用同一套接线逻辑，不需要特判表头。
