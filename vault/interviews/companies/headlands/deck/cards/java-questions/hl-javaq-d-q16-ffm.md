---
id: hl-javaq-d-q16-ffm
node: java-questions.d-memory
type: qa
step: 23
---
## Q
FFM API（Foreign Function and Memory）的 `Arena` 和 `MemorySegment` 比 `ByteBuffer`、`Unsafe` 好在哪？Java 21 里它是什么状态？

## A
- `Arena` 提供**确定的关闭**：关闭后再访问 segment 抛 `IllegalStateException: Already closed`，而不是崩 JVM。
- `MemorySegment` **检查边界**：越界抛 `IndexOutOfBoundsException`。例：1M 个 long 堆外，`byteSize=8000000`。
- 用 `StructLayout` 描述 C 风格结构，可定义 24 字节、对齐 8 的 Order 记录。
- 21 里 FFM 仍是**预览**（需要 `--enable-preview`），22 正式；生产上很多公司仍用基于 `ByteBuffer` / `Unsafe` 的库（Chronicle、Aeron 之类）。
- 追问"为什么不直接用 `Unsafe`"：内部 API，不安全，将被弃用；FFM 是正式替代。
