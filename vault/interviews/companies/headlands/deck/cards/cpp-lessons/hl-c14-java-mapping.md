---
id: hl-c14-java-mapping
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 1
---
## Q
Java 的 `Thread`、`synchronized`、`ReentrantReadWriteLock`、`Condition`、`ThreadLocal`、`CountDownLatch`、`BlockingQueue`、`interrupt` 在 C++ 里分别对应什么？

## A
- `Thread` / `ExecutorService` ↔ `std::thread` / `std::async`、`std::jthread`
- `synchronized` / `ReentrantLock` ↔ `std::mutex` + `lock_guard` / `unique_lock` / `scoped_lock`
- `ReentrantReadWriteLock` ↔ `std::shared_mutex`
- `Condition` / `wait/notify` ↔ `std::condition_variable`
- `Future` ↔ `std::future`；`ThreadLocal` ↔ `thread_local`
- `CountDownLatch` / `Semaphore` ↔ `std::latch` / `std::counting_semaphore`（C++20）
- `BlockingQueue` ↔ 自己用 `mutex` + `condition_variable` 写
- `Thread.interrupt()` ↔ `stop_token`（C++20，协作式）
