---
id: pl-conc-memmodel-found-volatile
node: concurrency.atomics-memory-models
type: qa
step: 2
---
## Q
Java 的 `volatile` 和 happens-before 是什么？用一个“写线程发布数据、读线程等标志”的小场景说明它保证了什么。

## A
**happens-before**（先行发生）是 Java 内存模型（JMM）里的一个关系：如果操作 A happens-before 操作 B，那么 A 的结果对 B **一定可见**，且 A 不会被重排到 B 之后。程序里有几种方式建立它：
- 同一线程内，前面的语句 happens-before 后面的；
- 对同一把锁，解锁 happens-before 之后的加锁；
- 对同一个 `volatile` 变量，写 happens-before 之后的读；
- `Thread.start()` 之前的操作 happens-before 新线程里的所有操作；线程里的所有操作 happens-before 另一线程成功 `join()` 它。
关系具有传递性。

**`volatile`** 修饰一个字段，含义是：对它的每次读写都直接访问主内存语义（不被缓存在寄存器里），并建立上面的 happens-before。

场景：
```java
static int data;
static volatile boolean ready;
// reader thread
while (!ready) Thread.onSpinWait();
System.out.println("data = " + data);
// writer thread
data = 42;          // plain write
ready = true;       // volatile write publishes everything before it
```
输出：`data = 42`。推理：`data = 42` 在同一线程内 happens-before `ready = true`；`ready = true`（volatile 写）happens-before 读线程里读到 `true` 的那次 volatile 读；读之后的 `println` 在读线程内。沿传递性，读线程一定看到 `data == 42`。如果 `ready` 不是 `volatile`，读线程可能永远看不到 `true`，或者看到 `true` 却读到 `data` 的旧值 0。

边界：`volatile` 只保证可见性和有序性，**不保证复合操作的原子性**：`counter++` 对 volatile 字段仍然是三步（读、加、写），多个线程同时做仍会丢更新，需要锁或原子类。
