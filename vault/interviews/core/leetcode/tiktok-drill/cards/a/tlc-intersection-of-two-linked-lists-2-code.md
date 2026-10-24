---
id: tlc-intersection-of-two-linked-lists-2-code
node: a.intersection-of-two-linked-lists
type: qa
step: 2
---
## Q
**LC 160 相交链表**｜写出 Python 实现

两个无环单链表的头节点 `head_a`、`head_b`（节点数各在 `[1, 3 * 10^4]`）。返回两条链表相交的起始节点（同一个节点对象），不相交则返回 `None`。要求 `O(m + n)` 时间、`O(1)` 额外空间，且不能改变链表结构。

## A
**思路。** 两个指针 `a`、`b` 从各自表头出发。`a` 走到 `None` 之后改从 `head_b` 开始，`b` 走到 `None` 之后改从 `head_a` 开始。两者路程相同，相交时一定在交点相遇；不相交时一起走到 `None`，`a is b` 也成立，退出循环并返回 `None`。

```python
def get_intersection_node(head_a: ListNode | None, head_b: ListNode | None) -> ListNode | None:
    a, b = head_a, head_b
    while a is not b:                   # 比的是节点本身（地址），不是值
        a = a.next if a else head_b     # 走到头就换到另一条链表的表头
        b = b.next if b else head_a
    return a                            # 相交节点；不相交时 a、b 同时为 None
```

运行：`[4,1,8,4,5]` 与 `[5,6,1,8,4,5]`（共享后三个节点）→ 值为 `8` 的节点，`[1,9,1,2,4]` 与 `[3,2,4]` → 值为 `2` 的节点，`[2,6,4]` 与 `[1,5]` → `None`，两条等长且不相交的链表 → `None`。

**复杂度。** 时间 `O(m + n)`：每个指针最多走 `m + n` 步；空间 `O(1)`。

**写法要点。** `while a is not b` 用身份比较，节点类没有重写 `__eq__`，用 `!=` 也一样，但 `is not` 明确表达「同一个对象」；`a.next if a else head_b` 用条件表达式把「到头换表」写成一行，条件是 `a` 本身为 `None`（已经越过末尾），而不是 `a.next is None`；循环不需要单独处理「不相交」，因为最后一步两者同为 `None`，`None is None` 为真。
