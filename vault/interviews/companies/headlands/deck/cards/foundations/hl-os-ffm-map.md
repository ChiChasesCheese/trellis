---
id: hl-os-ffm-map
node: foundations.os-processes-threads-ipc
type: qa
step: 22
---
## Q
用 FFM API（`java.lang.foreign`）映射文件怎么写？相比 `MappedByteBuffer` 改进了什么？JDK 21 的状态是什么？

## A
```java
try (FileChannel ch = FileChannel.open(p, CREATE, READ, WRITE);
     Arena arena = Arena.ofShared()) {
    MemorySegment seg = ch.map(FileChannel.MapMode.READ_WRITE, 0, 1L << 20, arena);
    seg.set(ValueLayout.JAVA_LONG, 0, 42L);
    seg.set(ValueLayout.JAVA_INT, 8, 7);
}   // 这里确定性取消映射，再访问会抛异常
```
改进：
- 最大映射大小：`long`，可达 TB 级（`MappedByteBuffer` 2 GB）；
- 取消映射：`Arena.close()` 确定性（原先靠 GC）；
- 字节序：本地字节序，大端要显式 `withOrder`；
- 访问检查：越界检查 + 时间安全检查（已释放抛异常）。

状态：FFM（Project Panama）在 JDK 21 是第三次**预览**（JEP 442），编译和运行都要 `--enable-preview`，JDK 22 正式。`Arena.ofConfined()` 只允许创建线程访问，`ofShared()` 允许多线程，跨进程共享通常用 `ofShared()`。
