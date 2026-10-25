---
id: tlc-swap-nodes-in-pairs-2-code
node: b.swap-nodes-in-pairs
type: qa
step: 2
---
## Q
**LC 24 两两交换链表中的节点**｜写出 Python 实现

单链表的头节点 `head`（节点数 `0..100`，`0 <= Node.val <= 100`，节点类型是 `ListNode`，有 `val` 和 `next`）。两两交换相邻节点并返回新的头节点，只能交换节点本身，不能修改 `val`。

## A
**思路。** 哑节点指向头节点，`prev` 从哑节点开始。只要 `prev` 后面还有两个节点 `a`、`b`，就用元组赋值把 `prev → a → b → rest` 改成 `prev → b → a → rest`，再让 `prev = a`。最后返回 `dummy.next`。

```python
def swap_pairs(head: ListNode | None) -> ListNode | None:
    dummy = ListNode(0, head)              # 哑节点：让头节点也有“前一个节点”
    prev = dummy
    while prev.next and prev.next.next:
        a, b = prev.next, prev.next.next   # 要交换的一对：prev -> a -> b -> rest
        prev.next, a.next, b.next = b, b.next, a   # 右边先整体求值，再依次赋值：prev -> b -> a -> rest
        prev = a                           # a 现在是这一对的尾巴，下一对紧跟在它后面
    return dummy.next
```

运行：`[1,2,3,4]` → `[2, 1, 4, 3]`，`[]` → `[]`，`[1]` → `[1]`，`[1,2,3]` → `[2, 1, 3]`，`[1,2]` → `[2, 1]`；节点对象保持不变，只改了指针；`10^5` 个节点的链表同样能处理。

**复杂度。** 时间 `O(n)`：每对节点常数次指针操作；空间 `O(1)`。

**写法要点。** 元组赋值 `prev.next, a.next, b.next = b, b.next, a` 的右边三项在赋值之前已经全部求值，所以 `b.next` 取到的是旧值（后续链表的入口），不需要临时变量；三个赋值目标分别只依赖 `prev`、`a`、`b` 这三个名字，不会因为前一个赋值而改变含义。循环条件 `prev.next and prev.next.next` 利用短路，先判断前者再访问后者，不会对 `None` 取属性。
