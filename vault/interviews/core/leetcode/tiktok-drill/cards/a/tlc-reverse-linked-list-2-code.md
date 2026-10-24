---
id: tlc-reverse-linked-list-2-code
node: a.reverse-linked-list
type: qa
step: 2
---
## Q
**LC 206 反转链表**｜写出 Python 实现

单链表头节点 `head`（节点数 `0` 到 `5000`，值在 `[-5000, 5000]`），反转它并返回新的头节点。用迭代完成，额外空间 `O(1)`。

## A
**思路。** `prev` 指向已反转部分的头（初始 `None`），`cur` 指向待处理的节点。每轮先存下 `cur.next`，再让 `cur.next = prev` 把这条边掉头，最后 `prev`、`cur` 一起前进。循环结束时 `prev` 就是新头。

```python
def reverse_list(head: ListNode | None) -> ListNode | None:
    prev: ListNode | None = None
    cur = head
    while cur:
        nxt = cur.next            # 先存下后继，否则改完指针就丢了
        cur.next = prev           # 翻转这一条边
        prev, cur = cur, nxt      # 两个指针一起前进
    return prev
```

运行：`[1,2,3,4,5]` → `[5, 4, 3, 2, 1]`，`[1,2]` → `[2, 1]`，`[]` → `[]`，`[7]` → `[7]`；`5000` 个节点同样直接通过。

**复杂度。** 时间 `O(n)`：每个节点处理一次；空间 `O(1)`：三个指针。

**写法要点。** `prev: ListNode | None = None` 给变量加类型标注，说明它可能为空；`while cur:` 用节点对象的真值判断（对象默认为真，`None` 为假），比 `cur is not None` 短；`prev, cur = cur, nxt` 元组赋值同时更新两个变量，不用中间量。显式写出 `nxt` 的三行版本比 `head.next, prev, head = prev, head, head.next` 的一行版本更适合面试：每步都能解释，赋值顺序也不会出错。
