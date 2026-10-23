---
id: hl-sdrun-java-discipline
node: system-design.how-to-run
type: qa
step: 26
---
## Q
Java 热路径的纪律：GC 停顿、对象头与指针追逐、堆外内存、锁与线程交接分别怎么做、为什么？

## A
- **GC 停顿**：稳态**零分配**（对象池、预分配数组、flyweight 视图、基本类型集合）；必要时 ZGC 或「一天只分配一次，夜里重启」+ 超大堆 + `-Xms=-Xmx` + `AlwaysPreTouch`。因为停顿 ∝ 存活对象或分配率，根治是分配率约为 0。
- **对象头与指针追逐**：数据放进 `long[]` / 连续数组 / 堆外，用整数下标代替引用，SoA；一次 DRAM 未命中约 80 ns。
- **堆外内存**：`MemorySegment`（FFM）/ `ByteBuffer.allocateDirect`，定长记录，`VarHandle` 原子读写；不受 GC 管，可映射文件、可跨进程共享。
- **锁与线程交接**：单写者 + SPSC 环，`setRelease` / `getAcquire`，忙等用 `Thread.onSpinWait()`；锁 = 内核介入 + 缓存行弹跳。
