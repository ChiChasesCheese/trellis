---
id: tlc-reverse-nodes-in-k-group-4-followup
node: a.reverse-nodes-in-k-group
type: qa
step: 4
---
## Q
**LC 25 K 个一组翻转链表**｜追问

面试官接着问：（1）不足 `k` 个的那一组也要翻转（或从尾部开始分组）？（2）只反转第 `m` 到第 `n` 个节点（LC 92）？（3）能用栈写得更简单一点吗，代价是什么？

## A
1. **不足的一组也翻**：把「数 `k` 个，数不够就返回」改成「数到末尾为止」，对数到的那几个节点照样翻。`[1,2,3,4,5]`、`k = 3` 得到 `[3,2,1,5,4]`。**从尾部开始分组**（不足的留在头部）：先求链表长度 `n`，令头部的 `n % k` 个节点保持不动，再对剩下的做 K 组反转；或者先整体反转，按上面的做法做一遍，再整体反转回来。
2. **区间反转**（LC 92）：哑节点后走 `m - 1` 步得到 `pre`，在 `pre` 后面做 `n - m` 次头插：每次取出 `pre.next` 后面那个节点，插到 `pre` 后面。只有一组，不需要数 `k`。
3. **栈版本**：每组把 `k` 个节点压入 `list`，够 `k` 个就倒着弹出并依次连接，不足则不动。代码直观，`O(k)` 额外空间，不满足进阶的 `O(1)`；链表本身的节点复用，不创建新节点。
```python
def reverse_k_group_stack(head: ListNode | None, k: int) -> ListNode | None:
    dummy = ListNode(0)
    tail = dummy
    while head:
        group: list[ListNode] = []
        node = head
        while node and len(group) < k:
            group.append(node)
            node = node.next
        if len(group) < k:                    # 不足一组：原样接上
            tail.next = head
            break
        for n in reversed(group):
            tail.next = n
            tail = n
        tail.next = node                      # 先接下一组的头，避免成环
        head = node
    return dummy.next
```
   `[1,2,3,4,5]`、`k = 2` 得到 `[2, 1, 4, 3, 5]`。

**Python 提醒**：反转后组尾的 `next` 仍然指着旧的后继，会形成环或带出多余的节点，必须及时把它改到下一组（或 `None`）。链表题用 `is` 比较节点身份，不要用 `==`；`ListNode` 没有定义 `__eq__` 时二者等价，但养成习惯可以避免之后给节点加了比较方法而出错。
