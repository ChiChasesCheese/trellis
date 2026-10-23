---
id: hl-j17-bytebuffer-problems
node: java21.j17-ffm-api
type: qa
step: 3
---
## Q
`ByteBuffer.allocateDirect` 有哪三个结构性问题？FFM 各用什么解决？

## A
1. **容量是 `int`**，最大约 2 GB。想要 3 GB 的表，`(int) 3_000_000_000L = -1294967296` 抛 `IllegalArgumentException`，只能拆成多个 buffer → FFM 的 `MemorySegment.byteSize()` 是 `long`。
2. **没有 `close()`**：要等 GC 发现 `ByteBuffer` 不可达再由 `Cleaner` 释放；GC 不紧张时可能很久不释放，`-XX:MaxDirectMemorySize` 满了就 `OutOfMemoryError: Direct buffer memory`。想「用完立刻还」只能用 `Unsafe` 或反射黑科技 → FFM 的 `Arena` + `close()`。
3. **没有结构**：偏移量、类型靠人记，字段偏移（如 `ID=0, PX=8, QTY=16`）是魔法数字，改一个字段要改一堆 → FFM 的 `MemoryLayout` / `VarHandle`。
