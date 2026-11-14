---
slug: amazon-lazy-merge-event-streams
---
## Q
**惰性合并 k 路有序事件流**｜Medium

`k` 个迭代器各自按时间戳升序产出 `(ts, event)`。写一个生成器按时间全局升序产出所有事件，不能预先读完全部事件。

## A
**一句话。** 最小堆只放每路的当前头 `(ts, 路号, event)`，弹出最早的就只从同一路再拉一个，堆大小始终 `<= k`。

```python
def merge_streams(streams):
    its = [iter(s) for s in streams]
    heap = []

    def pull(i):              # 从第 i 路再拉一个
        head = next(its[i], None)
        if head is not None:
            heappush(heap, (head[0], i, head[1]))

    for i in range(len(its)):
        pull(i)
    while heap:
        ts, i, ev = heappop(heap)
        yield ts, ev
        pull(i)               # 只补刚弹出的那一路
```

**复杂度。** 时间 `O(N log k)`，`N` 为事件总数；空间 `O(k)`。

**易错点。**
- 堆里只放 `(ts, event)`：时间戳相同就去比 `event`，`dict` 不能比较直接 `TypeError`；路号放第二位当 tie-breaker，每路在堆里只有一项所以不会再往后比。
- 一开始把所有事件都推进堆：失去惰性，内存变成 `O(N)`。

**追问。**
- 实时无界流？：堆顶不一定全局最早，安静的流可能晚到更早的事件；要水位线，所有流都推进到 `>= t` 才放出 `t` 之前的事件，空闲流靠心跳推进。
- 标准库？：`heapq.merge(*streams)` 就是这个实现，也是惰性的。

**同模式。** LC 23 合并 K 个升序链表、LC 373 查找和最小的 K 对数字、LC 378 有序矩阵中第 K 小的元素、LC 632 最小区间
