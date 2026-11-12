---
slug: codetop-supp-1
---
## Q
**补充题 1 排序奇升偶降链表**｜Medium

链表奇数位升序、偶数位降序，原地按值升序排好，要求 `O(n)` 时间、`O(1)` 空间。

## A
**一句话。** 拆、反、并：按位置奇偶拆成两条，偶数位头插反转成升序，再合并两条升序链表。

```python
def sort_odd_even_list(head):
    odd, even = ListNode(), ListNode()
    tail, node, pos = odd, head, 1
    while node:
        nxt = node.next
        if pos % 2:             # 奇数位：尾插
            tail.next = tail = node
        else:                   # 偶数位：头插即反转
            node.next = even.next
            even.next = node
        node, pos = nxt, pos + 1
    tail.next = None            # 切断旧偶数结点，免得成环
    cur = dummy = ListNode()
    a, b = odd.next, even.next
    while a and b:
        if a.val <= b.val:
            cur.next, a = a, a.next
        else:
            cur.next, b = b, b.next
        cur = cur.next
    cur.next = a or b
    return dummy.next
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 偶数位不反转就合并：`[1,8,3,6,5,4,7,2]` 得 `[1,3,5,7,8,6,4,2]`。
- 拆完不切断 `tail.next`：合并时成环，遍历永不结束。
- 按值奇偶拆：要按位置拆，不看 `val`。

**追问。**
- 一般链表怎么排序？：归并排序，快慢指针找中点、断开、递归、合并，`O(n log n)`。

**同模式。** LC 206 反转链表、LC 21 合并两个有序链表、LC 328 奇偶链表、LC 148 排序链表
