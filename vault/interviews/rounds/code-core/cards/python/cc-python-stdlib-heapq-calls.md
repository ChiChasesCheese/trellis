---
id: cc-python-stdlib-heapq-calls
node: python.stdlib
type: qa
---
## Q
You need the cheapest item repeatedly, a top-3 by score, and a max-heap. Write the `heapq` calls from memory, including the deterministic tie-break.

## A
```python
import heapq
h = []                                   # a plain list IS the heap
heapq.heappush(h, (cost, seq, item))     # tuple key: ties resolve by seq
cost, seq, item = heapq.heappop(h)       # smallest; h[0] peeks without popping
heapq.heapify(rows)                      # O(n), in place
heapq.nlargest(3, rows, key=len)         # top-k without a full sort
heapq.heappush(h, (-score, item))        # max-heap by negation
```

- `heapq` is min-only — negate the key for a max-heap.
- Never mutate an item's key in place; push a new entry and drop stale tops on read ([[cc-performance-amortized-lazy-heap]]).
- `heappushpop` and `heapreplace` do both in one sift when you keep a bounded top-k.

## Q zh
你需要反复取出代价最小的项、按分数取 top-3、以及一个最大堆。凭记忆写出 `heapq` 的调用，包括确定性的平局处理。

## A zh
```python
import heapq
h = []                                   # 一个普通 list 就是堆
heapq.heappush(h, (cost, seq, item))     # 元组键：平局按 seq 决出
cost, seq, item = heapq.heappop(h)       # 取最小；h[0] 只看不弹
heapq.heapify(rows)                      # O(n)，原地
heapq.nlargest(3, rows, key=len)         # 不用全排序拿 top-k
heapq.heappush(h, (-score, item))        # 取负得到最大堆
```

- `heapq` 只有最小堆 —— 要最大堆就把键取负。
- 绝不要原地改某项的键；压入新项，读取时丢掉过期堆顶（[[cc-performance-amortized-lazy-heap]]）。
- 维护有界 top-k 时，`heappushpop` 和 `heapreplace` 一次下沉完成两件事。
