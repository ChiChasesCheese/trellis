---
id: tlc-reverse-nodes-in-k-group-5-alt
node: p1.reverse-nodes-in-k-group
type: qa
step: 5
---
## Q
**LC 25 K 个一组翻转链表**｜另一种解法

用递归怎么写这个问题？它和迭代版相比，什么时候该选哪个？

## A
**思路。** 先沿着链表数 `k` 个节点，数不够就原样返回 `head`。够了，就先**递归处理后面的部分**，得到它翻好之后的头；再用这个头作为 `prev` 起点，把本组 `k` 个节点反转，组尾自然连到后面的结果上。

```python
def reverse_k_group_rec(head: ListNode | None, k: int) -> ListNode | None:
    node = head
    for _ in range(k):                       # 数 k 个，不够就原样返回
        if node is None:
            return head
        node = node.next
    prev, cur = reverse_k_group_rec(node, k), head   # 后面的部分先处理好，当作翻转后的接尾
    for _ in range(k):
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    return prev
```

运行：`([1,2,3,4,5], 2)` → `[2, 1, 4, 3, 5]`，`([1,2,3,4,5], 3)` → `[3, 2, 1, 4, 5]`，`([1,2,3], 3)` → `[3, 2, 1]`，`([1,2,3,4,5,6,7], 3)` → `[3, 2, 1, 6, 5, 4, 7]`。

**复杂度。** 时间 `O(n)`；空间 `O(n/k)` 的调用栈。

**什么时候选哪个。**
- 递归版没有哑节点，也没有 `group_prev` 的接线，代码更短，思路是「先把后面的做完，再翻自己这一组」，面试里容易讲清楚。
- 迭代版满足进阶的 `O(1)` 空间；递归版的深度是 `n / k`，`k = 2`、`5000` 个节点时有 `2500` 层，超过 Python 默认递归上限约 `1000`，会 `RecursionError`；`k` 较大（如 `k = 1000`）时深度只有 `5`，没有问题。
- 面试官问到「额外空间」时，先说递归是 `O(n/k)`，再给出迭代版；如果面试官接受 `O(n/k)`，递归版更不容易写错指针。
