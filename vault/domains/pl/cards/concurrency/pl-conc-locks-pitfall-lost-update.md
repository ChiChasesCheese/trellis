---
id: pl-conc-locks-pitfall-lost-update
node: concurrency.locks-shared-memory
type: qa
step: 9
---
## Q
4 个线程各对一个共享整数累加 100 万次，不加锁会丢多少更新？为什么这种 bug 在测试里经常漏过去？

## A
Java 实测（`plain++` 不加锁，对比 `synchronized` 内累加）：
```java
for (int j = 0; j < 1_000_000; j++) plain++;                         // 4 threads
for (int j = 0; j < 1_000_000; j++) synchronized (lock) { locked++; } // 4 threads
```
输出：`unsynchronized: 1050193 (expected 4000000)`、`synchronized: 4000000`。丢了约四分之三的更新；Go 同样的代码得到 `1338145`。每次运行的数字不同。

为什么丢：`n++` 是读、加、写三步。两个线程都读到 5，都写回 6，一次加法消失。线程越多、临界区越短、核越多，碰撞越频繁。

为什么漏过测试：
1. 数据竞争是**概率性**的，取决于调度。把循环从 100 万减到 1000，单核小负载下大概率一次不丢，测试绿了。
2. 编译器和 CPU 的优化会改变表现：JIT 编译前后、不同硬件上结果不同。
3. 很多业务场景的竞争窗口只有几纳秒，只在生产的高并发下才暴露。

代价权衡：不加锁快（这台机器上 7 毫秒），加锁正确但慢约 70 倍（488 毫秒，激烈竞争下）。这提醒的是**结构**：不要让 4 个线程每次迭代都争同一个变量，而是每个线程累加自己的局部变量，最后合并一次，得到既快又对的结果。

检测手段：Go 的 `go run -race` 会指出两条冲突访问的栈（`WARNING: DATA RACE`）；Java 用 jcstress 压测；Rust 编译器直接拒绝。
