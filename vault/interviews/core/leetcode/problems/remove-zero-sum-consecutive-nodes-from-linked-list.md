---
slug: remove-zero-sum-consecutive-nodes-from-linked-list
---
## Q
**LC 1171 从链表中删去总和值为零的连续节点**｜Medium

反复删去链表中和为 `0` 的连续节点序列，返回最终链表头。

## A
**一句话。** 前缀和加哈希两遍扫描：第一遍记每个前缀和最后出现的节点，第二遍让节点直接跳到它之后。

```python
def remove_zero_sum_sublists(head):
    dummy = ListNode(0, head)
    last = {}                  # 前缀和 -> 最后一个取到它的节点
    s, node = 0, dummy
    while node:                # 后出现的覆盖先出现的
        s += node.val
        last[s] = node
        node = node.next
    s, node = 0, dummy
    while node:
        s += node.val
        node.next = last[s].next   # 中间一段和为 0，整段跳过
        node = node.next
    return dummy.next
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 第一遍记录第一次出现的节点：第二遍指针会指回前面，链表成环。
- 只删相邻两个和为 0 的：`[1,2,-3]` 应为 `[]`，三个连续节点也能和为 0。
- 不加哨兵：头部整段被删时没有前驱，`dummy` 的前缀和 `0` 也要进哈希表。

**追问。**
- 数组版怎么做？：和为 `K` 的子数组个数用前缀和计数（LC 560）。
- 能 `O(1)` 额外空间吗？：不能，需要哈希表记前缀和；退路是 `O(n^2)` 枚举。

**同模式。** LC 560 和为 K 的子数组、LC 525 连续数组、LC 523 连续的子数组和、LC 82 删除排序链表中的重复元素 II
