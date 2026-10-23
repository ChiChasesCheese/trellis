---
id: hl-javaq-d-q13-follow-ups
node: java-questions.d-memory
type: qa
step: 13
---
## Q
追问：怎么观察对象的实际大小？怎么压缩一个有一百万个小对象的结构？新 JDK 对对象头有什么改进？

## A
- **观察工具**：`jcmd <pid> GC.class_histogram`（每类实例数和字节数）；第三方 JOL 库；也可用 `ThreadMXBean.getThreadAllocatedBytes` 前后差测一个对象的大小。
- **压缩一百万个小对象**：改成并行数组，或打包进 `long[]` / `ByteBuffer`。`@Contended` 是反方向（加填充，用于防伪共享）。
- **紧凑对象头**：较新的 JDK 有实验性的"紧凑对象头"（头压到 8 字节），Java 21 里**没有**，面试时只说"在做"。
