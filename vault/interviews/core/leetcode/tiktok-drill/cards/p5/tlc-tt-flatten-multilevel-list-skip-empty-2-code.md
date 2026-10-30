---
id: tlc-tt-flatten-multilevel-list-skip-empty-2-code
node: p5.tt-flatten-multilevel-list-skip-empty
type: qa
step: 2
---
## Q
**展平多级链表（值为空的嵌套节点要排除）**｜写出 Python 实现

多级双向链表的节点有 `val`、`prev`、`next`、`child`（节点数不超过 `1000`）。展平成单层双向链表：子链表放在节点与其后继之间；`val` 为 `None` 的节点不出现在结果里，但它的 `child` 要展开；保留节点的 `child` 置空；返回新链表的头，没有有值节点时返回 `None`。

## A
**思路。** 第一步用递归做先序遍历（沿 `next` 循环，遇到 `child` 递归），把所有节点按「当前 → 子链表 → 后继」的顺序收进 `order`。第二步顺序扫描 `order`：空节点跳过，有值节点接到当前尾巴后面，同时重设 `prev`、`next`，并把 `child` 清空。

```python
def flatten_skip_empty(head: 'Node | None') -> 'Node | None':
    order: list[Node] = []                   # 先序：当前节点 -> 子链表 -> 后继

    def collect(node: Node | None) -> None:
        while node:                          # 沿 next 横着走；只有 child 才递归
            order.append(node)
            collect(node.child)              # 整条子链表（含更深层）先于后继
            node = node.next

    collect(head)
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

运行：`1 - ∅ - 3`，`∅` 带 `7 - 8` → `[1, 7, 8, 3]`；`7` 再带 `9` → `[1, 7, 9, 8, 3]`；`∅ - 2`，`∅` 带 `5 - ∅` → `[5, 2]`；`0 - ∅ - 3`（空节点没有子链表）→ `[0, 3]`；单个空节点 → `None`；空链表 → `None`；每个节点只有一个 `child` 的 `1000` 层嵌套 → `1000` 个节点（调大递归上限后；默认上限下抛 `RecursionError`）。

**复杂度。** 时间 `O(n)`；空间 `O(n)`（`order` 加深度等于嵌套层数的递归栈）。

**写法要点。** `collect` 里先 `append`、再递归 `child`、最后才走 `next`，就是先序；遍历阶段不改任何指针，所以 `node.next` 在走到它之前一直有效；`while node` 沿 `next` 循环，递归深度只取决于嵌套层数；`node.val is None` 判断空，不要写 `not node.val`（`0` 是合法的值）；`node.prev, node.next = tail, None` 一次重设，保证新链末尾的 `next` 为 `None`；`new_head` 在遇到第一个有值节点时才设置。
