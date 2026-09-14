---
id: concurrency-bounded-queue-invariants
node: concurrency.patterns
type: qa
---
## Q
You're asked to write a bounded blocking queue from scratch. State the two blocking invariants and sketch `put`/`take` with one lock and two conditions.

## A
Invariants: `put` **waits while full**, `take` **waits while empty**; after mutating, each signals the *opposite* waiters.

```java
final ReentrantLock lock = new ReentrantLock();
final Condition notFull = lock.newCondition(), notEmpty = lock.newCondition();

void put(T x) { lock.lock(); try {
    while (count == capacity) notFull.await();
    enqueue(x); notEmpty.signal();
} finally { lock.unlock(); } }

T take() { lock.lock(); try {
    while (count == 0) notEmpty.await();
    T x = dequeue(); notFull.signal(); return x;
} finally { lock.unlock(); } }
```

Every wait is a `while` loop; unlock in `finally`.

## Q zh
有界队列在并发中的不变量是什么？关键的临界区是什么？

## A zh
不变量：
- `size >= 0` 且 `size <= capacity`
- 如果 `size == 0`，消费者会阻塞
- 如果 `size == capacity`，生产者会阻塞

关键的临界区：
- 锁保护：`size`、`head`、`tail` 指针（或数组索引）
- 入队操作：增加大小，获取下一个写位置
- 出队操作：减少大小，获取下一个读位置

条件变量：
- `notEmpty`：当大小从 0 变为 1 时发出信号（通知等待的消费者）
- `notFull`：当大小从 capacity 变为 capacity-1 时发出信号（通知等待的生产者）
