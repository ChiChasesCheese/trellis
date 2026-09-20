---
id: concurrency-condvar-wait-loop
node: concurrency.primitives
type: qa
---
## Q
为什么条件变量的等待必须写成
```java
while (queue.isEmpty()) { notEmpty.await(); }
```
而绝不能写成 `if (queue.isEmpty()) notEmpty.await();`？两个理由。

## A
- **虚假唤醒（spurious wakeup）**：平台可能在根本没有信号的情况下唤醒一个等待者 —— POSIX 和 JVM 都允许这样做。
- **等你真正运行时谓词可能又不成立了**：在信号发出和你重新拿到锁之间，另一个被唤醒的（或插队的）线程可能已经把那个元素消费掉了。`signalAll` 正是要唤醒一批必须重新检查的线程。

循环会在*持有锁的状态下*重新检验谓词，所以只有条件真正成立时你才会往下走。规则：wait 永远放在一个守护谓词的循环里。
