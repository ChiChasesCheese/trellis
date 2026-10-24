---
id: tlc-python-heapq-5-merge
node: python.heapq
type: qa
step: 5
---
## Q
**Python 工具箱｜`heapq.merge` 多路归并**

合并 `k` 个已排序序列，`heapq.merge` 做了什么？复杂度是多少？它和手写的「堆里放 `(值, 序号)`」有什么关系？

## A
`heapq.merge(*iterables, key=None, reverse=False)` 返回一个**惰性迭代器**，按顺序产出合并结果；内部堆里始终只有 `k` 个元素（每路一个当前头）。

```python
import heapq
print(list(heapq.merge([1, 4, 7], [2, 5], [3, 6, 8])))   # [1, 2, 3, 4, 5, 6, 7, 8]
print(list(heapq.merge([(1, "a"), (4, "b")], [(2, "c")], key=lambda t: t[0])))
print(list(heapq.merge([7, 4, 1], [5, 2], reverse=True)))   # [7, 5, 4, 2, 1]：输入本身是降序
```

- 总元素 `N`、路数 `k`：时间 `O(N log k)`，额外空间 `O(k)`，因为是生成器，不必先把结果全部装进内存。
- **每一路必须自己已经有序**，`merge` 不检查，错序的输入得到错序的输出。
- `reverse=True` 的含义是「输入都是降序、输出也降序」，不是把升序输入反着合并。
- 手写等价形式（LC 23 合并 K 个升序链表要用，因为 `ListNode` 不是普通序列）：

```python
def merge_k(lists: list[ListNode | None]) -> ListNode | None:
    h = [(l.val, i, l) for i, l in enumerate(lists) if l]
    heapq.heapify(h)
    dummy = tail = ListNode()
    while h:
        _, i, node = heapq.heappop(h)
        tail.next = tail = node          # 链接并前进尾指针
        if node.next:
            heapq.heappush(h, (node.next.val, i, node.next))
    return dummy.next
```

适用：LC 23、LC 378（有序矩阵第 k 小）、LC 373 数对和最小的前 k 个。
