---
id: hl-cq-q28-script
node: cpp-questions.g-concurrency
type: qa
step: 6
---
## Q
用英文 60 秒回答：How do you synchronize threads in C++? `mutex`, `lock_guard`, `scoped_lock`, `condition_variable`, deadlock.

## A
结构：RAII 加锁（`lock_guard`/`unique_lock`/`scoped_lock`）→ 条件变量必带谓词（虚假唤醒；有界队列实例）→ 死锁靠统一顺序或 `scoped_lock` → C++ 互斥量不可重入。

- I protect shared state with a `std::mutex`, always locked through **RAII** - `lock_guard` for simple cases, `unique_lock` when I need to wait or unlock early, and **`scoped_lock`** when I need several mutexes at once, since it avoids deadlock internally.
- For waiting I use a **condition variable with a predicate**, because of **spurious wakeups** and because the condition may change before I reacquire the lock. I wrote a bounded queue that way and verified the consumed sum.
- Deadlock needs circular wait; I prevent it with **consistent lock ordering** or `scoped_lock` - two threads transferring in opposite directions ran fine.
- C++ mutexes aren't reentrant, unlike Java's `synchronized`.
