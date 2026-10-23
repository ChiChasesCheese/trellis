---
id: hl-c14-raii-locks
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 6
---
## Q
面试问：`mutex`、`lock_guard`、`unique_lock`、`scoped_lock`、`shared_lock` 的区别？
Interview question: What are the differences between the C++ lock wrappers?

## A
`mutex` 的手动 `lock()`/`unlock()` 容易漏解锁（异常、提前 return），**永远用 RAII 包装**：
- `lock_guard`：构造加锁、析构解锁，最简单。
- `unique_lock`：可手动解锁/重新加锁、可与 `condition_variable` 配合；更灵活但稍重。
- `scoped_lock`（C++17）：同时锁多个 `mutex`，内部用死锁避免算法。
- `shared_lock` + `shared_mutex`：读写锁。

临界区越短越好；**不要在持锁时调用未知代码**（回调、虚函数、IO）。
