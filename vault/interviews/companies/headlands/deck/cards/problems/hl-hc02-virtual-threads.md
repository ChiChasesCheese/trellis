---
id: hl-hc02-virtual-threads
node: problems.hc02-merge-k-streams
type: qa
step: 13
---
## Q
为什么每个 source 用虚拟线程（virtual thread）生产者而不是线程池？它有哪些坑？

## A
平台线程一对一对应 OS 线程，很重（MB 级栈，几千个就吃力）；虚拟线程由 JVM 调度，极轻，可开几十万个，跑在少量载体线程（carrier thread）上。「每流一个线程、写普通阻塞代码」在 k=10000 时平台线程就崩了；虚拟线程阻塞在 `take()` / `put()` / 网络 I/O 时让出载体线程。线程池则要为「最坏阻塞数」定池大小。

```java
Thread t = Thread.ofVirtual().name("merge-producer-0").start(() -> { ... });
```
**坑**：
- 纯自旋（`while (!flag) {}`）不让出载体线程；
- JDK 21 里 `synchronized` 块内阻塞会**钉住**（pin）载体线程，所以阻塞处用 `ReentrantLock` 或 `java.util.concurrent` 的类（`ArrayBlockingQueue` 内部用 `ReentrantLock`）；
- **不要池化**虚拟线程；
- 不适合 CPU 密集任务（不阻塞，没好处）或需要线程局部大对象的场景。

阻塞队列还保证 happens-before：`put(x)` 之前的写入，另一线程 `take()` 到 `x` 之后都看得见，传递对象不必额外加锁。构造器里直接启动线程时，不要让 `this` 逃逸（线程只用局部变量）。
