---
id: tlc-sort-list-4-followup
node: b.sort-list
type: qa
step: 4
---
## Q
**LC 148 排序链表**｜追问

面试官接着问：（1）进阶要求**常数空间**，递归栈也不能有，怎么做？（2）为什么链表排序不用快速排序？（3）怎么保证排序是**稳定**的？

## A
1. **自底向上归并**：先数出长度 `n`。`size` 从 `1` 开始，每轮把链表依次切成长度 `size` 的小段，把相邻两段合并，并接到上一段合并结果的尾部；`size` 翻倍，直到 `size >= n`。需要一个 `cut(node, size)`：取 `node` 开头的 `size` 个节点，在那里断开，返回剩下部分的头。合并函数除了返回头，还要返回尾，下一段才能接上。没有递归，额外空间 `O(1)`，时间仍是 `O(n log n)`。

```python
def cut(node: ListNode | None, size: int) -> ListNode | None:
    while size > 1 and node:
        node = node.next
        size -= 1
    if not node:
        return None
    rest, node.next = node.next, None
    return rest
```

2. **为什么不用快排**：链表不能 `O(1)` 随机取基准，也没法像数组那样双向交换划分；基准选在端点时，有序输入会退化到 `O(n^2)`。归并排序的复杂度与输入分布无关，并且合并天然适合链表。
3. **稳定**：合并时相等的值先取左边那一段的节点（`a.val <= b.val`），左半段在原链表里本来就靠前，所以相同值的节点保持原来的先后顺序。把 `<=` 改成 `<` 就不稳定了。

**Python 提醒**：`sorted` 和 `list.sort` 是稳定的，要按节点值排序时必须给 `key=lambda n: n.val`，因为 `ListNode` 没有 `<`；直接 `sorted(nodes)` 会抛 `TypeError`。
