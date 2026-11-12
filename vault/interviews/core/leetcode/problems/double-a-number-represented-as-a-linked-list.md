---
slug: double-a-number-represented-as-a-linked-list
---
## Q
**LC 2816 翻倍以链表形式表示的数字**｜Medium

链表从高位到低位表示一个非负整数（每节点一位），把它翻倍，返回结果链表。

## A
**一句话。** 进位只来自右边一位（`>= 5` 就进 1），所以从左到右扫一趟，前面挂哑头接最高位进位。

```python
def double_it(head):
    dummy = ListNode(0, head)
    cur = dummy
    while cur:
        nxt = cur.next
        carry = 1 if nxt and nxt.val >= 5 else 0
        cur.val = (cur.val * 2 + carry) % 10
        cur = nxt
    return dummy if dummy.val else dummy.next
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 进位写成 `> 5`：`[5]` 得 `[0]`，应为 `[1,0]`。
- 忘了哑头：`[9,9,9]` 没地方放最高位的 `1`。
- 输入 `[0]` 时哑头值为 `0`，要丢掉，否则多一个前导零。

**追问。**
- 乘以任意个位数 `k` 怎么办？：进位不再是 0/1，改为反转链表或用栈，从低位带 `carry`，`divmod(val*k+carry, 10)`。
- 不改输入怎么做？：新建节点，或用栈存各位再从低位建链。

**同模式。** LC 2 两数相加、LC 445 两数相加 II、LC 66 加一、LC 43 字符串相乘
