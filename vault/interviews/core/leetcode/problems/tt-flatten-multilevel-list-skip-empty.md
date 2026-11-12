---
slug: tt-flatten-multilevel-list-skip-empty
---
## Q
**展平多级链表（值为空的嵌套节点要排除）**｜Medium

多级双向链表节点有 `val`、`prev`、`next`、`child`，子链表插在该节点和它原后继之间。展平成单层双向链表，`val` 为 `None` 的「入口」节点不进结果但它的 `child` 仍要展开，所有 `child` 置空，返回新头（没有有值节点返回 `None`）。

## A
**一句话。** 先递归按先序（当前、`child`、`next`）收集所有节点，再线性重连，跳过 `val` 为 `None` 的节点。

```python
def flatten_skip_empty(head):
    order = []

    def collect(node):
        while node:               # 沿 next 循环，只有 child 递归
            order.append(node)
            collect(node.child)   # 子链表先于后继
            node = node.next

    collect(head)
    new_head = tail = None
    for node in order:
        node.child = None
        if node.val is None:      # 入口节点不进结果
            continue
        node.prev, node.next = tail, None
        if tail:
            tail.next = node
        else:
            new_head = node
        tail = node
    return new_head
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 空节点连同子链表一起丢掉：`1 - ∅ - 3` 带 `7 - 8` 只遍历有值节点得 `[1,3]`，应为 `[1,7,8,3]`。
- 头是空节点时仍返回原 `head`：`∅ - 2` 要返回第一个有值的节点。
- 重连时不重设 `prev`：它还指着被跳过的空节点。
- 用 `not node.val` 判空：合法值 `0` 会被一起删掉，要用 `is None`。

**追问。**
- 嵌套很深怕递归爆栈？：用显式栈收集先序，先压 `next` 再压 `child`，重连部分不变。
- 要 `O(1)` 额外空间？：先按 LC 430 把各层拼成一条链，再扫一遍摘掉 `val` 为 `None` 的节点。

**同模式。** LC 430 扁平化多级双向链表、LC 341 扁平化嵌套列表迭代器、LC 114 二叉树展开为链表、LC 138 随机链表的复制
