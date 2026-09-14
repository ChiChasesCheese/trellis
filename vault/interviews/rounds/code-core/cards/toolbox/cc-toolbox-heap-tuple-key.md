---
id: cc-toolbox-heap-tuple-key
node: toolbox.heap
type: qa
---
## Q
You need the least-loaded server, ties by smallest index. Write the heap entry, and say what breaks if a field in it is not comparable.

## A
**`heapq` is a min-heap over ordinary tuple comparison**, so the tie-break is simply the next tuple element.

```python
heap = [(0, i) for i in range(n)]        # ascending list ⇒ already a valid heap
load, i = heapq.heappop(heap)
heapq.heappush(heap, (load + 1, i))
```

- Every element that can be reached by a comparison must be orderable. If a payload object sits in the tuple and two entries tie on all preceding fields, the pop raises `TypeError` — put a **unique** tiebreaker (index, sequence number) before any payload.
- Descending on one field and ascending on another: negate the numeric one ([[cc-toolbox-heap-max-negation]]).
- The heap orders by the key **at push time**; a load that changes afterwards leaves a stale entry behind ([[cc-toolbox-heap-lazy-invalidation]]).

## Q zh
你需要负载最小的服务器，并列时取下标最小的。写出堆元素，并说明其中某个字段不可比较时会怎样。

## A zh
**`heapq` 是基于普通 tuple 比较的小顶堆**，所以 tie-break 就是 tuple 的下一个元素。

```python
heap = [(0, i) for i in range(n)]        # 升序列表 ⇒ 本身就是合法的堆
load, i = heapq.heappop(heap)
heapq.heappush(heap, (load + 1, i))
```

- 任何可能被比较到的元素都必须可排序。如果 tuple 里放了 payload 对象，而两个条目在前面所有字段上都相等，pop 会抛 `TypeError` —— 在任何 payload 之前放一个**唯一**的 tiebreaker（下标、序号）。
- 一个字段降序、另一个升序：对数值字段取负（[[cc-toolbox-heap-max-negation]]）。
- 堆是按**push 时**的 key 排序的；之后再变化的负载会留下一个过期条目（[[cc-toolbox-heap-lazy-invalidation]]）。
