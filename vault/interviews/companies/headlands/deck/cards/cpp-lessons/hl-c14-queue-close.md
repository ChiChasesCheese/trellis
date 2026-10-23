---
id: hl-c14-queue-close
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 11
---
## Q
阻塞队列的 `close()` 怎么写？为什么这是干净的关闭协议？多生产者多消费者用 `notify_one` 还是 `notify_all`？

## A
```cpp
void close() {
    { std::lock_guard<std::mutex> g(m_); closed_ = true; }
    not_empty_.notify_all();
}
```
- `pop` 的等待条件是 `!q_.empty() || closed_`：关闭后消费者把队列**排空**，之后得到空 `optional` 退出。
- `notify_all` 让所有阻塞的消费者都醒来看到 `closed_`。
- 多生产者多消费者：用 `notify_all`，或每个条件一个 `cv`（`not_empty_` / `not_full_`）。
- 实测：生产者放入 1000 个，消费者收到 1000 个，和 500500。
