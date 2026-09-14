---
id: concurrency-condvar-wait-loop
node: concurrency.primitives
type: qa
---
## Q
Why must a condition-variable wait always be
```java
while (queue.isEmpty()) { notEmpty.await(); }
```
and never `if (queue.isEmpty()) notEmpty.await();`? Two reasons.

## A
- **Spurious wakeups**: the platform may wake a waiter with no signal at all — permitted by POSIX and the JVM.
- **The predicate can be false again by the time you run**: between the signal and reacquiring the lock, another woken (or barging) thread may have consumed the item. `signalAll` deliberately wakes many threads that must re-check.

The loop re-tests the predicate *while holding the lock*, so you only proceed when the condition truly holds. Rule: wait is always inside a loop guarding the predicate.

## Q zh
为什么条件变量的等待必须写成
```java
while (queue.isEmpty()) { notEmpty.await(); }
```
而绝不能写成 `if (queue.isEmpty()) notEmpty.await();`？两个理由。

## A zh
- **虚假唤醒（spurious wakeup）**：平台可能在根本没有信号的情况下唤醒一个等待者 —— POSIX 和 JVM 都允许这样做。
- **等你真正运行时谓词可能又不成立了**：在信号发出和你重新拿到锁之间，另一个被唤醒的（或插队的）线程可能已经把那个元素消费掉了。`signalAll` 正是要唤醒一批必须重新检查的线程。

循环会在*持有锁的状态下*重新检验谓词，所以只有条件真正成立时你才会往下走。规则：wait 永远放在一个守护谓词的循环里。
