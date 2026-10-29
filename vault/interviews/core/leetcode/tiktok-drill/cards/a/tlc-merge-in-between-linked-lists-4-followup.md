---
id: tlc-merge-in-between-linked-lists-4-followup
node: a.merge-in-between-linked-lists
type: qa
step: 4
---
## Q
**LC 1669 合并两个链表**｜追问

面试官接着问：（1）要把被删下来的那一段也返回，怎么做？（2）`a` 可以等于 `0`（删头）怎么办？（3）不允许改动原链表呢？

## A
1. **取出被删段。** 在下标 `b` 处断开，保存被删段的头尾：

```python
def cut_segment(list1: ListNode, a: int, b: int) -> tuple[ListNode | None, ListNode | None]:
    dummy = ListNode(0, list1)
    before = dummy
    for _ in range(a):                          # before：下标 a - 1
        before = before.next
    last = before
    for _ in range(b - a + 1):                  # last：下标 b，被删段的最后一个节点
        last = last.next
    removed, rest = before.next, last.next      # 被删段的头，以及它后面剩下的部分
    last.next = None                            # 断开：被删段自成一条链
    before.next = rest                          # 剩下的部分接回去
    return dummy.next, removed
```

2. **`a = 0`。** 哑节点已经处理：`before` 就是哑节点本身，`before.next = list2` 之后 `dummy.next` 成了新头，返回 `dummy.next` 即可；没有哑节点就得单独判断头部。
3. **不改原链表。** 沿 `list1` 复制 `a` 个节点，再复制 `list2` 全部，再复制 `b + 1` 之后的节点，时间和空间都是 `O(n + m)`；面试里先问清是否允许原地改。

**Python 提醒**：`before = before.next` 走过头会得到 `None`，下一次 `.next` 抛 `AttributeError: 'NoneType' object has no attribute 'next'`；约束保证 `b < n - 1` 所以这里不会发生，但改题（如 `b` 可达末尾）时要加判断。
