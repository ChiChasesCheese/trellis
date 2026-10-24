---
id: tlc-flatten-a-multilevel-doubly-linked-list-2-code
node: a.flatten-a-multilevel-doubly-linked-list
type: qa
step: 2
---
## Q
**LC 430 扁平化多级双向链表**｜写出 Python 实现

多级双向链表的节点有 `val`、`prev`、`next`、`child`，`child` 指向一条可继续嵌套的子链表。原地扁平化为单层双向链表：子链表放在 `curr` 与 `curr.next` 之间，所有 `child` 置空，返回头节点。节点数不超过 `1000`，`1 <= Node.val <= 10^5`，可能为空。

## A
**思路。** 一个指针 `cur` 从头往后走。遇到 `cur.child`，先沿 `next` 找到子链表这一层的尾巴，把尾巴接上 `cur.next`，再让 `cur.next` 指向子链表的头并清空 `child`。`cur` 继续往后走时就会走进子链表，下一级的 `child` 在那里被同样处理。

```python
def flatten(head: 'Node | None') -> 'Node | None':
    cur = head
    while cur:
        if cur.child:
            tail = cur.child
            while tail.next:                   # 子链表这一层的尾巴（它的下一级还没展开，next 链只有这一层）
                tail = tail.next
            tail.next = cur.next               # 子链表的尾巴接上 cur 原来的后继
            if cur.next:
                cur.next.prev = tail
            cur.next = cur.child               # cur 直接指向子链表的头
            cur.child.prev = cur
            cur.child = None                   # 子指针必须清空
        cur = cur.next                         # 往后走：下一个就是刚接进来的子链表的头
    return head
```

运行：示例 1（`1-2-3-4-5-6`，`3` 带 `7-8-9-10`，`8` 带 `11-12`）→ `[1, 2, 3, 7, 8, 11, 12, 9, 10, 4, 5, 6]`；示例 2（`1-2`，`1` 带 `3`）→ `[1, 3, 2]`；空链表 → `None`；嵌套 1000 层、每层一个节点 → 展平后 1000 个节点，`prev` 链一致。

**复杂度。** 时间 `O(n)`：每个节点最多被「找尾巴」走一次、被主循环走一次；空间 `O(1)`。

**写法要点。** 函数返回 `head` 本身，因为头节点不会变（只会在它后面插入）；注解写成字符串 `'Node | None'`，因为 `Node` 由判题环境定义；`while tail.next` 停在最后一个节点，不是走出链表；`if cur.next` 守住末尾节点带 `child` 的情况，这时子链表尾巴的 `next` 本来就是 `None`。
