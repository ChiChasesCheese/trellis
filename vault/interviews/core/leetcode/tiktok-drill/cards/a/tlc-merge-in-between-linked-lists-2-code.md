---
id: tlc-merge-in-between-linked-lists-2-code
node: a.merge-in-between-linked-lists
type: qa
step: 2
---
## Q
**LC 1669 合并两个链表**｜写出 Python 实现

链表 `list1`（长度 `3..10^4`）、整数 `a`、`b`（`1 <= a <= b < list1.length - 1`）、链表 `list2`（长度 `1..10^4`）。删除 `list1` 下标 `a..b` 的节点，把 `list2` 接在原位置，返回结果链表的头。要求原地改指针。

## A
**思路。** 用哑节点指向 `list1`，从哑节点走 `a` 步到达下标 `a - 1` 的节点 `before`；再从 `before` 走 `b - a + 2` 步到达下标 `b + 1` 的节点 `after`。然后 `before.next = list2`，找到 `list2` 的尾，接上 `after`。

```python
def merge_in_between(list1: ListNode, a: int, b: int, list2: ListNode) -> ListNode:
    dummy = ListNode(0, list1)                  # 哑节点：即使 a = 0 也有"a 的前一个节点"
    before = dummy
    for _ in range(a):                          # 走 a 步，停在下标 a - 1 的节点
        before = before.next
    after = before
    for _ in range(b - a + 2):                  # 再走 b - a + 2 步，停在下标 b + 1 的节点
        after = after.next
    before.next = list2                         # 接上 list2 的头
    tail = list2
    while tail.next:                            # 找 list2 的尾
        tail = tail.next
    tail.next = after                           # list2 的尾接回 list1 的后半段
    return dummy.next
```

**运行。** 示例 1 `[10,1,13,6,9,5]`，`a = 3, b = 4`，`[1000000,1000001,1000002]` → `[10,1,13,1000000,1000001,1000002,5]`；示例 2 → `[0,1,1000000,1000001,1000002,1000003,1000004,6]`；`[1,2,3,4]`、`a = 0, b = 1`、`[9]` → `[9,3,4]`。

**复杂度。** 时间 `O(n + m)`：最多走 `n` 个 `list1` 节点和 `m` 个 `list2` 节点；空间 `O(1)`。

**写法要点。** 哑节点（dummy node）让「下标 `a - 1` 的节点」总存在，下标从哑节点（相当于 `-1`）数起，所以走 `a` 步到 `a - 1`；`for _ in range(k)` 表示「只要次数、不要循环变量」；找尾用 `while tail.next`，停在最后一个节点，而不是 `while tail`（那样会走到 `None`）；先接 `list2` 再找尾，因为 `before` 后面的旧节点在 `after` 之前都已不需要。
