---
id: hl-hc07-offheap
node: problems.hc07-ticker-hash-map
type: qa
step: 14
---
## Q
堆外内存（off-heap）与 FFM API 的 `Arena` / `MemorySegment` 怎么用？`OffHeapTickerMap` 的设计和限制是什么？

## A
普通对象在堆上由 GC 管理；堆外内存在 JVM 之外由程序自己申请释放。Java 21 的 **FFM API**（预览，Java 22 转正，需 `--enable-preview`）：
```java
try (Arena arena = Arena.ofShared()) {
    MemorySegment seg = arena.allocate(1024, 64);        // 1024 字节，64 字节对齐，已清零
    seg.set(ValueLayout.JAVA_LONG, 0, 42L);
    long v = seg.get(ValueLayout.JAVA_LONG, 0);
}                                                         // 之后访问 seg 抛 IllegalStateException
```
旧的 `sun.misc.Unsafe` 无任何安全检查，越界即 JVM 崩溃；FFM 有边界和生命周期检查。

`OffHeapTickerMap(int maxEntries)`（`AutoCloseable`）：一整块 64 字节对齐，每槽 16 字节 `[key:8][value:8]`，`key == 0` 空，4 槽正好一条缓存行（x86）。槽数 = 不小于 `2·maxEntries` 的 2 的幂；满了再插入**新** key → `IllegalStateException`，已有 key 仍可更新；没有 `remove`、没有 `resize`；`key ≤ 0` 或 `maxEntries ∉ [1, 2²⁸]` → `IllegalArgumentException`。`close()` 幂等，之后任何访问 → `IllegalStateException`。必须能从别的线程访问，所以用 `Arena.ofShared()`（`ofConfined()` 在别的线程访问会 `WrongThreadException`）。

用处：布局对齐自控；GC 看不到这块内存；可映射文件 / 共享内存。代价：手动 close、每次访问有边界检查、无自动扩容。**堆外没有更快**（4.1 vs 4.0；11.8 vs 11.1）；好处是不占堆、GC 看不见、布局可控；GC 停顿没测，不对「GC 抖动」下定量结论。

C++：没有 GC，剩下的是对齐、定长、地址不变、对象生命周期；`aligned new` 不要和普通 `delete` 混用。
