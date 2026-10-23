---
id: hl-j09-priorityqueue-concurrency
node: java21.j09-sequenced-collections
type: qa
step: 30
---
## Q
Sequenced Collections 的新方法有线程安全保证吗？并发场景该用哪些类？

## A
新方法没带来任何同步保证，`Collections.synchronizedList(...)` 等包装器保持原样。

并发场景用：
- `ConcurrentSkipListMap`（它是 `NavigableMap`，所以也是 `SequencedMap`）；
- `ConcurrentLinkedDeque`。
