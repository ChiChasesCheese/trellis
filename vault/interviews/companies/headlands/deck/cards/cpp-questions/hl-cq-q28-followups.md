---
id: hl-cq-q28-followups
node: cpp-questions.g-concurrency
type: qa
step: 5
---
## Q
三个追问：notify 时要不要持有锁？`lock_guard` 和 `unique_lock` 的开销？读写锁用什么？

## A
- **notify**：持锁和不持锁都正确；解锁后再 notify 可以避免被唤醒的线程立刻又阻塞，但谓词涉及的状态必须在锁下修改。
- **开销**：`lock_guard` 与 `unique_lock` 差别可忽略；`unique_lock` 多存一个标志，因此可以提前解锁。
- **读写锁**：`std::shared_mutex`，读者用 `shared_lock`，写者用 `unique_lock`；只有读远多于写且临界区较长时才值得。
