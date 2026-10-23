---
id: hl-ld01-sharedchannel
node: problems.ld01-spsc-channel
type: qa
step: 11
---
## Q
`SharedChannel` 的 `create` / `open` / `close` 语义是什么？实现里最容易出错的顺序问题是什么？

## A
API：`create(Path, capacity)`、`open(Path)`、`capacity()`、`maxPayload()`、`send`/`finish`（生产者）、`receive`/`isDrained`（消费者）、`close()`（取消映射，幂等，**不删文件**）。

- **`create`**：新建 / 覆盖文件，大小 `MessageRing.segmentBytes(capacity)`；`FileChannel.map(READ_WRITE, 0, size, arena)`（`Arena.ofShared()`）得到 `MemorySegment`，再 `MessageRing.init`。`capacity` 非法 → `IllegalArgumentException`，且**不要动文件**；
- **`open`**：映射已有文件并 `attach`；文件不存在 → `NoSuchFileException`；文件太小 / 全零 / 随机内容 → `IllegalStateException`；
- **`close`** 之后 `send/receive` 抛 `IllegalStateException`；文件留在磁盘上；关闭后重新 `open`，积压的消息还在（数据在文件里）；
- `create` 必须在对方 `open` 之前完成。

```java
long size = MessageRing.segmentBytes(capacity);       // 先校验 capacity，再动文件
Arena arena = Arena.ofShared();
try (FileChannel ch = FileChannel.open(file, CREATE, READ, WRITE, TRUNCATE_EXISTING)) {
    MemorySegment seg = ch.map(MapMode.READ_WRITE, 0, size, arena);
    return new SharedChannel(arena, MessageRing.init(seg, capacity));
} catch (IOException | RuntimeException e) { arena.close(); throw e; }
```
**顺序**：`segmentBytes(capacity)` 在 `FileChannel.open` **之前**调用且自己校验容量；若先 `open(…, TRUNCATE_EXISTING)` 再校验，对已有文件调 `create(file, 100)` 会先截断再抛异常——调用方丢了数据。`try-with-resources` 关的是 `FileChannel`，**映射仍有效**直到 `arena.close()`；失败路径要关 `arena`，不泄漏映射。

数据：父进程发 500 万条消息（平均约 32 字节，共约 160 MB）、子进程收，约 190 ms，约 2600 万条/秒（含子 JVM 启动，每端每条各分配一个 `byte[]`）；单进程两线程 1000 万条 `long` 约 180 ms（约 5500 万条/秒）；200 万条变长消息两线程 87 ms。

变体：C++ 版 `std::atomic<uint64_t>` + `memory_order_release/acquire`，`mmap`/`shm_open`；`alignas(64)`、`std::hardware_destructive_interference_size`。
