---
id: hl-os-mappedbytebuffer
node: foundations.os-processes-threads-ipc
type: qa
step: 21
---
## Q
用传统 `MappedByteBuffer` 映射文件并写入一个 long 怎么写？它有哪些限制和坑？

## A
```java
try (FileChannel ch = FileChannel.open(p, CREATE, READ, WRITE)) {
    MappedByteBuffer mb = ch.map(FileChannel.MapMode.READ_WRITE, 0, 4096);
    mb.order(ByteOrder.nativeOrder());   // 默认大端！
    mb.putLong(0, 0xCAFEBABEL);          // 绝对写，不影响 position
    mb.force();                           // msync，请求落盘
}
```
限制和坑：
- 每次映射最大 **2 GB**（`ByteBuffer` 用 `int` 索引）；
- **没有确定性的取消映射**，要等 `MappedByteBuffer` 被 GC 回收；
- **字节序默认大端**，x86 / ARM 本地是小端：写 `0xCAFEBABEL` 再用 FFM 的 `JAVA_LONG` 读会读到 `0xBEBAFECA00000000`，必须 `order(nativeOrder())`；
- 访问映射区时底层文件被别的进程截断，会导致 JVM 崩溃（`SIGBUS`）或抛 `InternalError`。
