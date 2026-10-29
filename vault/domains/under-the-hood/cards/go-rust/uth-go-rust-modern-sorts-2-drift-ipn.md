---
id: uth-go-rust-modern-sorts-2-drift-ipn
node: go-rust.modern-sorts
type: qa
step: 2
---
## Q
**Rust 的 sort 与 sort_unstable 是什么算法**｜Rust · 1.81 起

Rust 1.81 换掉了标准库的排序，稳定与不稳定的分别是什么？

## A
**背景。** 真实数据常常已经部分有序。归并排序（merge sort）把两段各自排好的数据合并成一段；如果输入里本来就有现成的有序段（run），就可以直接拿来合并，省掉重新排序的功夫。稳定指相等元素保持原来的先后顺序。

**结构。** 稳定的 `sort` 是 driftsort；不稳定的 `sort_unstable` 是 ipnsort（快排加堆排序兜底）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">driftsort: 先找输入里已有的顺序段 (run)</text>
<rect x="10" y="26" width="70" height="28" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="45" y="45" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">升序</text>
<rect x="80" y="26" width="60" height="28" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="110" y="45" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">降序</text>
<rect x="140" y="26" width="110" height="28" rx="2" fill="none" style="stroke:var(--accent,#3b6fd4)" stroke-width="1" stroke-dasharray="4 3"/>
<text x="195" y="45" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">无序</text>
<rect x="250" y="26" width="80" height="28" rx="2" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="290" y="45" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">升序</text>
<text x="8" y="70" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">降序段整段反转; 无序段交给稳定快排</text>
<text x="8" y="96" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">再按 powersort 的启发式决定先合并哪两段:</text>
<rect x="10" y="108" width="70" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="45" y="124.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="90" y="108" width="60" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="120" y="124.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<rect x="160" y="108" width="80" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="200" y="124.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<rect x="250" y="108" width="80" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="290" y="124.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D</text>
<line x1="80" y1="132" x2="95" y2="150" stroke="currentColor" stroke-width="1"/>
<line x1="90" y1="132" x2="95" y2="150" stroke="currentColor" stroke-width="1"/>
<rect x="40" y="150" width="110" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="95" y="166.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A+B</text>
<text x="8" y="192" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ipnsort (不稳定): 整个数组是一整段升序/降序就 O(n) 结束</text>
</svg>
```

**细节。**

- driftsort：先找输入里已有的升序或降序段（run），按 powersort 的启发式决定归并顺序
- 无序的段交给稳定快排
- ipnsort：长度 ≤ 20 用插入排序；整个数组是一整段有序或逆序，就 O(n) 结束
- 否则快排，不平衡划分超过 `2·⌊log₂ n⌋` 次就改堆排序

**为什么。** 真实数据常常部分有序，利用已有的顺序比无视它更快。

**例题：** LC 148 排序链表（同类：LC 56 合并区间）

给链表头节点，按升序排好并返回，节点数不超过 `5 * 10^4`。例：`[4,2,1,3]` → `[1,2,3,4]`。下面是归并排序：从中间断开，两半各自排好，再合并两个有序链表，和 driftsort 合并有序段是同一个动作。

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def sort_list(head: ListNode | None) -> ListNode | None:
    if head is None or head.next is None:
        return head
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None
    left, right = sort_list(head), sort_list(mid)

    dummy = ListNode()
    tail = dummy
    while left and right:
        if left.val <= right.val:
            tail.next, left = left, left.next
        else:
            tail.next, right = right, right.next
        tail = tail.next
    tail.next = left or right
    return dummy.next
```
