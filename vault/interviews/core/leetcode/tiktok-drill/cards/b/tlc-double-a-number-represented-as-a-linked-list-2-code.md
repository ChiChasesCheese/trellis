---
id: tlc-double-a-number-represented-as-a-linked-list-2-code
node: b.double-a-number-represented-as-a-linked-list
type: qa
step: 2
---
## Q
**LC 2816 翻倍以链表形式表示的数字**｜写出 Python 实现

链表（节点数 `[1, 10^4]`，每个节点 `0..9`，高位在前，无前导零）表示一个非负整数；把它翻倍，返回结果链表的头节点。要求不转成整数。

## A
**思路。** 翻倍时每位的进位只取决于右邻居是否 `>= 5`，所以从左到右扫一趟：每位 `= (自己*2 + 进位) % 10`。在头部放一个值为 0 的哑头，让最高位的进位自然落到哑头上；若哑头仍是 0 就丢掉。

```python
def double_it(head: ListNode | None) -> ListNode | None:
    dummy = ListNode(0, head)          # 哨兵：最高位进位时，它自己变成新的最高位 1
    cur: ListNode | None = dummy
    while cur:
        nxt = cur.next
        carry = 1 if nxt and nxt.val >= 5 else 0   # 下一位 *2 是否 >= 10
        cur.val = (cur.val * 2 + carry) % 10
        cur = nxt
    return dummy if dummy.val else dummy.next
```

运行：`[1,8,9]` → `[3,7,8]`，`[9,9,9]` → `[1,9,9,8]`，`[0]` → `[0]`，`[5]` → `[1,0]`，`[2,5]` → `[5,0]`，`10^4` 个 9 → 长度 `10001`，以 `1,9,9` 开头、以 `9,9,8` 结尾。

**复杂度。** 时间 `O(n)`：每个节点访问一次；空间 `O(1)`：原地改值，只多一个哑头。

**写法要点。** `nxt` 先取出再改 `cur.val`，因为判断用的是下一位原值，而下一位还没被改；`1 if nxt and nxt.val >= 5 else 0` 用短路处理链尾（最后一位没有右邻居，进位为 0）；`dummy if dummy.val else dummy.next` 同时解决「要不要新最高位」和「结果 0 不留前导零」；标注 `cur: ListNode | None` 因为循环以 `None` 结束。
