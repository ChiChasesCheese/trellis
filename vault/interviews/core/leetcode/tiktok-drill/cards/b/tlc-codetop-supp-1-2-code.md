---
id: tlc-codetop-supp-1-2-code
node: b.codetop-supp-1
type: qa
step: 2
---
## Q
**补充题 1 排序奇升偶降链表**｜写出 Python 实现

单链表（长度 `0..5 * 10^4`，值在 `[-10^5, 10^5]`），位置从 `1` 开始，奇数位上升序、偶数位上降序。写 `sort_odd_even_list(head)`，返回整条链表按值升序后的头结点，`O(n)` 时间、`O(1)` 额外空间。

## A
**思路。** 一趟扫描把链表按位置拆成奇链和偶链：奇链尾插，偶链头插（头插即反转）；然后合并两条升序链表。

```python
def sort_odd_even_list(head: ListNode | None) -> ListNode | None:
    odd_dummy, even_dummy = ListNode(), ListNode()
    odd_tail = odd_dummy
    node, pos = head, 1
    while node:
        nxt = node.next
        if pos % 2:                    # 奇数位：本来就升序，尾插保持顺序
            odd_tail.next = node
            odd_tail = node
        else:                          # 偶数位：本来降序，头插即反转成升序
            node.next = even_dummy.next
            even_dummy.next = node
        node, pos = nxt, pos + 1
    odd_tail.next = None               # 切断最后一个奇数结点指向旧偶数结点的边
    tail = dummy = ListNode()          # 合并两条升序链表
    a, b = odd_dummy.next, even_dummy.next
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next
```

运行：`[1,8,3,6,5,4,7,2]` → `[1, 2, 3, 4, 5, 6, 7, 8]`，`[1,8,3,6,5,4,7]` → `[1, 3, 4, 5, 6, 7, 8]`，`[5]` → `[5]`，`[2,9]` → `[2, 9]`，空链表 → `None`。

**复杂度。** 时间 `O(n)`：拆分一趟、合并一趟；空间 `O(1)`：只有几个指针和两个哑结点。

**写法要点。** 两个哑结点（`ListNode()`）让「第一个结点」和「后续结点」用同一段代码处理，不用特判头。先存 `nxt = node.next` 再改指针，否则头插会丢掉后面的链表。`tail.next, a = a, a.next` 是元组赋值：右边整体先求值，再从左到右赋值，所以安全；但 `a, a.next = a.next, tail` 这种写法会先把 `a` 改成下一个结点，再给「新的 `a`」设 `next`，指针接错。`tail.next = a or b` 一句话接上剩下的那一条。
