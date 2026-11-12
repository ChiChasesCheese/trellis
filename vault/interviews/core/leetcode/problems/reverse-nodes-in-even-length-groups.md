---
slug: reverse-nodes-in-even-length-groups
---
## Q
**LC 2074 反转偶数长度组的节点**｜Medium

链表按 `1, 2, 3, ...` 的长度依次分组（最后一组可能不足）。把每个长度为偶数的组整体反转，返回头节点。

## A
**一句话。** 用 `prev` 指向上一组的尾，每组先数出实际长度，偶数就原地反转并接线。

```python
def reverse_even_length_groups(head):
    prev, size = head, 2     # 第 1 组长 1，奇数，不翻
    while prev.next:
        node, count = prev.next, 0
        while node and count < size:   # 数实际长度
            node, count = node.next, count + 1
        if count % 2 == 0:
            first = prev.next
            tail, cur = node, first    # 初值取下一组的头
            for _ in range(count):
                cur.next, tail, cur = tail, cur, cur.next
            prev.next = tail           # tail 成本组新头
            prev = first               # 原头变本组的尾
        else:
            for _ in range(count):
                prev = prev.next
        size += 1
    return head
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 用预期长度 `size` 判奇偶：`[1..9]` 最后一组预期 `4` 个、实际 `3` 个，不该反转。
- 反转的累积指针初值取 `None`：本组新尾指向空，后面节点全丢；要取下一组的头。
- 奇数组不推进 `prev`：下一轮从错误位置开始。

**追问。**
- 固定组长 `k` 怎么改（LC 25）？：同一框架，把 `size += 1` 换成固定 `k`，并且只在凑满 `k` 个时反转。
- 递归写法行吗？：深度只是组数，约 `sqrt(2n)`，但不是 `O(1)` 空间。

**同模式。** LC 25 K 个一组翻转链表、LC 206 反转链表、LC 92 反转链表 II、LC 24 两两交换链表中的节点
