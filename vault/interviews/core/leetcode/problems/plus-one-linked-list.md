---
slug: plus-one-linked-list
---
## Q
**LC 369 给单链表加一**｜Medium

链表表示一个非负整数，最高位在表头。把它加 `1`，返回结果链表。

## A
**一句话。** 进位只沿末尾连续的 `9` 传：最后一个非 `9` 节点加一，其后全置 `0`，哑节点兜底全 `9`。

```python
def plus_one(head):
    dummy = ListNode(0, head)   # 应对 999 -> 1000
    not_nine = dummy            # 最后一个非 9 节点
    node = head
    while node:
        if node.val != 9:
            not_nine = node
        node = node.next
    not_nine.val += 1
    node = not_nine.next
    while node:                 # 其后全是 9，变 0
        node.val = 0
        node = node.next
    return dummy if dummy.val else head
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 只给末节点加一：`[1,9,9]` 得 `[1,9,10]`，应为 `[2,0,0]`。
- 没有哑节点：`[9,9,9]` 得 `[0,0,0]`，应为 `[1,0,0,0]`。
- `not_nine` 初值取 `head`：`[9,9]` 的头被加成 `10`。

**追问。**
- 低位在前的存储怎么做？：从头遇 `9` 变 `0` 继续，遇非 `9` 加一结束；走到尾仍有进位就补一个 `1`。
- 加任意链表（LC 445）？：用栈或反转对齐低位，逐位相加带进位。

**同模式。** LC 66 加一、LC 2 两数相加、LC 445 两数相加 II、LC 206 反转链表
