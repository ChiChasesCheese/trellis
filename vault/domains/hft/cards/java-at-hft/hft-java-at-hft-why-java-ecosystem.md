---
id: hft-java-at-hft-why-java-ecosystem
node: java-at-hft.why-java
type: qa
step: 4
---
## Q
Java 生态里有哪些专门为低延迟打造的工具，使它在交易公司里可行？

## A
这些库把“零垃圾、堆外、无锁”的写法标准化，不必每家公司从头重造：
- **Disruptor**：无锁环形缓冲区，线程间消息传递；
- **Agrona**：无垃圾集合、堆外缓冲区、并发队列；
- **Aeron**：基于 UDP 和 IPC 的低延迟消息传输，带录制回放和复制状态机；
- **Chronicle Queue/Map**：基于内存映射文件的持久化队列和堆外键值存储；
- **SBE**：生成 flyweight 编解码器的二进制消息格式；
- **JMH、HdrHistogram、JFR、async-profiler**：基准、延迟直方图和剖析；
- **ZGC 与 Azul Prime 的 C4**：并发整理的低停顿收集器。

有了这些，Java 在几十微秒量级的系统里可以做得很稳，也是它与“普通业务 Java”最大的差别。
