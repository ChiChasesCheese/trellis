---
id: hl-javaq-j-q44-pitfalls
node: java-questions.j-storage
type: qa
step: 5
---
## Q
`MappedByteBuffer` 的五个坑分别是什么？mmap 能保证持久性吗？怎么用 mmap 做追加日志？
Does mmap give you durability? How would you build an append-only log with mmap?

## A
1. **缺页造成尾延迟**：首次访问冷页要读盘（毫秒），线程卡在一次"普通内存读"上，JVM 也不知道（还会拖慢 safepoint 到达）。可 `MappedByteBuffer.load()` 预热、`mlock`（原生）。
2. **无法显式 unmap**：映射在对象被 GC 时才释放（FFM 的 `Arena` 映射可确定性关闭，21 仍是预览）。
3. **大小**：`ByteBuffer` 下标是 `int`，单个映射 ≤ 2 GB（要分段映射）；FFM `MemorySegment` 用 `long`。
4. **I/O 错误**（磁盘满、文件被截断）发生在访问内存时，Java 里表现为 `InternalError` / JVM 崩溃，不是好处理的 `IOException`。
5. **持久化**同 write：`MappedByteBuffer.force()` ≈ `msync`；mmap **本身不给持久性**。

追加日志：预分配固定大小段文件 + 映射 + 原子推进写指针；写满切下一段。
