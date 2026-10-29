---
id: tlc-swap-nodes-in-pairs-4-followup
node: b.swap-nodes-in-pairs
type: qa
step: 4
---
## Q
**LC 24 两两交换链表中的节点**｜追问

面试官接着问：（1）每 `k` 个一组翻转，不足 `k` 个的保持原样（LC 25）？（2）递归怎么写，有什么代价？（3）如果允许修改节点的值，最短的写法是什么，为什么还是不推荐？

## A
1. **K 个一组翻转**：先从 `group_prev` 往后数 `k` 个节点，不足就结束；足够时把这一组原地反转，再把组头组尾接回去。`k = 2` 就是两两交换。

```python
def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    dummy = ListNode(0, head)
    group_prev = dummy
    while True:
        kth = group_prev
        for _ in range(k):                 # 往后数 k 个节点，不够就结束
            kth = kth.next
            if not kth:
                return dummy.next
        group_next = kth.next
        prev, cur = group_next, group_prev.next
        while cur is not group_next:       # 组内反转，第一个节点反转后指向 group_next
            cur.next, prev, cur = prev, cur, cur.next
        tail = group_prev.next             # 翻转前的第一个节点，现在是这一组的尾巴
        group_prev.next = kth
        group_prev = tail
```

   `[1,2,3,4,5]`、`k = 2` → `[2, 1, 4, 3, 5]`，`k = 3` → `[3, 2, 1, 4, 5]`。`O(n)` 时间、`O(1)` 空间。
2. **递归**：`second = head.next; head.next = swap(second.next); second.next = head; return second`，三行写完，基例是 `head` 为空或只有一个节点。代价是栈深 `n / 2`；题目范围 `n <= 100` 没有问题，`10^5` 个节点会触发 `RecursionError`。
3. **允许改值**：遍历时每次 `a.val, b.val = b.val, a.val` 然后 `a = b.next`，不需要重连指针。但题目明确禁止；并且当节点带有其他数据、或者别处持有对这些节点的引用时，交换值会让引用指向“错误的元素”。

**Python 提醒**：元组赋值先求值右边，再按从左到右的顺序给目标赋值。`cur.next, prev, cur = prev, cur, cur.next` 可行，是因为第一个目标 `cur.next` 在 `cur` 被改写之前就完成了赋值；把 `cur` 放在第一位，后面的 `cur.next` 就会指向新节点，出错。链表节点没有定义 `__eq__`，比较两个节点用 `is`。
