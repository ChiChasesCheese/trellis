---
id: hft-java-agrona-aeron-agrona
node: java.agrona-aeron
type: qa
step: 1
---
## Q
Agrona 库提供哪些工具？交易系统为什么不直接用 `java.util.HashMap`？

## A
Agrona（Real Logic 出品，是 Aeron 的基础库）提供：
- **无垃圾集合**：`Int2IntHashMap`、`Long2ObjectHashMap` 等原始类型的 map 和 list，开放寻址，没有 Entry 对象，也没有装箱；
- **缓冲区**：`DirectBuffer`、`UnsafeBuffer` 统一包装 `byte[]`、`ByteBuffer` 或内存地址，提供按偏移读写 `long`、`int` 的方法；
- **并发结构**：堆外的 `OneToOneRingBuffer`、`ManyToOneRingBuffer`，以及并发队列；
- **空闲策略**：`IdleStrategy`，控制没活干时是自旋还是睡眠。

`HashMap<Long, Order>` 每插入一个条目，要创建一个 `Long` 键（约 24 字节）和一个 `Node`（约 32 字节），读取时还要跟随好几次指针；`Long2ObjectHashMap` 把键存在原始 `long[]` 里，稳态不分配。
