---
id: tlc-tt-flatten-multilevel-list-skip-empty-2-code
node: b.tt-flatten-multilevel-list-skip-empty
type: qa
step: 2
---
## Q
**展平多级链表（值为空的嵌套节点要排除）**｜写出 Python 实现

多级双向链表的节点有 `val`、`prev`、`next`、`child`（节点数不超过 `1000`）。展平成单层双向链表：子链表放在节点与其后继之间；`val` 为 `None` 的节点不出现在结果里，但它的 `child` 要展开；保留节点的 `child` 置空；返回新链表的头，没有有值节点时返回 `None`。

## A
**思路。** 第一步用栈做先序遍历，把所有节点按「当前 → 子链表 → 后继」的顺序收进 `order`。第二步顺序扫描 `order`：空节点跳过，有值节点接到当前尾巴后面，同时重设 `prev`、`next`，并把 `child` 清空。

```python
def flatten_skip_empty(head: 'Node | None') -> 'Node | None':
    order: list[Node] = []                   # 先序：当前节点 -> 子链表 -> 后继
    stack: list[Node] = [head] if head else []
    while stack:
        node = stack.pop()
        order.append(node)
        if node.next:
            stack.append(node.next)          # 后压后继，先压不到：子链表先出栈
        if node.child:
            stack.append(node.child)
    new_head: Node | None = None
    tail: Node | None = None
    for node in order:
        node.child = None                    # 所有 child 清空
        if node.val is None:                 # 值为空的“入口”节点：不进结果，但它的 child 已经在 order 里被展开
            continue
        node.prev, node.next = tail, None
        if tail:
            tail.next = node
        else:
            new_head = node
        tail = node
    return new_head
```

运行：`1 - ∅ - 3`，`∅` 带 `7 - 8` → `[1, 7, 8, 3]`；`7` 再带 `9` → `[1, 7, 9, 8, 3]`；`∅ - 2`，`∅` 带 `5 - ∅` → `[5, 2]`；`0 - ∅ - 3`（空节点没有子链表）→ `[0, 3]`；单个空节点 → `None`；空链表 → `None`。

**复杂度。** 时间 `O(n)`；空间 `O(n)`。

**写法要点。** 栈里先压 `next` 再压 `child`，后进先出使子链表先于后继出栈，就是先序；遍历阶段不改任何指针，所以栈里的 `node.next` 在被弹出前一直有效；`node.val is None` 判断空，不要写 `not node.val`（`0` 是合法的值）；`node.prev, node.next = tail, None` 一次重设，保证新链末尾的 `next` 为 `None`；`new_head` 在遇到第一个有值节点时才设置。
