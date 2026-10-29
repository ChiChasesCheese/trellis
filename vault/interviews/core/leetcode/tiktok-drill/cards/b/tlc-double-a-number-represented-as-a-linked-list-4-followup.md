---
id: tlc-double-a-number-represented-as-a-linked-list-4-followup
node: b.double-a-number-represented-as-a-linked-list
type: qa
step: 4
---
## Q
**LC 2816 翻倍以链表形式表示的数字**｜追问

面试官接着问：（1）如果乘以任意个位数 `k`，前瞻还成立吗？（2）面试官要求你用常规的「反转 → 计算 → 反转」写一遍？（3）为什么不直接转成整数？

## A
1. **乘以 `k`**：进位可以大到 `k-1`，且依赖右边的进位，不再是「看右邻居一位」就够。改用从低位带 `carry` 的做法：反转后 `carry, val = divmod(val * k + carry, 10)`，最后若 `carry` 非 0 再补节点。
2. **反转写法**：

```python
def reverse(head: ListNode | None) -> ListNode | None:
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev

def double_it_rev(head: ListNode | None) -> ListNode | None:
    head = reverse(head)               # 低位在前，进位自然向后传
    carry = 0
    cur, last = head, None
    while cur:
        carry, cur.val = divmod(cur.val * 2 + carry, 10)
        cur, last = cur.next, cur
    if carry:
        last.next = ListNode(carry)    # 最高位进位：在反转后的链尾补一个节点
    return reverse(head)
```

三趟都是 `O(n)` 时间、`O(1)` 空间；单趟前瞻版少两次反转，这是它的优势。
3. **转整数**：`10^4` 位的字符串超过 Python 默认 4300 位上限，`int(s)` 抛 `ValueError`；即使放开上限，也绕开了题目要考的指针与进位处理。

**Python 提醒**：`head.next, prev, head = prev, head, head.next` 的右边先整体求值再赋值，所以顺序安全；如果拆成三行，必须先保存 `head.next`。
