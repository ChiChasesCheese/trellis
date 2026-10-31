---
id: tlc-merge-two-sorted-lists-4-followup
node: b.merge-two-sorted-lists
type: qa
step: 4
---
## Q
**LC 21 合并两个有序链表**｜追问

面试官接着问：（1）写一个**递归**版本，它的风险是什么？（2）合并**去掉重复值**？（3）合并 `k` 个有序链表？

## A
1. **递归**：取较小的队头，它的 `next` 指向「对其余部分的合并结果」。代码只有几行，但递归深度等于 `m + n`，链表上万个节点就会超过 Python 默认的递归上限 1000；迭代版没有这个风险。

```python
def merge_rec(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    if not l1 or not l2:
        return l1 or l2
    if l1.val <= l2.val:
        l1.next = merge_rec(l1.next, l2)
        return l1
    l2.next = merge_rec(l1, l2.next)
    return l2
```

2. **去重**：接节点前比较它的值和 `tail.val`，相同就跳过这个节点（只前进、不接）。哑节点的值要取一个不可能出现的值（这里值域是 `[-100, 100]`，用 `ListNode(101)`），避免它和第一个真实节点误判相等。
3. **`k` 个链表（LC 23）**：反复调用本函数顺序合并是 `O(N · k)`；用最小堆是 `O(N log k)`；分治两两合并同样 `O(N log k)`，其中的合并步骤就是这个函数。

**Python 提醒**：写 `ListNode()` 不带参数要求类的构造函数给 `val`、`next` 设了默认值，LeetCode 的定义是这样；自己写类时别忘了默认参数。`tail.next, list1 = list1, list1.next` 这种元组赋值是安全的：右边先全部求值，再依次赋给左边。
