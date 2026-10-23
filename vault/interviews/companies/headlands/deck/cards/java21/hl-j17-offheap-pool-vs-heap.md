---
id: hl-j17-offheap-pool-vs-heap
node: java21.j17-ffm-api
type: qa
step: 11
---
## Q
100 万条成交记录：堆上 `Fill[]`（`record Fill(long id, long px, int qty)`）与堆外 `sequenceLayout` 池，内存形态和 GC 影响有何区别？

## A
- **堆上**：每个 `Fill` 是独立对象（对象头 + 字段，约 **32 字节**），数组里是 100 万个**引用**，GC 要追踪 100 万个对象。
- **堆外**：一块**连续的 24 MB**（24 字节 × 100 万 = 24 000 000），GC 眼里「一个都没有」，离开 `try` 块立刻归还，不用等 GC。

可用 `-XX:NativeMemoryTracking=summary` 观察堆外使用。算出 n = 1000000、qty 合计 102999997、VWAP ≈ 18999.5。
