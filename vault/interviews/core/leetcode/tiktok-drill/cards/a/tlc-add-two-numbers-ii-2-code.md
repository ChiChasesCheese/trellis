---
id: tlc-add-two-numbers-ii-2-code
node: a.add-two-numbers-ii
type: qa
step: 2
---
## Q
**LC 445 两数相加 II**｜写出 Python 实现

两个非空链表表示两个非负整数，高位在前，每个结点一位数字（链表长度 `1` 到 `100`）。返回和的链表，同样高位在前；不能修改输入链表。

## A
**思路。** 把两条链表各压进一个栈，栈顶就是个位。同时弹栈相加并带进位，每得到一位就用头插法接到结果链表前面；循环条件包含进位，保证最后的进位不丢。

```python
def add_two_numbers(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    s1: list[int] = []
    s2: list[int] = []
    while l1:                              # 压栈：栈顶就是个位
        s1.append(l1.val)
        l1 = l1.next
    while l2:
        s2.append(l2.val)
        l2 = l2.next
    head: ListNode | None = None
    carry = 0
    while s1 or s2 or carry:               # 最后一个进位也要处理
        carry += (s1.pop() if s1 else 0) + (s2.pop() if s2 else 0)
        carry, digit = divmod(carry, 10)
        head = ListNode(digit, head)       # 头插法：新结点接在已有结果前面
    return head
```

运行：`[7,2,4,3] + [5,6,4]` → `[7,8,0,7]`，`[2,4,3] + [5,6,4]` → `[8,0,7]`，`[0] + [0]` → `[0]`，`[5] + [5]` → `[1,0]`，`[9,9,9] + [1]` → `[1,0,0,0]`。

**复杂度。** 时间 `O(n + m)`：每个结点压栈一次、弹栈一次；空间 `O(n + m)`（两个栈）加结果链表。

**写法要点。** 用 `list` 当栈（`append` / `pop` 都是均摊 `O(1)`）；`s1.pop() if s1 else 0` 让短的数自动补 `0`，不用先对齐长度；`divmod(carry, 10)` 一次同时得到新进位和当前位；`ListNode(digit, head)` 在构造时就把新结点接到旧头前面，头插法只需一行。
