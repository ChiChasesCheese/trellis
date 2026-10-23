---
id: hl-javaq-d-q16-risks
node: java-questions.d-memory
type: qa
step: 22
---
## Q
堆外内存的四类风险分别是什么？`DirectByteBuffer` 的内存什么时候释放，为什么会 OOM？怎么查堆外泄漏？

## A
1. **生命周期**：`DirectByteBuffer` 的内存要等对象被 GC 才释放（通过 `Cleaner`），堆压力小时可能很久不释放，撞上上限报堆外 OOM（例：`MaxDirectMemorySize=16m` 时分配 64 MB 报 `Cannot reserve 67108864 bytes of direct buffer memory`）。
2. **越界**：`ByteBuffer` 和 `MemorySegment` 检查边界；`Unsafe` 不检查，写错直接崩 JVM。
3. **不可见**：堆 dump 里看不到。
4. **序列化**要自己定义字节格式，字节序用 `ByteOrder.nativeOrder()`。

查泄漏：`-XX:NativeMemoryTracking=summary` 加 `jcmd <pid> VM.native_memory`；`BufferPoolMXBean`。
