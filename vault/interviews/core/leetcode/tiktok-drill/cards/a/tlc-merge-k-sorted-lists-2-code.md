---
id: tlc-merge-k-sorted-lists-2-code
node: a.merge-k-sorted-lists
type: qa
step: 2
---
## Q
**LC 23 合并 K 个升序链表**｜写出 Python 实现

链表数组 `lists`（`0 <= k <= 10^4`，每条链表长度 `<= 500`，总长度 `<= 10^4`，节点值在 `[-10^4, 10^4]`），每条链表升序。合并成一条升序链表并返回，用最小堆实现。

## A
**思路。** 把每条非空链表的队头放进堆，堆元素是 `(值, 链表编号, 节点)`。反复取堆顶，接到结果尾部；如果该节点还有后继，用后继替换堆顶，否则弹出堆顶。堆空时所有节点都已接完。

```python
import heapq


def merge_k_lists(lists: list[ListNode | None]) -> ListNode | None:
    # 堆里放 (值, 链表编号, 节点)：值相同时比编号，永远不会去比较 ListNode
    heap = [(node.val, i, node) for i, node in enumerate(lists) if node]
    heapq.heapify(heap)
    dummy = tail = ListNode()
    while heap:
        _, i, node = heap[0]            # 堆顶就是当前最小的队头
        tail.next = node
        tail = node
        if node.next:                   # 该链表还有后继：原地替换堆顶，只做一次下沉
            heapq.heapreplace(heap, (node.next.val, i, node.next))
        else:
            heapq.heappop(heap)
    return dummy.next
```

运行：`[[1,4,5],[1,3,4],[2,6]]` → `[1, 1, 2, 3, 4, 4, 5, 6]`，`[]` → `[]`，`[[]]` → `[]`，`10^4` 条各含一个节点的链表也能正确合并。

**复杂度。** 时间 `O(N log k)`：每个节点恰好被弹出一次，堆大小不超过 `k`；空间 `O(k)`。

**写法要点。** `heapify` 把列表原地调成堆，`O(k)`，比逐个 `heappush` 的 `O(k log k)` 快；`heap[0]` 只看堆顶不弹出，配合 `heapreplace`（弹出堆顶并压入新元素，一次下沉）比 `heappop` 加 `heappush` 少一半工作；元组里的编号 `i` 是 tie-breaker；`dummy = tail = ListNode()` 用哑节点省掉对结果头的特判；`_` 表示不用的值。
