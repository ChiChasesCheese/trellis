---
id: hl-c13-spsc-code
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 12
---
## Q
写出 `SpscRing<T, N>` 的 `push` 和 `pop`，标明每个原子操作的内存序。

## A
```cpp
bool push(const T& v) {                        // 仅生产者线程
    std::size_t t = tail_.load(std::memory_order_relaxed);        // 自己的变量
    if (t - head_.load(std::memory_order_acquire) == N) return false;   // 满
    buf_[t & (N - 1)] = v;
    tail_.store(t + 1, std::memory_order_release);                // 发布槽位
    return true;
}
bool pop(T& out) {                             // 仅消费者线程
    std::size_t h = head_.load(std::memory_order_relaxed);
    if (h == tail_.load(std::memory_order_acquire)) return false; // 空
    out = buf_[h & (N - 1)];
    head_.store(h + 1, std::memory_order_release);                // 归还槽位
    return true;
}
```
- 声明：`alignas(64) std::atomic<size_t> head_{0}, tail_{0};` 与 `alignas(64) T buf_[N];`，并 `static_assert((N & (N-1)) == 0)`。
- 实测：二百万个元素按序、无丢失传输，和校验匹配。
