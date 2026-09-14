---
id: cc-algorithms-topological-deterministic-order
node: algorithms.topological
type: qa
---
## Q
Several jobs become ready at the same moment. Kahn's with a `deque` emits them in an arbitrary order. Make it "smallest id first".

## A
**Swap the queue for a heap** — the ready *set* is genuinely unordered, so an order has to be imposed rather than discovered.

```python
ready = [u for u in nodes if indeg[u] == 0]
heapq.heapify(ready)
u = heapq.heappop(ready)
...
heapq.heappush(ready, v)
```

- Cost rises from O(V + E) to O(V log V + E) — irrelevant at assessment sizes, and `heapify` makes the build O(V) ([[cc-toolbox-heap-heapify]]).
- With a plain `deque`, the emitted order depends on the order edges were read. A hidden test **will** reorder the input, and your output changes while your logic did not.
- "Lexicographically smallest topological order" is exactly this heap version; a spec saying "any valid order" still deserves a deterministic one, so your own output is reproducible ([[cc-output-ordering-total-order]]).

## Q zh
若干作业在同一时刻就绪。用 `deque` 的 Kahn 算法会以任意顺序输出它们。改成「id 最小者优先」。

## A zh
**把队列换成堆** —— 就绪*集合*本身确实无序，所以顺序必须由你强加，而不是被发现。

```python
ready = [u for u in nodes if indeg[u] == 0]
heapq.heapify(ready)
u = heapq.heappop(ready)
...
heapq.heappush(ready, v)
```

- 代价从 O(V + E) 升到 O(V log V + E) —— 在测评规模下无关紧要，而且 `heapify` 让建堆是 O(V)（[[cc-toolbox-heap-heapify]]）。
- 用普通 `deque` 时，输出顺序取决于边被读入的顺序。隐藏测试**一定**会重排输入，于是逻辑没变而输出变了。
- 「字典序最小的拓扑序」正是这个堆版本；即便 spec 说「任意合法顺序」，也值得给出确定的那一个，好让你自己的输出可复现（[[cc-output-ordering-total-order]]）。
