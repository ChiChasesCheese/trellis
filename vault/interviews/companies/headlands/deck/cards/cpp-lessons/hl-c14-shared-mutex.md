---
id: hl-c14-shared-mutex
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 8
---
## Q
面试问：什么时候用 `shared_mutex`？写出读写锁的价格类。
Interview question: When do you use `shared_mutex`?

## A
```cpp
class Prices {
    mutable std::shared_mutex m_;
    long px_ = 100;
public:
    long read() const { std::shared_lock<std::shared_mutex> g(m_); return px_; }
    void write(long v) { std::unique_lock<std::shared_mutex> g(m_); px_ = v; }
};
```
- 许多读者**或**一个写者（Java 的 `ReentrantReadWriteLock`）。
- 适合**读远多于写且读临界区较长**；否则普通 `mutex` 更快，因为 `shared_mutex` 本身更重。
