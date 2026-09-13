---
id: leetcode-q-convert-binary-search-tree-to-sorted-doubly-linked-list-pattern
node: linked-list.doubly-linked-list
type: qa
anki: 1787175411334
tags: [lc::426, leetcode, pattern, recall]
---
## Q
BST 转排序双向链表：为什么用中序遍历收集节点，再统一连接，而不是边遍历边连接？

## A
中序遍历 BST 天然按升序访问节点，所以先用中序遍历把所有节点按顺序收集到列表 `lst` 中；之后用下标关系批量设置 `node.left = prev`、`node.right = next`（含首尾循环：`lst[(i+1)%n]` 和 `lst[i-1]`），一次性把链表变成循环双向链表。这样把「遍历顺序」和「指针连接」两个关注点分开，逻辑更清晰，避免在递归中同时维护 prev 指针状态。

**Evidence**

```
lst = []
def inorder(node):
    if node is None: return
    inorder(node.left)
    lst.append(node)
    inorder(node.right)
inorder(root)
n = len(lst)
for i in range(n):
    node = lst[i]
    node.left = lst[i-1]
    node.right = lst[(i+1) % n]
return lst[0] if n >= 1 else None
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F426%20-%20Convert%20Binary%20Search%20Tree%20to%20Sorted%20Doubly%20Linked%20List)
