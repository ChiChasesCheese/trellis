---
id: hl-c13-spinlock
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 9
---
## Q
用 `std::atomic_flag` 写一个自旋锁。`lock` 和 `unlock` 各该用什么内存序？为什么？

## A
```cpp
class SpinLock {
    std::atomic_flag f_ = ATOMIC_FLAG_INIT;
public:
    void lock() {
        while (f_.test_and_set(std::memory_order_acquire))
            std::this_thread::yield();
    }
    void unlock() { f_.clear(std::memory_order_release); }
};
```
- `test_and_set` 用 **acquire**，`clear` 用 **release**：正好形成临界区的边界，前一个持有者在临界区内的写入对下一个持有者可见。
- 自旋时 `yield`/退避，否则占满核心。
- 实测：两个线程共累加 200000 次，自旋锁保护的计数器精确得 200000。
