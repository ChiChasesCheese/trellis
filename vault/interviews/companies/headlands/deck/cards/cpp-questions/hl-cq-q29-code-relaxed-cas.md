---
id: hl-cq-q29-code-relaxed-cas
node: cpp-questions.g-concurrency
type: qa
step: 8
---
## Q
补全代码：用 `memory_order_relaxed` 的 `fetch_add` 让 `atomic<long> counter` 加 1；再用 `compare_exchange_weak` 的 CAS 循环，无锁地把 `atomic<int> maxv` 更新为不小于 `v` 的最大值。

## A
```cpp
std::atomic<long> counter{0};
counter.fetch_add(1, std::memory_order_relaxed);   // 4 线程 x 100 万次 -> 4000000

std::atomic<int> maxv{0};
int cur = maxv.load(std::memory_order_relaxed);
while (cur < v && !maxv.compare_exchange_weak(cur, v, std::memory_order_relaxed)) {}
// CAS 失败时 cur 被刷新为当前值，再重试
```
统计计数器只需要原子性，`relaxed` 就够，结果精确。
