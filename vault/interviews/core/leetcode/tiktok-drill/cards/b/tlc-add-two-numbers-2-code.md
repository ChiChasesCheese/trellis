---
id: tlc-add-two-numbers-2-code
node: b.add-two-numbers
type: qa
step: 2
---
## Q
**LC 2 两数相加**｜写出 Python 实现

两个非空单链表 `l1`、`l2`（结点数 `1..100`，每个结点 `0..9`），按个位在前的逆序存储非负整数。返回它们的和（同样的逆序链表）。要求逐位相加，不要把整条链转成整数。

## A
**思路。** `carry` 同时充当「累加器」：每轮先把存在的 `l1`、`l2` 当前位加进去，再用 `divmod(carry, 10)` 拆成新进位和当前位，接到结果链表尾部。循环条件是 `l1 or l2 or carry`：任何一条还有结点，或者还剩进位，就继续。

```python
def add_two_numbers(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    dummy = tail = ListNode()          # 哑结点：头结点不用特判
    carry = 0
    while l1 or l2 or carry:           # 两条链都走完后，还要看有没有进位
        if l1:
            carry += l1.val
            l1 = l1.next
        if l2:
            carry += l2.val
            l2 = l2.next
        carry, digit = divmod(carry, 10)   # 商是新的进位，余数是当前位
        tail.next = ListNode(digit)
        tail = tail.next
    return dummy.next
```

运行：`l1=[2,4,3], l2=[5,6,4]` → `[7, 0, 8]`，`l1=[0], l2=[0]` → `[0]`，`l1=[9,9,9,9,9,9,9], l2=[9,9,9,9]` → `[8, 9, 9, 9, 0, 0, 0, 1]`，`l1=[5], l2=[5]（只剩进位）` → `[0, 1]`，`l1=[1], l2=[9,9]` → `[0, 0, 1]`。

**复杂度。** 时间 `O(max(m, n))`，两条链各走一遍；空间 `O(1)`（不计结果链表本身，结果长度至多 `max(m, n) + 1`）。

**写法要点。** `dummy = tail = ListNode()` 一行建哑结点并让尾指针指向它，最后返回 `dummy.next`；`while l1 or l2 or carry` 一个条件处理三种情况；`if l1:` 里累加并前进，缺失的位自然当 `0`；`carry, digit = divmod(carry, 10)` 一步得到商和余数；不用 `tail.next = tail = ListNode(...)` 这种链式赋值，写成两行更不易出错。
