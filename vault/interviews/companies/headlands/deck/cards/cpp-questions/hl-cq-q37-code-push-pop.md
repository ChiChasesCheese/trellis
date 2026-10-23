---
id: hl-cq-q37-code-push-pop
node: cpp-questions.i-low-latency
type: qa
step: 8
---
## Q
补全 SPSC 队列的 `push` 和 `pop`（成员：`head_`、`tail_` 两个 `atomic<size_t>`，`head_cache_`、`tail_cache_` 两个本地缓存，数组 `buf_[N]`，`N` 是 2 的幂；先用缓存的对方索引判满 / 空，看起来满 / 空时才 acquire 读真实值）。

## A
```cpp
bool push(const T& v) {
    auto t = tail_.load(std::memory_order_relaxed);
    if (t - head_cache_ == N) {                       // 看起来满了才去读真正的 head
        head_cache_ = head_.load(std::memory_order_acquire);
        if (t - head_cache_ == N) return false;
    }
    buf_[t & (N - 1)] = v;
    tail_.store(t + 1, std::memory_order_release);    // 发布元素
    return true;
}
bool pop(T& out) {
    auto h = head_.load(std::memory_order_relaxed);
    if (h == tail_cache_) {                           // 看起来空了才去读真正的 tail
        tail_cache_ = tail_.load(std::memory_order_acquire);
        if (h == tail_cache_) return false;
    }
    out = buf_[h & (N - 1)];
    head_.store(h + 1, std::memory_order_release);    // 释放槽位
    return true;
}
```
