---
id: hl-c14-blocking-queue
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 10
---
## Q
面试问：实现一个线程安全的有界阻塞队列（生产者-消费者）的 `push` 和 `pop`。
Interview question: Implement a bounded blocking queue.

## A
```cpp
void push(T v) {
    std::unique_lock<std::mutex> lk(m_);
    not_full_.wait(lk, [&] { return q_.size() < cap_; });
    q_.push_back(std::move(v));
    lk.unlock();
    not_empty_.notify_one();
}
std::optional<T> pop() {            // 空 optional = 已关闭且排空
    std::unique_lock<std::mutex> lk(m_);
    not_empty_.wait(lk, [&] { return !q_.empty() || closed_; });
    if (q_.empty()) return std::nullopt;
    T v = std::move(q_.front()); q_.pop_front();
    lk.unlock();
    not_full_.notify_one();
    return v;
}
```
- 成员：`mutex`、两个 `condition_variable`（`not_empty_`、`not_full_`）、`deque`、容量、`closed_`。
- 必须 `unique_lock`：`wait()` 要能解锁/重加锁。
