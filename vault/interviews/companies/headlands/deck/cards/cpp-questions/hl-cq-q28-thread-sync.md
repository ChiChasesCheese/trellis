---
id: hl-cq-q28-thread-sync
node: cpp-questions.g-concurrency
type: qa
step: 1
---
## Q
面试题：C++ 怎么同步线程？`mutex`、`lock_guard`、`scoped_lock`、`condition_variable`、死锁。
How do you synchronize threads in C++? `mutex`, `lock_guard`, `scoped_lock`, `condition_variable`, deadlock.

## A
- 用 `std::mutex` 保护共享数据，**永远通过 RAII 加锁**：`lock_guard`（简单场景）、`unique_lock`（需要等待或提前解锁）、`scoped_lock`（一次锁多个互斥量，内部避免死锁）。
- 等待条件用 `condition_variable` 加**谓词**，防**虚假唤醒**（spurious wakeup）。
- **死锁**需要循环等待；用统一的加锁顺序，或 `scoped_lock` 来预防。
- C++ 的互斥量**不可重入**，不像 Java 的 `synchronized`。
