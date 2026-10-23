---
id: hl-javaq-d-q16-main
node: java-questions.d-memory
type: qa
step: 21
---
## Q
Java 里什么时候、怎么用堆外内存（off-heap）？风险是什么？
When and how would you use off-heap memory in Java? What are the risks?

## A
一句话：堆外 = **不受 GC 管理**的内存。方式：`ByteBuffer.allocateDirect`（受 `-XX:MaxDirectMemorySize` 限制）、`MappedByteBuffer`（mmap 文件）、`sun.misc.Unsafe`（内部 API）、**FFM API**（`Arena` + `MemorySegment`，21 预览）。

用途：
- 大数据缓存，堆变小，GC 更快、不扫描内容。
- 与 native / I/O 零拷贝。
- 跨进程共享。
- 自控布局（`StructLayout` 描述 C 风格 struct，如 24 字节的 Order 记录）。

风险：手动生命周期、越界 / 悬空、泄漏在堆 dump 里不可见。
