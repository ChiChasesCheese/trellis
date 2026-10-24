---
id: pl-conc-locks-found-condvar
node: concurrency.locks-shared-memory
type: qa
step: 4
---
## Q
条件变量（condition variable）是什么？它解决互斥锁解决不了的什么问题？请用“消费者等待队列非空”的场景说明。

## A
互斥锁只能回答“谁能进来”，回答不了“**等一个条件成立**”。场景：消费者线程要从队列里取数据，队列现在是空的。
- 反复加锁、检查、解锁（忙等）：白白烧 CPU；
- 睡一小会儿再试：延迟高、不精确。

**条件变量**让线程高效地等：`wait()` 会**原子地**做三件事——释放手里的锁、让当前线程睡眠、被唤醒后重新拿到锁再返回。生产者修改完状态后调用 `notify`（唤醒一个）或 `notifyAll`（唤醒全部），睡着的线程被叫醒，重新抢锁，检查条件。

例子（Java，`wait`/`notify` 是每个对象自带的条件变量）：
```java
synchronized (lock) {                       // consumer
    while (items.isEmpty()) lock.wait();    // release the lock and sleep until notified
    System.out.println("got " + items.poll());
}
// producer:
synchronized (lock) { items.add(42); lock.notify(); }
```
输出：`got 42`。

四种语言的对应物：Java `Object.wait/notify` 或 `Condition`；Go `sync.Cond`（`Wait`/`Signal`/`Broadcast`）；Rust `Condvar`（`wait_while`、`notify_one`）；Python `threading.Condition`（`wait`、`notify`）。它们总是和一把互斥锁配对使用，**检查条件必须在持锁时进行**。

重要的写法规则：等待写在循环里 `while (条件不成立) wait()`，不能用 `if`。原因是醒来不等于条件成立（虚假唤醒；或被别的线程抢先取走了数据）。
