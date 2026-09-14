---
id: cc-performance-amortized-lazy-heap
node: performance.amortized
type: qa
---
## Q
You need the least-loaded server after every connect and disconnect. Loads change in place, but `heapq` has no decrease-key. Describe the standard trick and prove it is fast enough.

## A
**Lazy invalidation: push a fresh `(load, index)` on every change, and discard stale tops on read.**

```python
while heap:
    ld, t = heap[0]
    if ld != load[t]:
        heapq.heappop(heap); continue
    return t
```

- Each event pushes at most one entry, so at most n entries ever exist and each is popped at most once — O(n log n) total, amortized O(log n) per operation, even though a single read can pop thousands.
- The heap holds more entries than there are servers; that is a memory cost, not a time cost.
- The tuple `(load, index)` also gives the "ties go to the smallest index" rule for free.

## Q zh
每次连接和断开之后你都需要负载最轻的服务器。负载是原地变的，而 `heapq` 没有 decrease-key。说出标准技巧，并证明它够快。

## A zh
**惰性失效：每次变更都压入一个新的 `(load, index)`，读取时把过期的堆顶丢掉。**

```python
while heap:
    ld, t = heap[0]
    if ld != load[t]:
        heapq.heappop(heap); continue
    return t
```

- 每个事件最多压入一项，所以总共最多 n 项，每项最多被弹出一次 —— 总计 O(n log n)，摊还每次操作 O(log n)，尽管单次读取可能弹掉上千项。
- 堆里的项会多于服务器数量；那是内存代价，不是时间代价。
- 元组 `(load, index)` 还顺带白送了「平局取最小下标」这条规则。
