---
id: tlc-delete-node-in-a-linked-list-2-code
node: a.delete-node-in-a-linked-list
type: qa
step: 2
---
## Q
**LC 237 删除链表中的节点**｜写出 Python 实现

单链表（`2..1000` 个节点，值互不相同，`-1000..1000`），只给要删除的非尾节点 `node`，没有 `head`，删除它，使链表的值序列中不再有它的值。要求 `O(1)`。

## A
**思路。** 后继一定存在。把后继的值搬到 `node`，再让 `node.next` 跳过后继，效果等同于删掉了 `node` 的值。

```python
def delete_node(node: ListNode) -> None:
    nxt = node.next                          # node 不是尾节点，nxt 一定存在
    node.val, node.next = nxt.val, nxt.next  # 把后继的值搬过来，再跳过后继
```

运行：`[4,5,1,9]` 删 `5` → `[4,1,9]`；删 `1` → `[4,5,9]`；`[4,5]` 删 `4` → `[5]`。

**复杂度。** 时间 `O(1)`：两次赋值；空间 `O(1)`。

**写法要点。** 元组赋值 `node.val, node.next = nxt.val, nxt.next` 先求出右边两个值再赋给左边，两个字段同时更新；先用 `nxt` 存住后继，读起来一目了然；函数返回 `None`，改的是对象本身而不是参数名；`ListNode` 沿用平台给的节点类。
