---
id: hl-j16-lock-discipline
node: java21.j16-concurrency-primitives
type: qa
step: 27
---
## Q
用 `ReentrantLock` 的铁律是什么？`lock()` 应该放在 `try` 里面还是外面？写出标准模板。

## A
**`unlock()` 必须在 `finally` 里**，否则异常路径永远占着锁。**`lock()` 放在 `try` 外面**，否则 `lock()` 自己失败时 `finally` 会错误解锁。

```java
lock.lock();
try {
    // 临界区
} finally {
    lock.unlock();
}
```
`ReentrantLock` 换 `synchronized` 不是「总是更好」：JDK 24 起 `synchronized` 在虚拟线程里不再 pin，简单互斥用 `synchronized` 更短且不会漏 `unlock`；需要超时、可中断、公平、多条件时才用 `ReentrantLock`。
