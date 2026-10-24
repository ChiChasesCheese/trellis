---
id: tlc-flatten-a-multilevel-doubly-linked-list-4-followup
node: a.flatten-a-multilevel-doubly-linked-list
type: qa
step: 4
---
## Q
**LC 430 扁平化多级双向链表**｜追问

面试官接着问：（1）能不能用递归写？有什么风险？（2）不用「找尾巴」这一步，换成显式栈怎么做？（3）展平之后还要能还原成原来的多级结构，怎么办？

## A
1. **递归**：`dfs(node)` 展平以 `node` 开头的这一层并返回展平后的尾节点，遇到 `child` 时递归、再把子链表接进来。写法直观，但递归深度等于嵌套层数；嵌套 1000 层时 Python 会抛 `RecursionError`，迭代版没有这个风险。
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

**Python 提醒**：默认递归上限是 `1000`（`sys.getrecursionlimit()`）。用 `sys.setrecursionlimit` 调高只是把崩溃推迟到解释器栈溢出，面试里更好的答案是改成迭代。
