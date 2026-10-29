---
id: tlc-plus-one-linked-list-2-code
node: b.plus-one-linked-list
type: qa
step: 2
---
## Q
**LC 369 给单链表加一**｜写出 Python 实现

非负整数用单链表表示，最高位在头节点，每个节点存一位（`0..9`，节点数 `1..100`，无前导零，除了零本身）。返回这个整数加一之后的链表头。要求 `O(1)` 额外空间。

## A
**思路。** 在原链表前接一个值为 `0` 的哑节点，遍历一遍记录最后一个值不为 `9` 的节点 `not_nine`（初值是哑节点）。给它加一，再把它后面的所有节点（都是 `9`）置为 `0`。如果哑节点变成了 `1`（说明全是 `9`），返回哑节点，否则返回原头。

```python
def plus_one(head: ListNode) -> ListNode:
    dummy = ListNode(0, head)                   # 哑节点：应对 999 -> 1000 需要新增最高位
    not_nine = dummy                            # 最后一个值不是 9 的节点
    node = head
    while node:
        if node.val != 9:
            not_nine = node
        node = node.next
    not_nine.val += 1                           # 它加一，它后面全是 9，全部变成 0
    node = not_nine.next
    while node:
        node.val = 0
        node = node.next
    return dummy if dummy.val else head         # 哑节点被进位成 1 才是新头
```

**运行。** `[1,2,3]` → `[1,2,4]`；`[0]` → `[1]`；`[9,9,9]` → `[1,0,0,0]`；`[1,9,9]` → `[2,0,0]`；`[9]` → `[1,0]`；`[1,9,2,9]` → `[1,9,3,0]`。

**复杂度。** 时间 `O(n)`；空间 `O(1)`，只多一个哑节点。

**写法要点。** 哑节点让「全是 `9`」和「普通情况」走同一段代码，不用分支判断；`return dummy if dummy.val else head` 用值的真假直接选择新头（`dummy.val` 是 `0` 或 `1`）；`while node:` 遍历到 `None` 为止，两次遍历共用变量 `node`；原地修改节点值，不新建节点（除了哑节点）。
