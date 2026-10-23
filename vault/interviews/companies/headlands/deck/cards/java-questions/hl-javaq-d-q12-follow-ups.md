---
id: hl-javaq-d-q12-follow-ups
node: java-questions.d-memory
type: qa
step: 9
---
## Q
`arraycopy` 拷对象数组是深拷贝吗？怎么在不经过堆的情况下拷贝大缓冲区？
Is arraycopy a deep copy of an object array? How would you copy a large buffer without going through the heap?

## A
- **不是深拷贝**：拷的是引用，不是对象，是浅拷贝。写屏障 / 卡表（GC 记账）也让引用数组的拷贝比原始类型数组略贵。
- **不经过堆**：对 direct buffer 用 `ByteBuffer.put(ByteBuffer)`；`MemorySegment.copy`；文件到 socket 用 `FileChannel.transferTo`（零拷贝，zero-copy）。
