---
slug: odd-even-linked-list
---
## Q
**LC 328 奇偶链表**｜Medium

把链表中下标为奇数的节点排在前、下标为偶数的节点排在后，各组内保持原顺序，要求 `O(1)` 额外空间。

## A
**一句话。** 双指针 `odd` / `even` 隔点串成奇链、偶链，最后把偶链头接到奇链尾。

```python
def odd_even_list(head):
    if not head:
        return None
    odd, even = head, head.next
    even_head = even
    while even and even.next:
        odd.next = even.next    # 奇点跳过一个偶点
        odd = odd.next
        even.next = odd.next    # 偶点跳过刚摘下的奇点
        even = even.next
    odd.next = even_head
    return head
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 循环写成 `while odd and even`：偶数长度时 `odd` 变 `None` 再读 `odd.next`，`[1,2]` 崩溃。
- 忘了先存 `even_head`：循环后 `even` 已到链尾，找不回偶链头。

**追问。**
- 按节点值的奇偶分组？：两个哑头节点加尾插，遍历时按 `val % 2` 追加。
- 排序奇升偶降链表？：按下标拆成两条，反转偶链，再合并两个有序链表（LC 21）。

**同模式。** LC 86 分隔链表、LC 725 分隔链表、LC 143 重排链表、LC 148 排序链表
