---
slug: tt-reverse-k-group-variants
---
## Q
**K 个一组翻转链表的变体**｜Hard

链表每 `k` 个节点一组翻转，改指针不改值，额外空间 `O(1)`。基础版：从头分组，尾部不足 `k` 个保持原样。变体：（1）不足 `k` 个的一组也翻转；（2）从尾部开始分组，头部不足的一组保持原样；可组合。例：`[1..8]`，`k = 3` → 基础 `[3,2,1,6,5,4,7,8]`，从尾分组 `[1,2,5,4,3,8,7,6]`。

## A
**一句话。** 先量长度 `n`，算出每组大小序列（余数组放前面即从尾分组），再用哑节点逐组处理，该翻的原地翻转接线，不翻的跳过。

```python
def reverse_k_group(head, k, from_tail=False,
                    reverse_partial=False):
    n, node = 0, head
    while node:
        n, node = n + 1, node.next
    full, rest = divmod(n, k)
    part = (rest,) if rest else ()
    if from_tail:
        sizes = chain(part, repeat(k, full))
    else:
        sizes = chain(repeat(k, full), part)

    dummy = ListNode(0, head)
    gp = dummy                      # 本组前一个节点
    for size in sizes:
        first = gp.next             # 本组头，翻后变组尾
        if size == k or reverse_partial:
            prev, cur = None, first
            for _ in range(size):
                cur.next, prev, cur = prev, cur, cur.next
            gp.next = prev          # 前一组接新组头
            first.next = cur        # 本组尾接下一组头
            gp = first
        else:                       # 保持原样：整组跳过
            for _ in range(size):
                gp = gp.next
    return dummy.next
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 从尾分组时余数组仍放最后：`[1..8]`，`k = 3` 得到和从头分组相同的结果。
- 漏掉 `first.next = cur`：翻完的组尾指向 `None`，下一轮访问 `.next` 抛 `AttributeError`。
- 基础版翻了尾部：`[1,2,3,4,5]`，`k = 3` 应为 `[3,2,1,4,5]`，只有变体（1）才是 `[3,2,1,5,4]`。

**追问。**
- 只翻偶数长度的组（LC 2074）？：大小序列换成 `1, 2, 3, ...`，翻转条件改成组长为偶数。
- 为什么不用递归？：深度 `n / k`，`k` 小时会超默认递归上限，且要 `O(1)` 空间。

**同模式。** LC 25 K 个一组翻转链表、LC 2074 反转偶数长度组的节点、LC 24 两两交换链表中的节点、LC 92 反转链表 II
