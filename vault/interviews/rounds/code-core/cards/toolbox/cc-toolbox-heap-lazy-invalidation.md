---
id: cc-toolbox-heap-lazy-invalidation
node: toolbox.heap
type: qa
---
## Q
A worker's load changes while an entry carrying its old load is still inside the heap. `heapq` has no decrease-key. What do you do?

## A
**Lazy invalidation: never update in place — push a fresh entry and discard stale ones on pop.**

```python
w.ver += 1
heapq.heappush(heap, (w.load, w.id, w.ver))
...
while heap:
    load, wid, ver = heapq.heappop(heap)
    if ver == by_id[wid].ver:        # stale entry: silently dropped
        break
```

- The version can be the value itself when re-reading is cheap: `if load != cur_load[wid]: continue`.
- The heap grows to O(number of updates) — memory is the trade — but each entry is popped at most once, so the total stays O(m log m). That is the amortized argument you should say out loud.
- A *removed* element (a shut-down target, a deleted key) is handled identically: check a `dead` flag on pop rather than searching the heap for it.
- Without this, the alternatives are a linear scan per request (10^5 × 10^5 = 10^10) or an index-into-heap structure you do not have time to write.

## Q zh
某个 worker 的负载变了，而堆里还留着带旧负载的条目。`heapq` 没有 decrease-key。怎么办？

## A zh
**惰性失效：绝不原地更新 —— push 一个新条目，pop 时丢弃过期的。**

```python
w.ver += 1
heapq.heappush(heap, (w.load, w.id, w.ver))
...
while heap:
    load, wid, ver = heapq.heappop(heap)
    if ver == by_id[wid].ver:        # 过期条目：直接丢弃
        break
```

- 如果重新读取很便宜，版本号可以就是那个值本身：`if load != cur_load[wid]: continue`。
- 堆会涨到 O(更新次数) —— 内存是代价 —— 但每个条目最多被 pop 一次，所以总量仍是 O(m log m)。这就是你该讲出来的摊销论证。
- 被*移除*的元素（下线的目标、删掉的 key）处理方式相同：pop 时检查一个 `dead` 标志，而不是去堆里搜索它。
- 没有这一招，替代方案就是每次请求线性扫描（10^5 × 10^5 = 10^10），或者写一个你没时间写的带索引的堆。
