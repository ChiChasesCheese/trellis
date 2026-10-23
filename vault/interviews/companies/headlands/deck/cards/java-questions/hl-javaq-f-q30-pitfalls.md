---
id: hl-javaq-f-q30-pitfalls
node: java-questions.f-concurrency
type: qa
step: 20
---
## Q
使用 `ConcurrentHashMap` 的 `computeIfAbsent` 有哪些注意点？`size()` 和迭代器的语义是什么？
Is `size()` accurate?

## A
- **不要在 `computeIfAbsent` 的函数里修改同一个 map**（可能死锁或抛 `IllegalStateException`）；函数要短，因为期间持有桶锁。
- **`size()`**：并发下是近似快照（估计值）。
- **迭代器**：弱一致，不抛 `ConcurrentModificationException`。
