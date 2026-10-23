---
id: hl-business-cache-locality
node: company.business
type: qa
step: 14
---
## Q
CPU 缓存局部性（cache locality）怎样带来性能收益？"冷数据挪走"在一个构造的基准里能快多少，Java 里对应什么？

## A
做法：把很少用到的**冷数据**从对象里挪走，让热数据挤进**同一条缓存行**（cache line），一次加载就拿到全部要用的字段，减少缓存未命中。

在一个构造的基准里，这样做快约 **11.8 倍**。

Java 里的对应手段是**对象布局**的取舍和**堆外内存**（off-heap memory）。这是交易公司常考的"性能直觉"：被问"为什么这样更快"时，终点常常落在缓存局部性。
