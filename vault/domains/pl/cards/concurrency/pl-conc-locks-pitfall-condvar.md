---
id: pl-conc-locks-pitfall-condvar
node: concurrency.locks-shared-memory
type: qa
step: 11
---
## Q
使用条件变量（condition variable）等待某个条件时，为什么必须在循环里重新检查，而不能只用一次 `if`？各语言怎样降低这个风险？

## A
条件变量的 `wait` 原子地释放锁并睡眠，被唤醒后重新拿锁再返回。「被唤醒」不等于「条件成立」，有两个原因：
1. **虚假唤醒**（spurious wakeup）：操作系统和库允许 `wait` 在没有任何人通知时返回。
2. **被抢先**：被 `notify` 唤醒的线程要重新排队拿锁，在拿到之前，另一个线程可能已经取走了数据，条件重新变成假。

所以条件必须和一个**谓词**（predicate，一个读共享状态的判断）配对，醒来后重新判断：
```java
synchronized (lock) {
    while (items.isEmpty()) lock.wait();   // not "if"
    System.out.println("got " + items.poll());
}
```
Go 的 `sync.Cond`、Python 的 `Condition` 写法同形（`for cond.Wait()`、`while not items: cv.wait()`），输出同样是 `got 42`。

语言的应对反映了各自的哲学：
- Java、Go、Python 把循环交给程序员，文档里反复强调；写成 `if` 的 bug 平时能跑，只在高并发下偶发。
- Rust 的 `Condvar::wait_while(guard, |v| v.is_empty())` 把循环和谓词封装在库里，调用者不可能写成 `if`；Python 有 `wait_for(predicate)` 同理。

最佳实践：
- 通知方先在锁内修改状态，再 `notify`；等待方在锁内检查状态。
- 能用更高层的结构就不要直接写条件变量：阻塞队列、`Semaphore`、`CountDownLatch`、通道、`Future`，它们内部已经正确地写了这个循环。
