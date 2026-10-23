---
id: hl-cache-java-exits
node: foundations.cpu-cache-locality
type: qa
step: 17
---
## Q
Java 里怎样摆脱对象带来的缓存和内存开销？列出四条出路。

## A
1. **用原始类型数组**：`long[]`、`int[]`；要映射时用开放寻址 + 两个平行数组自己写，或用库（Eclipse Collections、fastutil、Agrona 的 `Long2LongHashMap`）。
2. **对象池 / 复用**：避免反复分配。
3. **堆外内存**（`ByteBuffer.allocateDirect` / FFM 的 `MemorySegment`）：数据布局自己控制，不受 GC 搬移影响。
4. **Project Valhalla 的值类型（value classes）**：目标是让 `Long` 这样的小对象没有头、能平铺在数组里。JDK 21 还没有，知道它存在即可。
