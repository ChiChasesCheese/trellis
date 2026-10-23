---
id: hl-cq-q28-code-bounded-queue
node: cpp-questions.g-concurrency
type: qa
step: 2
---
## Q
补全有界生产者–消费者队列 `BoundedQueue` 的 `push` 和 `pop`：成员有 `std::mutex m_`、两个条件变量 `not_full_` / `not_empty_`、`std::deque<int> q_`、容量 `cap_`。要求用 `unique_lock` 加谓词的 `wait`。

## A
```cpp
void push(int v) {
    std::unique_lock lk(m_);
    not_full_.wait(lk, [&] { return q_.size() < cap_; });   // 谓词：醒来后重新检查条件
    q_.push_back(v);
    not_empty_.notify_one();
}
int pop() {
    std::unique_lock lk(m_);
    not_empty_.wait(lk, [&] { return !q_.empty(); });
    int v = q_.front(); q_.pop_front();
    not_full_.notify_one();
    return v;
}
```
实测消费的总和正确。
