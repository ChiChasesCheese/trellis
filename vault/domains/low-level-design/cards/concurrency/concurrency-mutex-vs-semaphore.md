---
id: concurrency-mutex-vs-semaphore
node: concurrency.primitives
type: qa
---
## Q
A binary semaphore and a mutex both admit one thread at a time. What's the real difference, and when do you reach for a semaphore?

## A
**Ownership.** A mutex must be released by the thread that locked it (enabling reentrancy and priority-inheritance); a semaphore's permit can be released by *any* thread.

- Reach for a **counting semaphore** to limit access to N identical resources (connection pool of 10, rate-limit concurrent downloads).
- Reach for a **binary semaphore** for cross-thread signaling: thread A `acquire`s, thread B `release`s to wake it — impossible with a mutex.
- Protecting shared mutable state = mutex; permits/signaling = semaphore.

## Q zh
mutex 和 semaphore 之间有什么区别？何时使用每个？

## A zh
**Mutex（互斥体）**：
- 二元：锁定（1）或解锁（0）
- 仅持有者可以解锁
- 用途：保护临界区，强制独占访问

**Semaphore**：
- 计数器：N 许可
- 任何线程都可以释放许可（甚至没有获取的线程）
- 用途：控制 N 个资源的池访问、信令

例子：
- Mutex：保护`count`变量的增量
- Semaphore：有 10 个线程的线程池；10 个许可，一个线程获取一个许可来工作

混淆：
- 二元信号量 (N=1) 似乎像 mutex，但任何线程都可以释放它
- Java 的 `synchronized` 是 mutex
- `Semaphore(1)` 和 `ReentrantLock` 类似但不一样

何时使用：
- Mutex：保护数据
- Semaphore：管理资源池
