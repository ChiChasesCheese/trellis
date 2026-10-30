---
id: tlc-flatten-a-multilevel-doubly-linked-list-0-whole
node: p4.flatten-a-multilevel-doubly-linked-list
type: qa
---
## Q
**LC 430 扁平化多级双向链表**｜Medium · 近一年被问：美国 1 次、国内 0 次 · CodeTop 国内累计 1 次 · 最近 2026-07-18（美国面试记录）

给一个双向链表，每个节点有 `val`、`prev`、`next`，还有一个 `child` 指针；`child` 可以指向另一条独立的双向链表，子链表的节点同样可以有自己的 `child`，层层嵌套。把整个结构扁平化成单层双向链表：带子链表的节点 `curr` 的子链表必须出现在 `curr` 之后、`curr.next` 之前；所有 `child` 置为 `null`；返回扁平链表的头。节点数不超过 `1000`，`1 <= Node.val <= 10^5`，输入可能是空链表。例：第一层 `1-2-3-4-5-6`，`3` 的子链表是 `7-8-9-10`，`8` 的子链表是 `11-12` → `[1,2,3,7,8,11,12,9,10,4,5,6]`；`1-2` 里 `1` 的子链表是 `3` → `[1,3,2]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 递归展平：`dfs(node)` 展平以 `node` 开头的这一层并返回尾节点；沿 `next` 往后走，遇到 `child` 就先递归展平子链表，把它整段插到当前节点和原后继之间，尾巴变成子链表的尾巴。`O(n)` 时间，`O(嵌套深度)` 空间。

**识别。** 「子链表夹在 `curr` 与 `curr.next` 之间」就是先序顺序（当前 → `child` → `next`），`child` 指向的是一条结构相同的子问题，天然递归；「返回头、所有 `child` 置空」说明要原地改指针而不是新建节点；节点数 `<= 1000`，`O(n)` 绰绰有余。

**推导。** 暴力：递归先序把所有节点收进数组，再按顺序重连 `prev`/`next`，`O(n)` 时间、`O(n)` 空间 → 浪费：数组只是为了记住「子链表走完后该接谁」，而答案就是 `node.next`，当场就知道 → 洞察：让子问题返回自己展平后的尾巴，父层就能一步接好：`node.next` 指向子链表头，尾巴接回原后继 `nxt`，一共改 4 个指针 → 每个节点只被访问一次，`O(n)`。

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

运行：示例 1 → `[1, 2, 3, 7, 8, 11, 12, 9, 10, 4, 5, 6]`，示例 2 → `[1, 3, 2]`，空链表 → `None`；每个节点只带一个 `child`、嵌套 `900` 层 → 展平后 `900` 个节点，`prev` 全部一致。

**复杂度。** 时间 `O(n)`：每个节点只被访问一次；空间 `O(d)`，`d` 是嵌套层数（递归栈），最坏 `O(n)`。

**易错点。**
- 必须先记下原后继 `nxt = node.next`，再改 `node.next`。若先写 `node.next = node.child` 而没有保存 `nxt`，原后继丢失，示例 1 会得到 `[1,2,3,7,8,11,12]`（少了 `9,10,4,5,6`）。
- 漏掉 `node.child = None` 或 `node.child.prev = node`：前者违反题意，后者让从尾往头走的结果出错。
- 深度：嵌套层数最坏等于节点数，题目上限 `1000`，一条每层只有一个节点的嵌套链（`1000` 层）会超过 CPython 默认递归上限（约 `1000`）而抛 `RecursionError`（`900` 层没事）；要么 `sys.setrecursionlimit` 调高，要么用不递归的写法（见追问）。

**追问。**
- `O(1)` 额外空间的迭代写法：单指针往后走，遇到 `child` 就沿 `next` 找到子链表这一层的尾巴，接上 `cur.next`，再把 `cur.next` 指向子链表头；走到刚接进来的子链表头时，嵌套自动展开，没有递归深度问题。
- 用显式栈：遇到 `child` 先压入 `cur.next`，走到末尾再弹出接回，`O(n)` 时间、`O(嵌套深度)` 空间。
- 展平的逆操作：展平丢掉了层次，必须在展平时另存每个子链表的头和长度。

**同模式。** LC 114 二叉树展开为链表、LC 138 随机链表的复制、LC 341 扁平化嵌套列表迭代器、LC 426 将二叉搜索树转化为排序的双向链表。
