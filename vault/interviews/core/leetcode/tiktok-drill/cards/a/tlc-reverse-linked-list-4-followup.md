---
id: tlc-reverse-linked-list-4-followup
node: a.reverse-linked-list
type: qa
step: 4
---
## Q
**LC 206 反转链表**｜追问

面试官接着问：（1）用递归写一遍，它的空间和风险是什么？（2）只反转链表的第 `m` 到第 `n` 个节点？（3）不允许修改链表，只想按逆序输出？

## A
1. **递归**：假设 `reverse(head.next)` 已经把后面整段翻好并返回新头，那么原来的 `head.next` 现在是翻好后那段的尾，让它指回 `head`，再把 `head.next` 置空。
```python
def reverse_list_rec(head: ListNode | None) -> ListNode | None:
    if head is None or head.next is None:
        return head
    new_head = reverse_list_rec(head.next)    # 先把后面整段翻好
    head.next.next = head                     # 原来的后继现在指回我
    head.next = None                          # 我变成新的尾巴
    return new_head
```
   空间 `O(n)` 的调用栈。题目节点数可达 `5000`，超过 Python 默认递归上限约 `1000`，`5000` 个节点的链表会触发 `RecursionError`；迭代版没有这个问题。
2. **区间 `[m, n]`**（LC 92）：用哑节点（dummy）指向头，走到第 `m - 1` 个节点 `pre`；在 `pre` 后面做 `n - m` 次「头插」：每次把 `pre.next` 后面的那个节点摘出来插到 `pre` 后面。`m = 1` 时不需要特判。
3. **只读逆序输出**：不改指针，把值压进栈（Python 的 `list`），再弹出；或递归到链尾再在回溯时输出。空间 `O(n)`，代价是不能原地。

**Python 提醒**：元组赋值先对右边整体求值、再从左到右赋值，所以 `head.next, prev, head = prev, head, head.next` 成立；但如果左边把 `head` 放在 `head.next` 前面，`head.next` 会按已被修改的 `head` 去赋值。递归深度可用 `sys.setrecursionlimit` 放大，但那只是掩盖问题，链表本质上适合迭代。
