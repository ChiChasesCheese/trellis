---
id: cc-toolbox-heap-park-and-restore
node: toolbox.heap
type: qa
---
## Q
The least-loaded worker cannot fit this task, but a busier one can. You already popped it. Now what?

## A
**Park it, keep popping, then push every parked entry back.** Discarding it removes a worker that can still serve later, smaller tasks.

```python
parked, chosen = [], None
while heap:
    e = heapq.heappop(heap)
    if fits(e):
        chosen = e; break
    parked.append(e)
for e in parked:
    heapq.heappush(heap, e)
```

- Worst case, when nobody fits, is O(W log W) for that one task; the typical case is one or two pops, so the run stays fast.
- **"Least loaded" and "least loaded that fits" are different answers** — the spec almost always means the second, and the difference shows up only in the capacity tests.
- A parked entry may also be stale; re-validate on the next pop rather than trusting it ([[cc-toolbox-heap-lazy-invalidation]]).
- The same shape covers "cheapest available room", "nearest region with capacity", "smallest free block ≥ size".

## Q zh
负载最小的 worker 装不下这个任务，但更忙的那个可以。你已经把它 pop 出来了。怎么办？

## A zh
**先把它寄存起来，继续 pop，选完之后再把寄存的全部 push 回去。** 直接丢弃会移除一个仍能承接后续小任务的 worker。

```python
parked, chosen = [], None
while heap:
    e = heapq.heappop(heap)
    if fits(e):
        chosen = e; break
    parked.append(e)
for e in parked:
    heapq.heappush(heap, e)
```

- 最坏情况（谁都装不下）对这一个任务是 O(W log W)；典型情况只 pop 一两次，整体仍然很快。
- **「负载最小」和「负载最小且装得下」是两个不同的答案** —— spec 几乎总是指后者，而差异只在容量相关的测试里暴露。
- 被寄存的条目也可能已经过期；下次 pop 时重新校验，不要信它（[[cc-toolbox-heap-lazy-invalidation]]）。
- 同样的写法适用于「最便宜的可用房间」「最近且有容量的区域」「不小于 size 的最小空闲块」。
