---
id: hl-javaq-h-q39-code
node: java-questions.h-ipc
type: qa
step: 5
---
## Q
写出两个 JVM 通过 mmap 做 ping-pong 的核心代码：怎么声明 `VarHandle`、怎么发布、怎么等回应？为什么普通 `putLong` 不行？

## A
```java
static final VarHandle LONGS = MethodHandles
    .byteBufferViewVarHandle(long[].class, ByteOrder.nativeOrder());
LONGS.setVolatile(mb, 0, i);   // publish
while ((long) LONGS.getVolatile(mb, 64) != i)
    Thread.onSpinWait();       // wait for reply
```
- 父写序号 `i` 到偏移 0，子看到后把 `i` 回写到偏移 64，父自旋读偏移 64；结果 **0.15 µs**/往返。
- 偏移 0 和 64 分在**不同缓存行**（防伪共享）。
- **可见性**：两个进程里的 JMM 互不相知；但 `VarHandle` 的 volatile / acquire / release 访问会生成相应的内存屏障 / 指令，在同机同一页上跨进程同样有效（硬件缓存一致性）。普通 `ByteBuffer.putLong` **没有**这个保证（可能被编译器缓存 / 重排）。
