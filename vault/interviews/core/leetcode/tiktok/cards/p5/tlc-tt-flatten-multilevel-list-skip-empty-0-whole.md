---
id: tlc-tt-flatten-multilevel-list-skip-empty-0-whole
node: p5.tt-flatten-multilevel-list-skip-empty
type: qa
---
## Q
**展平多级链表（值为空的嵌套节点要排除）**｜Medium · 近一年被问：美国 1 次、国内 0 次 · 最近 2026-07-18（面试记录）

多级双向链表的每个节点有 `val`、`prev`、`next`、`child`；`child` 指向一条可继续嵌套的子链表，子链表放在该节点之后、它原来的后继之前。把它展平成单层双向链表，变化是：作为「嵌套入口」的节点自己的 `val` 为 `None`（空），它不能出现在结果里，但它的 `child` 仍要展开。所有保留节点的 `child` 置空，`prev`/`next` 重新连好，返回新链表的头；没有任何有值节点时返回 `None`。节点数不超过 `1000`。例：第一层 `1 - ∅ - 3`，`∅` 的子链表是 `7 - 8` → `[1,7,8,3]`；`7` 再带子链表 `9` → `[1,7,9,8,3]`；第一层 `∅ - 2`，`∅` 的子链表是 `5 - ∅` → `[5,2]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把「展开」和「过滤」分开：先用显式栈按先序（当前 → `child` → `next`）收集所有节点，包括空节点；再按这个顺序线性地重连，跳过 `val` 为 `None` 的节点，其余节点依次接成新链并清空 `child`。`O(n)` 时间，`O(n)` 空间。

**识别。** 这是 LC 430 的变体：展开顺序不变，仍是先序；新增的只是一个输出过滤条件。空节点要「不输出、但继续展开它的子链表」，说明遍历和输出是两件事。

**推导。** 直接在 LC 430 的原地拼接里一边展开一边摘除空节点，要同时处理头部是空节点、连续空节点、空节点带 `child` 等多种指针情形，容易出错 → 浪费：把拼接和删除交织在一起，每一种情形都要单独验证 `prev`/`next` → 洞察：先得到不含任何指针改动的先序序列（用栈遍历，只读），再对序列做一次顺序扫描：有值的节点依次连成新链，`prev`、`next`、`child` 都在这一步重设。每个节点只处理两次。

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

运行：`1 - ∅ - 3`，`∅` 带 `7 - 8` → `[1, 7, 8, 3]`；再让 `7` 带 `9` → `[1, 7, 9, 8, 3]`；`∅ - 2`，`∅` 带 `5 - ∅` → `[5, 2]`；单个空节点 → `None`；空链表 → `None`。

**复杂度。** 时间 `O(n)`；空间 `O(n)`（`order` 与栈）。

**易错点。**
- 把空节点连同它的子链表一起丢掉：`1 - ∅ - 3` 带 `7 - 8`，只遍历有值节点会得到 `[1, 3]`，正确是 `[1, 7, 8, 3]`。
- 头节点是空节点时仍返回原来的 `head`：`∅ - 2` 的返回值要是第一个有值的节点（`5`），不是 `head`。
- 重连时不重设 `prev`：新链里相邻节点之间原来隔着空节点，`prev` 还指着被跳过的节点，从尾往头遍历会走到不该出现的节点。

**追问。**
- 只要值的列表、不改指针：写成生成器，先序遍历时对有值节点 `yield node.val`。
- 要求 `O(1)` 额外空间：先用 LC 430 的拼接把所有层接到一条链上，再扫一遍摘掉 `val` 为 `None` 的节点。
- 判断「空」要用 `val is None`，不能用 `not val`，否则合法的值 `0` 会被一起删除。

**同模式。** LC 430 扁平化多级双向链表、LC 341 扁平化嵌套列表迭代器、LC 114 二叉树展开为链表、LC 138 随机链表的复制。
