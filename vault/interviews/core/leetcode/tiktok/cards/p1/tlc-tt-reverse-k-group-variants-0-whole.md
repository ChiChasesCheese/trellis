---
id: tlc-tt-reverse-k-group-variants-0-whole
node: p1.tt-reverse-k-group-variants
type: qa
---
## Q
**K 个一组翻转链表的变体**｜Hard · 近一年被问：美国 7 次、国内 12 次 · 最近 2026-10-27（国内面试记录）

给链表头节点 `head` 和正整数 `k`，每 `k` 个节点为一组翻转，必须改变节点的指针而不是节点的值，额外空间 `O(1)`。基础版：从头分组，尾部不足 `k` 个的部分保持原样。变体：（1）尾部不足 `k` 个的部分也要翻转；（2）从链表尾部开始分组，每 `k` 个一组翻转，头部不足 `k` 个的那一组保持原样；两个变体可以组合。节点数 `1 <= n <= 10^5`，`0 <= Node.val <= 10^5`，`k >= 1`，`k` 可以大于 `n`。例：`head = [1,2,3,4,5,6,7,8]`，`k = 3` → 基础 `[3,2,1,6,5,4,7,8]`；变体（1）`[3,2,1,6,5,4,8,7]`；变体（2）`[1,2,5,4,3,8,7,6]`；两者组合 `[2,1,5,4,3,8,7,6]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先走一遍量出长度 `n`，算出每一组的大小序列：`n // k` 个 `k`，再加上 `n % k` 的余数组，余数组放在前面（从尾分组）还是后面（从头分组）；然后用哑节点（dummy）逐组处理：该翻的组用标准的原地翻转并接线，不翻的组直接跳过。两个开关 `from_tail`、`reverse_partial` 覆盖全部变体，`O(n)` 时间、`O(1)` 空间。

**识别。** 「LC 25 加一条改规则」：难点不在翻转本身，而在两个独立的问题——**组的边界在哪里**、**哪些组要翻**。把它们和「翻转一段」解耦：边界只由 `n` 和 `k` 决定，是否翻转只看这一组是不是满 `k` 个（或开关允许翻转不满的）。单链表不能从后往前数，但长度一旦量出，「从尾分组」就等价于「余数组放在最前面」。

**推导。** 暴力：把节点值读进数组，分组翻转后写回，违反「改指针」，额外空间 `O(n)`。浪费：LC 25 的写法是「边走边数 `k` 个」，每个变体都要重写边界逻辑，尾分组更是无从下手。洞察：分组方案是 `n` 和 `k` 的函数，提前算成大小序列；每组的处理只剩两件事：翻或跳过。翻转一组时 `prev, cur = None, first` 逐个反接，再把前一组的尾接到新组头、本组原头（现在是尾）接到下一组的头。

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

运行：`[1,2,3,4,5,6,7,8]`、`k = 3`：默认 `[3, 2, 1, 6, 5, 4, 7, 8]`，`reverse_partial=True` → `[3, 2, 1, 6, 5, 4, 8, 7]`，`from_tail=True` → `[1, 2, 5, 4, 3, 8, 7, 6]`，两个都开 → `[2, 1, 5, 4, 3, 8, 7, 6]`；`[1,2,3,4,5]`、`k = 3`：默认 `[3, 2, 1, 4, 5]`，`reverse_partial=True` → `[3, 2, 1, 5, 4]`，`from_tail=True` → `[1, 2, 5, 4, 3]`；`k = 1` → 原链表；`[1,2]`、`k = 5`：默认 `[1, 2]`，`reverse_partial=True` → `[2, 1]`。`10^5` 个节点不到 `0.1` 秒。

**复杂度。** 时间 `O(n)`：量长度一遍、分组处理一遍，每个节点至多被翻转一次；空间 `O(1)`（`sizes` 是惰性迭代器，没有建列表）。

**易错点。**
- 从尾分组时余数组放错位置：仍把余数放在最后，`[1,...,8]`、`k = 3` 得到 `[3,2,1,6,5,4,7,8]`（和从头分组一样），正确是 `[1,2,5,4,3,8,7,6]`。
- 基础版和变体（1）只差一个开关：`[1,2,3,4,5]`、`k = 3`，基础版必须保持尾部 `[4,5]` 原样得到 `[3,2,1,4,5]`，变体（1）才得到 `[3,2,1,5,4]`。
- 漏掉 `first.next = cur`：翻完的组尾仍指向 `None`，下一轮 `group_prev.next` 是 `None`，访问 `.next` 抛 `AttributeError`。
- `k` 大于 `n`：整条链表就是余数组，默认不动，`reverse_partial=True` 整条翻转。

**追问。**
- 偶数长度组才翻转（LC 2074）：同一框架，大小序列换成 `1, 2, 3, ...`（最后一组取剩余长度），翻转条件改成「组长度为偶数」。
- 另一种写法：从尾分组 = 整条翻转、从头分组、再整条翻转回来，多两遍扫描但逻辑直观。
- 递归写法每层深度 `n / k`，`k` 小时 `10^5` 个节点会超过默认递归上限；`O(1)` 空间必须迭代。

**同模式。** LC 25 K 个一组翻转链表、LC 2074 反转偶数长度组的节点、LC 24 两两交换链表中的节点、LC 92 反转链表 II、LC 206 反转链表。
