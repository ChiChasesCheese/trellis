---
id: hl-ld01-message-layout
node: problems.ld01-spsc-channel
type: qa
step: 8
---
## Q
`MessageRing` 的内存布局和记录格式是什么？`init` / `attach` 的顺序为什么重要？

## A
段布局（`HEADER_BYTES = 512`，`segmentBytes(capacity) = 512 + capacity`）：
```
偏移    0  magic     long   0x5350534352494E47 ("SPSCRING")，最后用 release 写
偏移    8  capacity  int
偏移   12  version   int    = 1
偏移  128  head      long   消费者已消费的字节计数（只有消费者写）
偏移  256  tail      long   生产者已发布的字节计数（只有生产者写）
偏移  264  closed    long   生产者 finish() 后置 1
偏移  512  数据区    capacity 字节
```
头部各字段分开缓存行（head 在 128，tail 在 256），数据从 512 开始。

**记录** = `[len:int32][payload][补零到 8 字节对齐]`，总长 `recordSize(len) = (4 + len + 7) & ~7`；`maxPayload = capacity - 4`。对齐的好处：记录总从 8 的倍数偏移开始，4 字节长度字段永不跨越数据区末尾，`int/long` 读写保持对齐。`head/tail` 是**字节**计数。例：空消息（len=0）占 8；len=4 → 8；len=5 → 16；len=`maxPayload` 恰好占满；`maxPayload+1` → `IllegalArgumentException`。

**`init`**：清零头部、写 capacity/version，**最后**才 release 写 `magic`；容量非法或 segment 太小 → `IllegalArgumentException`。**`attach`**：先 acquire 读 `magic`，对了才信任别的字段；`magic/version/尺寸` 不对 → `IllegalStateException`。这与 `tail` 同一「先写数据后发布」协议。对着全零 / 随机内容 / 太小的文件 `open` 得明确异常而非读到垃圾。

`offer`：`msg.length > maxPayload()` → `IllegalArgumentException`（**永远**放不下，不同于「暂时满」的 `false`：前者是 bug，后者是背压）；`finish()` 之后 → `IllegalStateException`。

原子访问：`VarHandle` 用 `MethodHandles.memorySegmentViewVarHandle(ValueLayout.JAVA_LONG)`，坐标 `(MemorySegment, long 字节偏移)`（JDK 21 里 `ValueLayout.JAVA_LONG.varHandle()` 只有 `(MemorySegment)` 一个坐标，JDK 22 才加偏移）。长度前缀用 `JAVA_INT_UNALIGNED`（不依赖 segment 基址对齐）；拷贝 `MemorySegment.copy(msg, 0, seg, JAVA_BYTE, at + 4, len)`。**堆上 `byte[]` 段不支持 8 字节对齐的原子访问**（`Misaligned access`）——环必须建在原生 / 映射内存上，测试用 `Arena.ofShared().allocate(bytes, 128)`。

内存序同 Part 2：数据字节和长度都是普通写，只有 `tail` 用 `setRelease` 保护之前所有普通写。
