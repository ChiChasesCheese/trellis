---
id: hl-javaq-a-q03-gc-pauses
node: java-questions.a-speed
type: qa
step: 10
---
## Q
同一个分配密集负载（8 秒、约 100 MB 活跃数据、持续产生垃圾、堆 1 GB，探测线程记录相邻迭代的最大间隔）下，Parallel GC、G1、分代 ZGC 的最大停顿各是多少？怎么看待"不分配垃圾"的对照组？

## A
最大间隔（max gap）：
- **Parallel GC**：22.4 ms；超过 1 ms 的有 230 次，超过 10 ms 有 10 次。
- **G1**：8.2 ms；超过 1 ms 有 116 次，超过 10 ms 为 0。
- **分代 ZGC**：0.14 ms；超过 1 ms 为 0。
- **对照（不分配垃圾）**：0.02 ms 与 2.26 ms（两次独立运行）——这是操作系统自身的抖动，**不要算到 GC 头上**。

ZGC 在 JDK 21 要写 `-XX:+UseZGC -XX:+ZGenerational`。这些数字只看量级与趋势，不是严格基准。
