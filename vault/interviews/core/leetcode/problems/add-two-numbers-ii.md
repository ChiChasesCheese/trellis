---
slug: add-two-numbers-ii
---
## Q
**LC 445 两数相加 II**｜Medium

两个链表各表示一个非负整数，高位在前。求和并以同样形式返回，不能翻转输入。

## A
**一句话。** 两链表分别压栈，栈顶就是个位，同时弹栈相加带进位，每位用头插法接到结果前面。

```python
def add_two_numbers(l1, l2):
    s1, s2 = [], []
    while l1:
        s1.append(l1.val)
        l1 = l1.next
    while l2:
        s2.append(l2.val)
        l2 = l2.next
    head, carry = None, 0
    while s1 or s2 or carry:       # 进位也要处理
        carry += (s1.pop() if s1 else 0)
        carry += (s2.pop() if s2 else 0)
        carry, d = divmod(carry, 10)
        head = ListNode(d, head)   # 头插
    return head
```

**复杂度。** 时间 `O(n + m)`，空间 `O(n + m)`。

**易错点。**
- 循环条件漏了 `carry`：`[5] + [5]` 得 `[0]`，应为 `[1,0]`。
- 从链表头逐位相加：位数不同时错位，`[7,2,4,3] + [5,6,4]` 会得 `[12,8,8,3]`。

**追问。**
- 不用栈能做吗？：先反转两链表相加再还原，但会临时改动输入。
- 递归怎么写？：先算长度，长的先走差值步对齐，递归到底，回溯加进位。

**同模式。** LC 2 两数相加、LC 67 二进制求和、LC 415 字符串相加、LC 206 反转链表
