---
id: tlc-reorder-list-4-followup
node: b.reorder-list
type: qa
step: 4
---
## Q
**LC 143 重排链表**｜追问

面试官接着问：（1）允许 `O(n)` 额外空间，有没有更短的写法？（2）用递归能不能做？有什么风险？（3）把同样的「找中点 + 翻转」用来判断**回文链表**（LC 234）？

## A
1. **用 `O(n)` 空间**：把节点收集进列表 `nodes`，左右下标交替连接，最后把末尾节点的 `next` 置 `None`，代码更短，不容易出错，但不满足进阶要求的原地。用 `deque` 交替 `popleft`、`pop` 也行。

```python
def reorder_list_nodes(head: ListNode | None) -> None:
    nodes: list[ListNode] = []
    while head:
        nodes.append(head)
        head = head.next
    lo, hi = 0, len(nodes) - 1
    while lo < hi:
        nodes[lo].next = nodes[hi]
        lo += 1
        if lo == hi:
            break
        nodes[hi].next = nodes[lo]
        hi -= 1
    if nodes:
        nodes[lo].next = None
```

2. **递归**：递归到链表末尾，回溯时拿「当前尾部」去接前面的节点，写法很巧，但递归深度等于链表长度；`5 * 10^4` 远超 Python 默认递归上限 1000，需要 `sys.setrecursionlimit`，且栈空间 `O(n)`。
3. **回文链表（LC 234）**：找中点、翻转后半段，然后两个指针同时向后比较值。要恢复链表的原样，比较完再翻转一次后半段接回去。空间 `O(1)`。

**Python 提醒**：`sys.setrecursionlimit` 只改解释器的计数上限，真正的 C 栈仍然有限，递归深度几万层可能直接段错误。链表题优先写迭代版。
