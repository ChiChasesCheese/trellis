---
id: tlc-flatten-a-multilevel-doubly-linked-list-4-followup
node: p4.flatten-a-multilevel-doubly-linked-list
type: qa
step: 4
---
## Q
**LC 430 扁平化多级双向链表**｜追问

面试官接着问：（1）嵌套很深，递归超过限制怎么办，能不能 `O(1)` 额外空间？（2）不找尾巴，换成显式栈怎么做？（3）展平之后还要能还原成原来的多级结构，怎么办？

## A
1. **`O(1)` 额外空间的迭代**：单指针 `cur` 往后走；遇到 `child`，沿 `next` 找到子链表这一层的尾巴（它的下一级还没展开，`next` 链只含这一层），尾巴接上 `cur.next`，再让 `cur.next` 指向子链表头；`cur` 继续往后走时就走进了子链表，嵌套逐层展开。每个节点最多被找尾巴和主循环各走一次，`O(n)` 时间，没有递归深度问题。顺序不能错：先把尾巴接到 `cur.next`，再改 `cur.next`。

```python
def flatten_splice(head: 'Node | None') -> 'Node | None':
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

2. **显式栈**：遇到 `child` 先把 `cur.next` 压栈，再接子链表；走到链表末尾时弹栈接回。`O(n)` 时间，`O(嵌套深度)` 空间。

```python
def flatten_stack(head: 'Node | None') -> 'Node | None':
    stack: list[Node] = []
    cur = head
    while cur:
        if cur.child:
            if cur.next:
                stack.append(cur.next)         # 暂存被挤到后面的后继
            cur.next = cur.child
            cur.next.prev = cur
            cur.child = None
        if cur.next is None and stack:         # 这一层走完了，回到外层的后继
            cur.next = stack.pop()
            cur.next.prev = cur
        cur = cur.next
    return head
```

3. **还原**：展平后层次信息丢失。要还原，展平时就得另存每个子链表的头与长度（或在节点上多存一个层级标记），还原时按长度把链表切开，再把 `child` 指回去。

**Python 提醒**：默认递归上限是 `1000`（`sys.getrecursionlimit()`）。用 `sys.setrecursionlimit` 调高只是把崩溃推迟到解释器栈溢出；嵌套可能很深时，上面的迭代写法更稳。
