---
id: cc-toolbox-heap-topk
node: toolbox.heap
type: qa
---
## Q
10^6 records, you need the 10 largest by score. Sort, `nlargest`, or a size-k heap — cost and choice?

## A
**Keep a size-k *min*-heap: O(n log k) time, O(k) memory.**

```python
h = []
for r in rows:
    heapq.heappush(h, (r.score, r.id))
    if len(h) > k:
        heapq.heappop(h)          # the smallest of the kept ones leaves
```

- A full sort is O(n log n) time and O(n) memory — fine at 10^5, wasteful at 10^6, impossible if the input streams.
- `heapq.nlargest(k, rows, key=...)` implements exactly this and is the right answer when everything is already in memory; `heappushpop` inside the loop is the same thing hand-rolled with one sift instead of two.
- The result is **not sorted**: a heap only guarantees its root. Finish with `sorted(h, reverse=True)` and apply the declared tie-break there ([[cc-output-ordering-total-order]]).
- Min-heap for top-k *largest* is the part people invert; the root you evict must be the worst of the ones you are keeping.

## Q zh
10^6 条记录，要按 score 取最大的 10 个。排序、`nlargest`、还是大小为 k 的堆 —— 代价与选择？

## A zh
**维护一个大小为 k 的*小顶*堆：时间 O(n log k)，内存 O(k)。**

```python
h = []
for r in rows:
    heapq.heappush(h, (r.score, r.id))
    if len(h) > k:
        heapq.heappop(h)          # 弹出已保留者中最小的那个
```

- 全排序是 O(n log n) 时间、O(n) 内存 —— 10^5 尚可，10^6 就浪费，输入是流式时更不可能。
- `heapq.nlargest(k, rows, key=...)` 正是这个实现，在数据已全在内存时是正确答案；循环里的 `heappushpop` 是同一件事的手写版，只做一次下沉而不是两次。
- 结果**不是有序的**：堆只保证堆顶。最后用 `sorted(h, reverse=True)`，并在那里应用规定的 tie-break（[[cc-output-ordering-total-order]]）。
- 用小顶堆取最*大*的 k 个，正是大家会搞反的地方；被淘汰的堆顶必须是已保留者中最差的那个。
