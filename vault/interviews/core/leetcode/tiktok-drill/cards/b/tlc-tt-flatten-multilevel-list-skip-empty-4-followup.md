---
id: tlc-tt-flatten-multilevel-list-skip-empty-4-followup
node: b.tt-flatten-multilevel-list-skip-empty
type: qa
step: 4
---
## Q
**展平多级链表（值为空的嵌套节点要排除）**｜追问

面试官接着问：（1）只要值的列表，不要求改指针；（2）额外空间要 `O(1)`；（3）如果「空」的判断是 `not val`，会出什么问题？

## A
1. **只要值的列表**：写成生成器，先序遍历，有值节点 `yield node.val`，不需要重连，也不需要 `order` 列表；调用方可以惰性消费。
2. **`O(1)` 额外空间**：第一步用 LC 430 的拼接（找子链表尾巴并接上）把所有层并成一条链；第二步扫描一遍，把 `val` 为 `None` 的节点摘掉。

```python
def flatten_skip_empty_o1(head: 'Node | None') -> 'Node | None':
    cur = head
    while cur:                                   # 第一步：与 LC 430 相同的拼接
        if cur.child:
            tail = cur.child
            while tail.next:
                tail = tail.next
            tail.next = cur.next
            if cur.next:
                cur.next.prev = tail
            cur.next = cur.child
            cur.child.prev = cur
            cur.child = None
        cur = cur.next
    while head and head.val is None:             # 头部连续的空节点直接跳过
        head = head.next
    if head:
        head.prev = None
    cur = head
    while cur:                                   # 第二步：摘掉后面的空节点
        nxt = cur.next
        while nxt and nxt.val is None:
            nxt = nxt.next
        cur.next = nxt
        if nxt:
            nxt.prev = cur
        cur = nxt
    return head
```

`1 - ∅ - 3`，`∅` 带 `7 - 8` → `[1, 7, 8, 3]`，与栈版一致。
3. **`not val` 的问题**：`0` 也是假值。`0 - ∅ - 3` 若用 `not node.val` 判空，值为 `0` 的节点会被一起删掉，得到 `[3]`，正确是 `[0, 3]`。判断「没有值」要用 `val is None`。

**Python 提醒**：`is None` 比较的是身份，不受 `__eq__` 重载影响；`not x`、`if x` 把 `0`、`""`、`[]`、`None` 全部当假，在「值本身可以是 `0`」的场合是常见的隐蔽错误。
