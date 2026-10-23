---
id: hl-ld01-ipc-mmap
node: problems.ld01-spsc-channel
type: qa
step: 2
---
## Q
进程间通信（IPC）有哪几种？为什么低延迟系统首选共享内存（`mmap`）？Java 21 里怎么映射文件？

## A
线程共享同一进程内存（要注意可见性）；进程默认**隔离**，各有虚拟地址空间，A 的 `0x1000` 与 B 的 `0x1000` 通常是不同物理内存，传数据要经 IPC：管道、套接字、消息队列、**共享内存**。

管道和套接字每次传输都要**系统调用**（`write/read`），数据在内核缓冲区拷贝一到两次，还可能让线程睡眠、唤醒（微秒量级，消息边界要自己处理）。**共享内存**把同一批物理页映射进两个进程的地址空间，之后直接读写，无系统调用、无拷贝，延迟低一个数量级。

**`mmap`** 把文件（或匿名内存）映射到进程虚拟地址空间，像访问数组一样访问文件。两个进程用 `MAP_SHARED` 映射**同一个文件**，两进程的虚拟页指向同一批物理页（页缓存，page cache）。A 写一个字节，B 立刻读到（缓存一致性保证），无系统调用。文件只是「会合点」（也可用 `/dev/shm`、`shm_open`）；好处：跨平台、易清理、**进程崩溃后数据还在**。第一次访问某页触发缺页（page fault），由内核分配或读入物理页——一次性成本。

JDK 21（FFM 预览）：
```java
try (FileChannel ch = FileChannel.open(file, CREATE, READ, WRITE);
     Arena arena = Arena.ofShared()) {
    MemorySegment seg = ch.map(FileChannel.MapMode.READ_WRITE, 0, size, arena);  // 文件扩展到 size，新增部分全零
}   // arena.close() = 取消映射（munmap）；文件还在磁盘上
```
对比老办法 `MappedByteBuffer`：限 2 GiB（`int` 索引）、无确定性取消映射、原子访问要 `Unsafe`。FFM 的 `MemorySegment` + `Arena`：长度 `long`，`Arena.close()` 确定性取消映射。

最笨的方案：`ArrayList` + `remove(0)` O(n)；`ArrayBlockingQueue`（锁 + 条件变量）竞争时睡眠 / 唤醒要系统调用、延迟抖动，且**跨不了进程**；套接字 / 管道微秒量级。
