---
id: hl-cq-q29-followups
node: cpp-questions.g-concurrency
type: qa
step: 11
---
## Q
三个追问：`compare_exchange_weak` 和 `strong` 的区别？内存栅栏（fence）是什么？`atomic<std::shared_ptr>` 是无锁的吗？

## A
- **weak vs strong**：`weak` 可能伪失败（spurious failure），在某些架构的循环里更便宜；`strong` 只在值确实不同时才失败。
- **fence**：`std::atomic_thread_fence` 约束前后操作的顺序而不绑定变量；优先用带序的原子操作。
- **`atomic<shared_ptr>`**：不是无锁的，常见库用锁实现。
