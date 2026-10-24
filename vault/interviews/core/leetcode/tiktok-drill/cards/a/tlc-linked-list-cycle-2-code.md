---
id: tlc-linked-list-cycle-2-code
node: a.linked-list-cycle
type: qa
step: 2
---
## Q
**LC 141 环形链表**｜写出 Python 实现

链表头节点 `head`（节点数 `[0, 10^4]`，节点值可重复）。判断链表中是否存在环，要求 `O(1)` 额外空间。

## A
**思路。** 两个指针都从 `head` 出发。每轮 `slow` 走一步，`fast` 走两步，然后比较它们是否是同一个节点。`fast` 或 `fast.next` 为 `None` 说明走到了链表末尾，无环。

```python
def has_cycle(head: ListNode | None) -> bool:
    slow = fast = head
    while fast and fast.next:           # fast 走到头（None）说明无环
        slow = slow.next                # 慢指针一步
        fast = fast.next.next           # 快指针两步
        if slow is fast:                # 先走再比较：起点本来就相等
            return True
    return False
```

运行：`[3,2,0,-4]`（尾连下标 1）→ `True`，`[1,2]`（尾连下标 0）→ `True`，`[1]` → `False`，`[]` → `False`，`[1]` 自己连自己 → `True`，`10^4` 个节点、尾连下标 `5000` → `True`，`10^4` 个节点无环 → `False`。

**复杂度。** 时间 `O(n)`；空间 `O(1)`：两个指针。

**写法要点。** `slow = fast = head` 一行初始化两个指针；循环条件 `fast and fast.next` 同时保证 `fast.next.next` 可以安全求值，空链表和单节点也不需要特判；用 `is` 比较节点身份，不用 `==`，更明确，也避免节点类重写 `__eq__` 时出错；比较放在移动之后，否则起点相同会误判。`while` 里没有任何额外的数据结构，空间是严格 `O(1)`。
