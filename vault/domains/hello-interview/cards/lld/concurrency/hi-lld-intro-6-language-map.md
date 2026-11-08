---
id: hi-lld-intro-6-language-map
node: qb.lld.kv-store-eviction.pre-lld-concurrency-intro
type: qa
step: 6
---
## Q
**各语言的并发原语对照**｜低层设计 · 并发

面试常用语言里，锁、读写锁、条件变量、信号量、阻塞队列、原子整数和并发 map 分别对应什么？有哪些语言特例要记住？

## A
**要点。**

| 概念 | Java | Python | Go |
|---|---|---|---|
| 锁 | `synchronized` / `ReentrantLock` | `threading.Lock` | `sync.Mutex` |
| 读写锁 | `ReentrantReadWriteLock` | 无（用第三方） | `sync.RWMutex` |
| 条件变量 | `wait/notify` | `threading.Condition` | `sync.Cond` |
| 信号量 | `Semaphore` | `threading.Semaphore` | `x/sync/semaphore` |
| 阻塞队列 | `LinkedBlockingQueue` | `queue.Queue` | 带缓冲的 channel |
| 原子整数 | `AtomicInteger` | 无（用锁） | `sync/atomic` |
| 并发 map | `ConcurrentHashMap` | 无（用锁保护 dict） | `sync.Map` |

**易错。** Python 的 GIL 使 CPU 密集代码不能从线程中获益，I/O 密集的才能；要 CPU 并行用 multiprocessing。Go 的惯用法是用 channel 代替阻塞队列和条件变量，拿不准就用 channel。C++ 常需要手工组合原语（`std::mutex`、`std::condition_variable`、`std::atomic<int>`），可考虑 Intel TBB 的高层抽象；C# 对应 `lock`、`SemaphoreSlim`、`BlockingCollection`、`Interlocked`、`ConcurrentDictionary`。

**使用时机。** 用自己最熟的语言回答，先说出对应的原语名字。
