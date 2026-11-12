---
slug: merge-k-sorted-lists
---
## Q
**LC 23 合并 K 个升序链表**｜Hard

把 `k` 个升序链表合并成一个升序链表。

## A
**一句话。** 最小堆装每条链表的当前队头，弹最小的接到结果后，再把它的后继换进堆。

```python
def merge_k_lists(lists):
    # (值, 链表编号, 节点)：编号保证不会去比较 ListNode
    heap = [(n.val, i, n) for i, n in enumerate(lists) if n]
    heapq.heapify(heap)
    dummy = tail = ListNode()
    while heap:
        _, i, node = heap[0]
        tail.next = node
        tail = node
        if node.next:            # 原地替换堆顶，只下沉一次
            nx = node.next
            heapq.heapreplace(heap, (nx.val, i, nx))
        else:
            heapq.heappop(heap)
    return dummy.next
```

**复杂度。** 时间 `O(N log k)`，空间 `O(k)`。

**易错点。**
- 堆里只放 `(val, node)`：`[[1,4],[1,3]]` 值相同时比较 `ListNode` 抛 `TypeError`，要多放唯一编号。
- 空链表也入堆：`[[]]` 里是 `None`，读 `.val` 报错，建堆要过滤。
- 弹出后忘了放回后继：只得 `[1,1,2]`。

**追问。**
- 分治怎么做？：两两合并，共 `log k` 轮，同样 `O(N log k)`，额外空间 `O(1)`。
- 为什么不逐个顺序合并？：重复扫已合并部分，`O(N·k)`。
- 输入是 `k` 个有序文件或迭代器？：`heapq.merge`，惰性产生，内存只与 `k` 有关。

**同模式。** LC 21 合并两个有序链表、LC 378 有序矩阵中第 K 小的元素、LC 373 查找和最小的 K 对数字、LC 632 最小区间
