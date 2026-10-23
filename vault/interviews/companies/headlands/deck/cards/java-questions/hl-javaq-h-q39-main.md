---
id: hl-javaq-h-q39-main
node: java-questions.h-ipc
type: qa
step: 4
---
## Q
在 Java 里怎么实现共享内存 IPC？怎么保证跨进程的可见性？
How would you implement shared memory IPC in Java? How do you get correct visibility across processes?

## A
一句话：用 `FileChannel.map` 把同一个文件（Linux 上放 `/dev/shm`）映射进两个 JVM，得到 `MappedByteBuffer`；用 `VarHandle`（`MethodHandles.byteBufferViewVarHandle`）对映射内存做 `getVolatile / setVolatile`（或 acquire / release）；设计成**单生产者单消费者环形缓冲**：各自只写自己的序号，先写数据后发布序号。

- 生产者：写 `slot[tail % N]`，然后 `setRelease(tail, tail+1)` 发布。
- 消费者：`getAcquire(tail) > head` 时读 `slot[head % N]`，然后 `setRelease(head, head+1)`。
- 布局：head（8B）、pad 到 64B、tail（8B）、pad、环数据——head / tail 在不同缓存行防伪共享。
