---
slug: add-two-numbers
---
## Q
**LC 2 两数相加**｜Medium

两个非负整数按逆序存成链表（一个节点一位），返回它们的和，同样的链表形式。

## A
**一句话。** 逆序让个位在链头，两条链同步从低位走，每位加进位，写 `% 10`，进位传下去。

```python
def add_two_numbers(l1, l2):
    dummy = tail = ListNode()
    carry = 0
    while l1 or l2 or carry:     # 进位也算一轮
        if l1:
            carry += l1.val
            l1 = l1.next
        if l2:
            carry += l2.val
            l2 = l2.next
        carry, d = divmod(carry, 10)
        tail.next = ListNode(d)
        tail = tail.next
    return dummy.next
```

**复杂度。** 时间 `O(max(m,n))`，空间 `O(1)`（不计结果链）。

**易错点。**
- 循环条件漏了 `carry`：`[5]+[5]` 得 `[0]`，应为 `[0,1]`。
- 短链走完还读 `.val`：`[1,2,3]+[4]` 第二轮抛 `AttributeError`，要先判 `if l2`。

**追问。**
- 改成正序存储（LC 445）且不许反转输入？：两链各入栈，从栈顶（个位）弹出相加，头插法建结果。
- 为什么不转成整数再加？：Python 能过，定长整数语言会溢出；逐位模拟才通用。

**同模式。** LC 445 两数相加 II、LC 415 字符串相加、LC 67 二进制求和、LC 66 加一
