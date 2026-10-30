---
id: tlc-flatten-a-multilevel-doubly-linked-list-2-code
node: p4.flatten-a-multilevel-doubly-linked-list
type: qa
step: 2
---
## Q
**LC 430 扁平化多级双向链表**｜写出 Python 实现

多级双向链表的节点有 `val`、`prev`、`next`、`child`，`child` 指向一条可继续嵌套的子链表。原地扁平化为单层双向链表：子链表放在 `curr` 与 `curr.next` 之间，所有 `child` 置空，返回头节点。节点数不超过 `1000`，`1 <= Node.val <= 10^5`，可能为空。

## A
**思路。** `dfs(node)` 展平以 `node` 开头的这一层，返回展平后的尾节点。沿 `next` 往后走：先记下原后继 `nxt`；遇到 `child` 就递归展平子链表、拿到它的尾巴 `child_tail`，再让 `node.next` 指向子链表头，`child_tail.next` 接回 `nxt`，清空 `child`，这一段的尾巴变成 `child_tail`。

```python
def flatten(head: 'Node | None') -> 'Node | None':
    def dfs(node: Node) -> Node:              # 展平以 node 开头的这一层，返回展平后的尾节点
        tail = node
        while node:
            nxt = node.next                   # 先记下原后继：下面要改 node.next
            tail = node
            if node.child:
                child_tail = dfs(node.child)  # 子链表先展平，拿到它的尾巴
                node.next = node.child        # 子链表整段插到 node 和 nxt 之间
                node.child.prev = node
                child_tail.next = nxt
                if nxt:
                    nxt.prev = child_tail
                node.child = None             # 子指针必须清空
                tail = child_tail             # 这一段的尾巴变成子链表的尾巴
            node = nxt
        return tail

    if head:
        dfs(head)
    return head
```

运行：示例 1（`1-2-3-4-5-6`，`3` 带 `7-8-9-10`，`8` 带 `11-12`）→ `[1, 2, 3, 7, 8, 11, 12, 9, 10, 4, 5, 6]`；示例 2（`1-2`，`1` 带 `3`）→ `[1, 3, 2]`；空链表 → `None`；嵌套 `900` 层、每层一个节点 → 展平后 `900` 个节点，`prev` 链一致。

**复杂度。** 时间 `O(n)`：每个节点只被访问一次；空间 `O(d)`：递归栈深度等于嵌套层数 `d`，最坏 `O(n)`。

**写法要点。** 函数返回 `head` 本身，因为头节点不会变（只会在它后面插入）；注解写成字符串 `'Node | None'`，因为 `Node` 由判题环境定义；内层 `dfs` 返回尾节点，父层靠它一步接好，不必再沿 `next` 去找尾巴；`nxt = node.next` 必须在改指针之前保存；`if nxt` 守住末尾节点带 `child` 的情况，这时子链表尾巴的 `next` 本来就是 `None`。嵌套 `1000` 层会超过 CPython 默认递归上限（约 `1000`），抛 `RecursionError`，不递归的写法见追问卡。
