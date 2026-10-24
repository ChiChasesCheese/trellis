---
id: tlc-patterns-linked-list-2-template
node: patterns.linked-list
type: qa
step: 2
---
## Q
**链表技巧（Linked List）｜模板：反转与合并**

写出迭代反转链表（LC 206）和用哑节点合并两个有序链表的模板。

## A
**反转**：三个角色 `prev`（已反转部分的头）、`head`（当前）、`head.next`（下一个，先保存）。

```python
def reverse_list(head: ListNode | None) -> ListNode | None:
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next   # 同时：翻转指针、前移 prev、前移 head
    return prev
```

运行：`[1,2,3,4,5]` → `[5,4,3,2,1]`；`[1,2]` → `[2,1]`；`None` → `None`。时间 `O(n)`，空间 `O(1)`。

**合并（哑节点 + 尾指针）**：

```python
def merge_two(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b                     # 剩下的整段直接接上
    return dummy.next
```

- 哑节点让「第一个节点」和「后面的节点」用同一段代码处理，不用单独判断头节点。
- `head.next, prev, head = prev, head, head.next`：右边先整体求值，左边从左到右赋值，所以 `head.next` 必须排在 `head` 之前。顺序错了（`head, head.next, prev = ...`）会把链表弄断。
- 合并时用 `<=` 保持稳定（相等时先取 `a`）。
- 递归版 `reverse(head.next)` 优雅，但深度 `O(n)`，链表超过 1000 个节点时会超过 Python 的默认递归上限（LC 25 的 `n` 可达 `5000`），面试里优先写迭代。
