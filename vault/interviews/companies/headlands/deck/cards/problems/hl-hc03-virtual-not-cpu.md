---
id: hl-hc03-virtual-not-cpu
node: problems.hc03-recursive-sum
type: qa
step: 15
---
## Q
为什么虚拟线程（virtual thread）不适合 CPU 密集的并行求和？5000 万个 long 的实测数据怎么说？

## A
虚拟线程跑在载体线程（carrier，一个 ForkJoinPool，默认并行度 = 核数）上，只在**阻塞点**（I/O、锁、`sleep`）才卸载；CPU 密集线程永远不让出载体，没有时间片抢占。它**不会多出并行度**，解决的是「线程太贵、阻塞 I/O 太多」，不是「核不够用」。

实测（12 核，5000 万 long，取最好一次）：
- 顺序 128 位 `checkedSum`：16–18 ms；
- ForkJoin threshold=10⁵：3–4 ms（threshold=100：7–8 ms）；
- parallel stream（块下标）：4 ms；
- 虚拟线程 12 块：4–5 ms；10 000 块：4–8 ms；**1 000 000 块：190–204 ms**；
- 虚拟线程 12 块且 `-Djdk.virtualThreadScheduler.parallelism=1`：17 ms（≈ 顺序）。

解读：12 块与 ForkJoin 一样快，是因为载体恰有 12 个——并行度来自载体线程。限为 1 个就退化成顺序；百万个只增加创建 / 调度 / 栈块开销（慢约 50 倍）。加速只有约 4–5 倍：5000 万 × 8 B = 400 MB，顺序 17 ms ≈ 23 GB/s，**受内存带宽限制**，不是核数限制。

结论：**CPU 密集 → ForkJoin / parallel stream，线程数 ≈ 核数；I/O 密集 → 虚拟线程。** 另外区分：并行（parallelism）是真的同时在不同核上跑；并发（concurrency）是交替推进。
