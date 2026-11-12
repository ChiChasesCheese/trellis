---
slug: flatten-a-multilevel-doubly-linked-list
---
## Q
**LC 430 扁平化多级双向链表**｜Medium

双向链表的节点可能有 `child` 指向另一条双向链表（可嵌套）。把它扁平成单层双向链表，子链表插在该节点和它的后继之间。

## A
**一句话。** 递归展平：`dfs` 展平一层并返回尾节点，遇到 `child` 就把展平后的子链表整段插到当前节点和原后继之间。

```python
def flatten(head):
    def dfs(node):                 # 返回这一层的尾节点
        tail = node
        while node:
            nxt = node.next        # 先记原后继
            tail = node
            if node.child:
                ct = dfs(node.child)
                node.next = node.child
                node.child.prev = node
                ct.next = nxt
                if nxt:
                    nxt.prev = ct
                node.child = None
                tail = ct
            node = nxt
        return tail

    if head:
        dfs(head)
    return head
```

**复杂度。** 时间 `O(n)`，空间 `O(d)`（嵌套深度）。

**易错点。**
- 没先保存 `nxt`：改了 `node.next` 后原后继丢失，示例会少一大半节点。
- 漏掉 `node.child = None` 或 `child.prev = node`：前者违反题意，后者让倒着走出错。

**追问。**
- 嵌套 1000 层会怎样？：触到 CPython 递归上限，改用迭代：遇到 `child` 就找子链表尾，接上原后继。
- 能用显式栈吗？：遇到 `child` 先压 `cur.next`，走到末尾再弹出接回。

**同模式。** LC 114 二叉树展开为链表、LC 138 随机链表的复制、LC 341 扁平化嵌套列表迭代器
