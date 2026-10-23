---
id: hl-javaq-j-q44-say60
node: java-questions.j-storage
type: qa
step: 10
---
## Q
用英文 60 秒回答：`mmap` vs `read/write` for files: when would you use a `MappedByteBuffer`, and what are its pitfalls?

## A
结构：mmap 直接映射 page cache，读是内存访问 → 适合大文件随机访问与进程间共享 → 坑（冷页的缺页尾延迟、无法确定性 unmap、2 GB 限制、I/O 错误变成 InternalError）→ 持久仍需 force → 顺序流式读用普通 FileChannel。

> "`mmap` maps the file's page-cache pages directly into the process, so reading is a memory access and there's no syscall or extra copy per read; a page that isn't resident faults in from disk. It's great for large random-access files and for sharing memory between processes. The pitfalls: a cold page makes a plain memory read block for milliseconds, which hurts tail latency; in Java the mapping can't be deterministically unmapped before Java 22's FFM, a single `ByteBuffer` mapping is capped at 2 GB, and I/O errors surface as `InternalError` rather than `IOException`. For durability you still need `force`, which is `msync`. For sequential streaming I'd happily use plain `FileChannel` reads."
